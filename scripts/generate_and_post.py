#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_and_post.py

ブログ下書きファイルを読み込み、画像生成 → Wixアップロード → Wix下書き作成 まで自動化する。

使い方:
    python scripts/generate_and_post.py drafts/draft_2026-03-07_タイトル.md

必要な環境変数:
    WIX_API_KEY    - Wix APIキー (IST.xxx...)
    WIX_SITE_ID    - WixサイトID
    OPENAI_API_KEY - OpenAI APIキー (DALL-E 3 画像生成用)
"""

import os
import re
import sys
import time
import json
import uuid
import requests
from pathlib import Path
from typing import Optional, List, Dict
from openai import OpenAI

# ── 設定 ──────────────────────────────────────────────────────────────────────

WIX_API_KEY    = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID    = os.environ.get("WIX_SITE_ID", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

WIX_BASE = "https://www.wixapis.com"

# ── ユーティリティ ──────────────────────────────────────────────────────────────

def wix_headers():
    return {
        "Authorization": WIX_API_KEY,
        "wix-site-id": WIX_SITE_ID,
        "Content-Type": "application/json",
    }

def new_id():
    return str(uuid.uuid4())[:8]

# ── ドラフトファイルのパース ────────────────────────────────────────────────────

def parse_draft(file_path: str) -> dict:
    text = Path(file_path).read_text(encoding="utf-8")

    def find(pattern, default="", dotall=True):
        flags = re.DOTALL if dotall else 0
        m = re.search(pattern, text, flags)
        return m.group(1).strip() if m else default

    # タイトル・キーワードは1行のみ（DOTALL不使用）
    title    = find(r'\*\*タイトル：\*\*\n([^\n]+)', dotall=False)
    keywords = find(r'\*\*フォーカスキーワード：\*\*\n([^\n]+)', dotall=False)
    meta     = find(r'\*\*メタディスクリプション[^*]*\*\*\n(.+?)(?=\n\n|\n---)')
    body     = find(r'## 本文\n\n(.+?)(?=\n## 差し込み画像プロンプト|\Z)')

    # 画像プロンプト抽出
    image_prompts = []
    for m in re.finditer(
        r'\*\*(画像\d+[^*]*)\*\*.*?- 英語：(.+?)\n.*?- キャプション：(.+?)(?=\n\n|\*\*画像|\Z)',
        text, re.DOTALL
    ):
        image_prompts.append({
            "name":    m.group(1).strip(),
            "prompt":  m.group(2).strip(),
            "caption": m.group(3).strip(),
        })

    return {
        "title":         title,
        "meta":          meta,
        "keywords":      keywords,
        "body":          body,
        "image_prompts": image_prompts,
    }

# ── Markdown → Ricos 変換 ──────────────────────────────────────────────────────

def make_plain_text(text: str) -> dict:
    return {
        "type": "TEXT",
        "id":   new_id(),
        "nodes": [],
        "textData": {"text": text, "decorations": []},
    }

def make_text_nodes(text: str) -> list:
    """**bold** とURLリンクを含むテキストをパースしてTEXTノードのリストを返す"""
    result = []
    pattern = re.compile(r'\*\*(.+?)\*\*|https?://\S+')
    pos = 0

    for m in pattern.finditer(text):
        if m.start() > pos:
            plain = text[pos:m.start()]
            if plain:
                result.append(make_plain_text(plain))

        matched = m.group(0)
        if matched.startswith('**'):
            result.append({
                "type": "TEXT",
                "id":   new_id(),
                "nodes": [],
                "textData": {
                    "text": m.group(1),
                    "decorations": [{"type": "BOLD", "fontWeightValue": 700}],
                },
            })
        else:
            result.append({
                "type": "TEXT",
                "id":   new_id(),
                "nodes": [],
                "textData": {
                    "text": matched,
                    "decorations": [{
                        "type": "LINK",
                        "linkData": {
                            "link": {"url": matched, "target": "BLANK"}
                        },
                    }],
                },
            })
        pos = m.end()

    if pos < len(text):
        remaining = text[pos:]
        if remaining:
            result.append(make_plain_text(remaining))

    if not result:
        result.append(make_plain_text(""))

    return result

def md_to_ricos_nodes(md: str, image_urls: list) -> list:
    """
    MarkdownをパースしてRicosノードのリストを返す。
    image_urls: [{"url": ..., "caption": ...}, ...]
    画像は1番目・3番目・5番目の --- (divider) の直後に挿入する。
    """
    nodes = []
    img_idx = 0
    divider_count = 0
    bullet_buffer = []

    def flush_bullets():
        nonlocal bullet_buffer
        if not bullet_buffer:
            return
        list_items = []
        for item_text in bullet_buffer:
            list_items.append({
                "type": "LIST_ITEM",
                "id":   new_id(),
                "nodes": [{
                    "type": "PARAGRAPH",
                    "id":   new_id(),
                    "nodes": make_text_nodes(item_text),
                    "paragraphData": {},
                }],
            })
        nodes.append({
            "type": "BULLETED_LIST",
            "id":   new_id(),
            "nodes": list_items,
        })
        bullet_buffer.clear()

    lines = md.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]

        # 見出し (## )
        if line.startswith('## '):
            flush_bullets()
            nodes.append({
                "type": "HEADING",
                "id":   new_id(),
                "nodes": make_text_nodes(line[3:].strip()),
                "headingData": {"level": 2},
            })
            i += 1
            continue

        # 区切り線 (---)
        if line.strip() == '---':
            flush_bullets()
            nodes.append({
                "type": "DIVIDER",
                "id":   new_id(),
                "nodes": [],
                "dividerData": {},
            })
            divider_count += 1
            # 1・3・5番目の区切りの後に画像を挿入
            if divider_count in (1, 3, 5) and img_idx < len(image_urls):
                img = image_urls[img_idx]
                raw_url = img.get("url", "")
                if raw_url:
                    # static URL → wix:image:// URI に変換
                    media_m = re.search(r'/media/([^/\s]+)', raw_url)
                    wix_uri = f"wix:image://v1/{media_m.group(1)}/img.png" if media_m else raw_url
                    nodes.append({
                        "type": "IMAGE",
                        "id":   new_id(),
                        "nodes": [],
                        "imageData": {
                            "image": {"src": {"url": wix_uri}},
                            "caption": img["caption"],
                        },
                    })
                img_idx += 1
            i += 1
            continue

        # 箇条書き (- )
        if line.startswith('- '):
            bullet_buffer.append(line[2:].strip())
            i += 1
            continue

        # 空行
        if line.strip() == '':
            flush_bullets()
            i += 1
            continue

        # 通常段落
        flush_bullets()
        nodes.append({
            "type": "PARAGRAPH",
            "id":   new_id(),
            "nodes": make_text_nodes(line.strip()),
            "paragraphData": {},
        })
        i += 1

    flush_bullets()
    return nodes

# ── DALL-E 3 画像生成 ──────────────────────────────────────────────────────────

def generate_images(image_prompts: list, draft_path: str) -> list:
    """DALL-E 3で画像を生成してdrafts/images/に保存し、結果リストを返す"""
    client = OpenAI(api_key=OPENAI_API_KEY)

    date_match = re.search(r'\d{4}-\d{2}-\d{2}', Path(draft_path).name)
    date_str = date_match.group(0) if date_match else "unknown"

    images_dir = Path(draft_path).parent / "images"
    images_dir.mkdir(exist_ok=True)

    results = []
    for idx, img in enumerate(image_prompts, 1):
        print(f"  [{idx}/{len(image_prompts)}] 画像生成中: {img['name'][:40]}...")
        resp = client.images.generate(
            model="dall-e-3",
            prompt=img["prompt"],
            size="1792x1024",
            quality="standard",
            n=1,
        )
        dall_e_url = resp.data[0].url

        # ローカルに保存
        img_resp = requests.get(dall_e_url, timeout=60)
        local_path = images_dir / f"{date_str}_img{idx}.png"
        local_path.write_bytes(img_resp.content)
        print(f"       保存完了: {local_path.name}")

        results.append({
            "dall_e_url": dall_e_url,
            "local_path": str(local_path),
            "caption":    img["caption"],
            "name":       img["name"],
        })

    return results

# ── Wix Media へアップロード ───────────────────────────────────────────────────

def upload_to_wix_media(image_info: dict) -> Optional[dict]:
    """DALL-E URLをWix Media Managerに取り込み、ファイル情報dictを返す"""
    print(f"  Wixに取り込み中: {image_info['name'][:40]}...")

    resp = requests.post(
        f"{WIX_BASE}/site-media/v1/files/import",
        headers=wix_headers(),
        json={
            "url":         image_info["dall_e_url"],
            "displayName": image_info["name"],
            "mimeType":    "image/png",
        },
        timeout=30,
    )

    if not resp.ok:
        print(f"    ⚠ import失敗 ({resp.status_code}): {resp.text[:200]}")
        return None

    data = resp.json()
    file_id = (data.get("file") or {}).get("id") or data.get("fileId")

    if not file_id:
        print(f"    ⚠ file_idが取得できない: {json.dumps(data, ensure_ascii=False)[:200]}")
        return None

    # READY になるまで待機
    for attempt in range(20):
        time.sleep(3)
        check = requests.get(
            f"{WIX_BASE}/site-media/v1/files/{file_id}",
            headers=wix_headers(),
            timeout=15,
        )
        if check.ok:
            file_data = check.json().get("file", {})
            state = file_data.get("state", "")
            if state in ("READY", "OK"):
                url = file_data.get("url", "")
                media_match = re.search(r'/media/([^?#\s]+)', url)
                media_id = media_match.group(1) if media_match else file_data.get("id", "")
                print(f"       取り込み完了: {url[:70]}...")
                return {
                    "url":      url,
                    "id":       media_id,
                    "height":   1024,
                    "width":    1792,
                    "filename": file_data.get("displayName", "img.png"),
                }
            print(f"       待機中... ({state}, {attempt + 1}/20)")
        else:
            print(f"       確認失敗 ({check.status_code})")

    print("    ⚠ タイムアウト: ファイルがREADYにならない")
    return None

# ── Wix Blog 下書き作成 ────────────────────────────────────────────────────────

def create_wix_draft(draft_info: dict, ricos_nodes: list, featured_image: Optional[dict]) -> Optional[str]:
    """Wix Blog v3 で下書きを作成し、draft IDを返す"""

    body = {
        "draftPost": {
            "title":    draft_info["title"],
            "memberId": "69e25236-d316-4da8-92e4-f500aca1fe37",
            "richContent": {"nodes": ricos_nodes},
        }
    }

    # アイキャッチ画像（既存投稿と同じ形式）
    if featured_image:
        body["draftPost"]["media"] = {
            "custom": True,
            "wixMedia": {
                "image": {
                    "id":       featured_image["id"],
                    "url":      featured_image["url"],
                    "height":   featured_image["height"],
                    "width":    featured_image["width"],
                    "filename": featured_image["filename"],
                }
            },
        }

    # SEOデータ
    seo_tags = []
    if draft_info["title"]:
        seo_tags.append({"type": "title", "children": draft_info["title"]})
    if draft_info["meta"]:
        seo_tags.append({
            "type":  "meta",
            "props": {"name": "description", "content": draft_info["meta"]},
        })
    if seo_tags:
        body["draftPost"]["seoData"] = {"tags": seo_tags}

    resp = requests.post(
        f"{WIX_BASE}/blog/v3/draft-posts",
        headers=wix_headers(),
        json=body,
        timeout=30,
    )

    if not resp.ok:
        print(f"  ⚠ 下書き作成失敗 ({resp.status_code}):")
        print(f"  {resp.text[:500]}")
        return None

    draft_id = resp.json().get("draftPost", {}).get("id", "")
    return draft_id

# ── メイン ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("使い方: python scripts/generate_and_post.py <draft_file.md>")
        sys.exit(1)

    draft_path = sys.argv[1]
    if not Path(draft_path).exists():
        print(f"ファイルが見つかりません: {draft_path}")
        sys.exit(1)

    # 環境変数チェック
    missing = [v for v in ("WIX_API_KEY", "WIX_SITE_ID", "OPENAI_API_KEY") if not os.environ.get(v)]
    if missing:
        print(f"環境変数が未設定: {', '.join(missing)}")
        print("~/.zshrc に export WIX_API_KEY=... などを追記してから source ~/.zshrc を実行してください。")
        sys.exit(1)

    print(f"\n[1/4] ドラフトを読み込み中: {draft_path}")
    info = parse_draft(draft_path)
    print(f"      タイトル: {info['title']}")
    print(f"      画像プロンプト数: {len(info['image_prompts'])}")

    print("\n[2/4] DALL-E 3 で画像を生成中...")
    image_results = generate_images(info["image_prompts"], draft_path)

    print("\n[3/4] Wix Media Manager に取り込み中...")
    wix_images = []
    for img in image_results:
        result = upload_to_wix_media(img)
        wix_images.append({
            "file":    result,           # None の場合は画像なしでノードをスキップ
            "caption": img["caption"],
        })

    print("\n[4/4] Wix Blog 下書きを作成中...")
    # Ricos用に url と caption だけ渡す
    ricos_image_list = [{"url": w["file"]["url"] if w["file"] else None, "caption": w["caption"]} for w in wix_images]
    ricos_nodes = md_to_ricos_nodes(info["body"], ricos_image_list)
    print(f"      Ricosノード数: {len(ricos_nodes)}")

    featured_image = wix_images[0]["file"] if wix_images and wix_images[0]["file"] else None
    draft_id = create_wix_draft(info, ricos_nodes, featured_image)

    if draft_id:
        print(f"\n完了!")
        print(f"  Wix下書きID: {draft_id}")
        print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")
    else:
        print("\n下書き作成に失敗しました。上のエラーを確認してください。")
        sys.exit(1)

if __name__ == "__main__":
    main()
