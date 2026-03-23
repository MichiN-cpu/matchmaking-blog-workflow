#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_pipeline.py

トピック選択 → 記事生成 → 画像生成（DALL-E 3） → Wix下書き投稿 を一括実行。
GitHub Actions（3日ごと）および手動実行の両方で使用。

必要な環境変数:
    ANTHROPIC_API_KEY  - Claude で記事生成（推奨）
    OPENAI_API_KEY     - DALL-E 3 で画像生成（必須）
    WIX_API_KEY        - Wix API キー
    WIX_SITE_ID        - Wix サイト ID
"""

import os
import re
import time
import uuid
import requests
from datetime import date
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent

# ── 環境変数 ──────────────────────────────────────────────────────────────────

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OPENAI_KEY    = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY   = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID   = os.environ.get("WIX_SITE_ID", "")
WIX_BASE      = "https://www.wixapis.com"
MEMBER_ID     = "69e25236-d316-4da8-92e4-f500aca1fe37"

# ── ユーティリティ ─────────────────────────────────────────────────────────────

def wix_headers():
    return {
        "Authorization": WIX_API_KEY,
        "wix-site-id":   WIX_SITE_ID,
        "Content-Type":  "application/json",
    }

def new_id():
    return str(uuid.uuid4())[:8]

def load(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def save(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

# ── ① トピック選択 ────────────────────────────────────────────────────────────

def pick_topic(stock: str):
    parts = stock.split("---", 1)
    if len(parts) < 2:
        return None, None
    for line in parts[1].strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        title = line[2:].strip() if line.startswith("- ") else line
        return title, line
    return None, None

def remove_topic(stock: str, exact_line: str) -> str:
    lines = stock.splitlines()
    result, i = [], 0
    while i < len(lines):
        if lines[i].strip() == exact_line.strip():
            i += 1
            if i < len(lines) and lines[i].startswith("　"):
                i += 1
            continue
        result.append(lines[i])
        i += 1
    return "\n".join(result)

# ── ② 記事生成 ────────────────────────────────────────────────────────────────

def build_article_prompt(topic, guidelines, brief):
    return f"""以下は「あすなる愛媛」の結婚相談所ブログ用の編集方針とブリーフです。この2つに厳密に沿って、指定トピックで記事下書きを1本書いてください。

【編集方針】
{guidelines}

【あすなる愛媛用ブリーフ】
{brief}

【依頼】
トピック：「{topic}」

上記トピックで、**「あすなる愛媛」のブログ**として記事の本文を書いてください。

■ あすなる愛媛らしさ（必須）
- **一般的な結婚相談所の説明にならないように。** 読んだ人が「この相談所なら話を聞いてみたい」と感じる、具体的で温かみのあるトーンで書く。
- 記事の随所に、次の視点を自然に織り込む：少人数で一人ひとりに寄り添う／諦めないで柔軟に進められる／サポートの中身・相性で選ぶ／愛媛で婚活する人を応援／その人らしいペースで、安心して話せる場。
- 冒頭や締めで「愛媛で」「少人数で」「寄り添う」などを、押しつけにならない形で入れる。
- **避けること**：どの相談所のブログかわからないような一般的な説明。
- 歴史・成婚退会の「数」は強調しない。

■ その他
- 顧客目線・失敗しうる点・会員の幸せな未来・心理学以外の観点も入れる。
- 見出しは ## で。最後に改行を1つ入れて終えてください。
"""

def write_article(topic, guidelines, brief) -> str:
    prompt = build_article_prompt(topic, guidelines, brief)
    if ANTHROPIC_KEY:
        from anthropic import Anthropic
        client = Anthropic(api_key=ANTHROPIC_KEY)
        resp = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()
    else:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return (resp.choices[0].message.content or "").strip()

# ── ③ 画像プロンプト生成 ───────────────────────────────────────────────────────

def build_image_prompt_request(topic, body):
    return f"""以下の結婚相談所ブログ記事に合う画像プロンプトを3点、英語で作成してください。

【トピック】{topic}

【記事本文（冒頭）】
{body[:800]}

以下の形式で出力してください（余計な説明は不要）：

IMAGE1: <英語プロンプト>
IMAGE2: <英語プロンプト>
IMAGE3: <英語プロンプト>

ルール：
- flat illustration style, no text, soft warm tones, Japanese setting
- 必ず `no text` を含める
- 人物が出る場合は `East Asian appearance, black hair` を含める
- 写真ではなくイラスト調にする
"""

def generate_image_prompts(topic, body) -> list:
    prompt = build_image_prompt_request(topic, body)
    try:
        if ANTHROPIC_KEY:
            from anthropic import Anthropic
            client = Anthropic(api_key=ANTHROPIC_KEY)
            resp = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.content[0].text.strip()
        else:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_KEY)
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            text = (resp.choices[0].message.content or "").strip()
        return [m.group(1).strip() for m in re.finditer(r'IMAGE\d:\s*(.+)', text)]
    except Exception as e:
        print(f"  画像プロンプト生成エラー: {e}")
        return []

# ── ④ DALL-E 3 画像生成 → Wix Media インポート ─────────────────────────────────

def generate_and_import_images(prompts: list, date_str: str) -> list:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    results = []
    captions = ["記事のアイキャッチ画像", "記事の挿入画像2", "記事の挿入画像3"]

    for idx, prompt_text in enumerate(prompts, 1):
        label = "eyecatch" if idx == 1 else f"img{idx}"
        print(f"  [{idx}/3] DALL-E 3 生成中...")
        try:
            resp = client.images.generate(
                model="dall-e-3",
                prompt=prompt_text,
                size="1792x1024",
                quality="standard",
                n=1,
            )
            dall_e_url = resp.data[0].url
            print(f"       生成完了。Wixにインポート中...")
            file_info = import_to_wix(dall_e_url, f"{date_str}_{label}.png")
            results.append({"file": file_info, "caption": captions[idx - 1]})
        except Exception as e:
            print(f"       エラー: {e}")
            results.append({"file": None, "caption": captions[idx - 1]})

    return results

def import_to_wix(dall_e_url: str, name: str) -> Optional[dict]:
    resp = requests.post(
        f"{WIX_BASE}/site-media/v1/files/import",
        headers=wix_headers(),
        json={"url": dall_e_url, "displayName": name, "mimeType": "image/png"},
        timeout=30,
    )
    if not resp.ok:
        print(f"       import失敗: {resp.status_code}")
        return None
    data = resp.json()
    file_id = (data.get("file") or {}).get("id") or data.get("fileId")
    if not file_id:
        return None
    for i in range(20):
        time.sleep(3)
        check = requests.get(f"{WIX_BASE}/site-media/v1/files/{file_id}", headers=wix_headers(), timeout=15)
        if check.ok:
            fd = check.json().get("file", {})
            if fd.get("state") in ("READY", "OK"):
                url = fd.get("url", "")
                m = re.search(r"/media/([^?#\s]+)", url)
                return {"url": url, "id": m.group(1) if m else file_id, "height": 1024, "width": 1792, "filename": name}
            print(f"       待機中... ({fd.get('state')}, {i+1}/20)")
    print("       タイムアウト")
    return None

# ── ⑤ Wix Blog 下書き作成 ──────────────────────────────────────────────────────

def make_plain(t):
    return {"type": "TEXT", "id": new_id(), "nodes": [], "textData": {"text": t, "decorations": []}}

def make_text_nodes(t):
    result, pos = [], 0
    for m in re.compile(r'\*\*(.+?)\*\*|https?://\S+').finditer(t):
        if m.start() > pos:
            result.append(make_plain(t[pos:m.start()]))
        if m.group(0).startswith("**"):
            result.append({"type": "TEXT", "id": new_id(), "nodes": [], "textData": {"text": m.group(1), "decorations": [{"type": "BOLD", "fontWeightValue": 700}]}})
        else:
            result.append({"type": "TEXT", "id": new_id(), "nodes": [], "textData": {"text": m.group(0), "decorations": [{"type": "LINK", "linkData": {"link": {"url": m.group(0), "target": "BLANK"}}}]}})
        pos = m.end()
    if pos < len(t):
        result.append(make_plain(t[pos:]))
    return result or [make_plain("")]

def md_to_ricos(md: str, images: list) -> list:
    nodes, bullets, img_idx, div_count = [], [], 0, 0

    def flush():
        nonlocal bullets
        if not bullets:
            return
        items = [{"type": "LIST_ITEM", "id": new_id(), "nodes": [{"type": "PARAGRAPH", "id": new_id(), "nodes": make_text_nodes(b), "paragraphData": {}}]} for b in bullets]
        nodes.append({"type": "BULLETED_LIST", "id": new_id(), "nodes": items})
        bullets.clear()

    for line in md.splitlines():
        if line.startswith("## "):
            flush()
            nodes.append({"type": "HEADING", "id": new_id(), "nodes": make_text_nodes(line[3:].strip()), "headingData": {"level": 2}})
        elif line.strip() == "---":
            flush()
            nodes.append({"type": "DIVIDER", "id": new_id(), "nodes": [], "dividerData": {}})
            div_count += 1
            if div_count in (1, 3, 5) and img_idx < len(images):
                img = images[img_idx]
                if img.get("file"):
                    f = img["file"]
                    m = re.search(r"/media/([^?#\s]+)", f["url"])
                    wix_uri = f"wix:image://v1/{m.group(1)}/img.png" if m else f["url"]
                    nodes.append({"type": "IMAGE", "id": new_id(), "nodes": [], "imageData": {"image": {"src": {"url": wix_uri}}, "caption": img["caption"]}})
                img_idx += 1
        elif line.startswith("- "):
            bullets.append(line[2:].strip())
        elif line.strip() == "":
            flush()
        else:
            flush()
            nodes.append({"type": "PARAGRAPH", "id": new_id(), "nodes": make_text_nodes(line.strip()), "paragraphData": {}})
    flush()
    return nodes

def post_to_wix(title: str, body_md: str, images: list) -> Optional[str]:
    ricos = md_to_ricos(body_md, images)
    featured = images[0]["file"] if images and images[0].get("file") else None

    draft_post = {
        "title":       title,
        "memberId":    MEMBER_ID,
        "richContent": {"nodes": ricos},
    }
    if featured:
        m = re.search(r"/media/([^?#\s]+)", featured["url"])
        draft_post["media"] = {
            "custom": True,
            "wixMedia": {"image": {
                "id":       m.group(1) if m else featured["id"],
                "url":      featured["url"],
                "height":   featured["height"],
                "width":    featured["width"],
                "filename": featured["filename"],
            }},
        }

    resp = requests.post(
        f"{WIX_BASE}/blog/v3/draft-posts",
        headers=wix_headers(),
        json={"draftPost": draft_post},
        timeout=30,
    )
    if not resp.ok:
        print(f"  Wix投稿失敗: {resp.status_code}\n  {resp.text[:300]}")
        return None
    return resp.json().get("draftPost", {}).get("id")

# ── メイン ────────────────────────────────────────────────────────────────────

def main():
    missing = [v for v in ("OPENAI_API_KEY", "WIX_API_KEY", "WIX_SITE_ID") if not os.environ.get(v)]
    if missing:
        print(f"環境変数が未設定: {', '.join(missing)}")
        exit(1)

    today = date.today().strftime("%Y-%m-%d")

    # ① トピック選択
    stock_path = ROOT / "topics" / "stock.md"
    stock = load(stock_path)
    topic, exact_line = pick_topic(stock)
    if not topic:
        print("トピックが見つかりません。stock.md を確認してください。")
        exit(0)
    print(f"\n[1/5] トピック: {topic}")

    # ② 記事生成
    print("[2/5] 記事を生成中...")
    guidelines = load(ROOT / "EDITORIAL_GUIDELINES.md")
    brief = load(ROOT / "ASUNARU_EHIME_BRIEF.md")
    body = write_article(topic, guidelines, brief)
    if not body:
        print("記事生成に失敗しました。")
        exit(1)
    print(f"     完了（{len(body)}文字）")

    # ③ ファイル保存
    safe = re.sub(r'[\\/:*?"<>|\s]+', "_", topic).strip("_")[:50]
    draft_path = ROOT / "drafts" / f"draft_{today}_{safe}.md"
    save(draft_path, body)
    print(f"[3/5] 下書き保存: {draft_path.name}")

    # ④ 画像生成 → Wixインポート
    print("[4/5] 画像プロンプトを生成中...")
    img_prompts = generate_image_prompts(topic, body)
    wix_images = []
    if img_prompts:
        wix_images = generate_and_import_images(img_prompts, today)
    else:
        print("     画像プロンプト生成失敗。画像なしで続行。")

    # ⑤ Wix下書き投稿
    print("[5/5] Wixに下書きを投稿中...")
    # タイトルを本文から抽出（なければトピック名）
    title_m = re.search(r'^#\s+(.+)', body, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else topic
    draft_id = post_to_wix(title, body, wix_images)
    if not draft_id:
        exit(1)

    # ログ・stock更新
    log_path = ROOT / "used" / "log.md"
    log = load(log_path)
    new_row = f"| {today} | {topic} |"
    lines = log.splitlines()
    for i, line in enumerate(lines):
        if "|----" in line or "|----------" in line:
            lines.insert(i + 1, new_row)
            break
    save(log_path, "\n".join(lines))
    save(stock_path, remove_topic(stock, exact_line))

    print(f"\n✅ 完了！")
    print(f"   Wix下書きID: {draft_id}")
    print(f"   管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")

if __name__ == "__main__":
    main()
