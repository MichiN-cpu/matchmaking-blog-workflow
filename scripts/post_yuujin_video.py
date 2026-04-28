#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
動画告知記事：サポートなしで婚活した友人の体験談 - Wix投稿スクリプト
"""

import os
import re
import time
import uuid
import requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_ID = "fc247847-d52b-438c-ab23-95bae771dc0a"  # お知らせ

client = OpenAI(api_key=OPENAI_KEY)

def wix_headers():
    return {
        "Authorization": WIX_API_KEY,
        "wix-site-id":   WIX_SITE_ID,
        "Content-Type":  "application/json",
    }

def nid():
    return str(uuid.uuid4())[:8]

def sp():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}
    ], "paragraphData": {}}

def make_text_nodes(text):
    result, pos = [], 0
    for m in re.compile(r'https?://\S+').finditer(text):
        if m.start() > pos:
            result.append({"type": "TEXT", "id": nid(), "nodes": [],
                           "textData": {"text": text[pos:m.start()], "decorations": []}})
        result.append({"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": m.group(0), "decorations": [
                           {"type": "LINK", "linkData": {"link": {"url": m.group(0), "target": "BLANK"}}}
                       ]}})
        pos = m.end()
    if pos < len(text):
        result.append({"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": text[pos:], "decorations": []}})
    return result or [{"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": "", "decorations": []}}]

def p(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": make_text_nodes(text), "paragraphData": {}}


# ── richContent 構築 ───────────────────────────────────────────────────────────

def build_nodes():
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    nodes.append(p("YouTubeに新しい動画をアップしました！！"))
    nodes.append(sp())
    nodes.append(p("今回登場してくれたのは、私の友人です。"))
    nodes.append(sp())
    nodes.append(p("彼女はお見合い形式の婚活サービスを使っていたんですが、そのサービス、お見合いをセッティングしてくれるだけで、あとのサポートはほぼなかったんですよね。"))
    nodes.append(sp())
    nodes.append(p("仲人もいない。アドバイスをしてくれる人もいない。"))
    nodes.append(sp())
    nodes.append(p("それでも彼女は諦めなかった。"))
    nodes.append(sp())
    nodes.append(p("自分で動いた。"))
    nodes.append(sp())
    nodes.append(p("参考にしたのが、IBJの代表・石坂茂さんが書かれた「プロの仲人が伝授！90日後にプロポーズされる賢い婚活」という本です（あすなる愛媛もIBJに加盟しています）。"))
    nodes.append(sp())
    nodes.append(p("その本を読みながら、彼の気持ちを理解して、関係を丁寧に育てて、最後は自分から彼の背中をそっと押した。"))
    nodes.append(sp())
    nodes.append(p("3年の婚活を経て、ご成婚。"))
    nodes.append(sp())
    nodes.append(p("動画の中で彼女が話してくれる「好きから始まらなくていい」という言葉、すごくリアルで、すごく温かくて、私も聞きながら胸がじーんとしました。"))
    nodes.append(sp())
    nodes.append(p("「ピンとこなくても進んでいいの？」「好きじゃないのに失礼じゃないかな」って悩んだことがある方、ぜひこの動画を見てほしいんです。"))
    nodes.append(sp())
    nodes.append(p("サポートなしでここまでやり遂げた彼女の話、きっと何かを届けてくれると思います。"))
    nodes.append(sp())
    nodes.append(p("▶️ https://youtu.be/sGzxBsIr2ho"))
    nodes.append(sp())
    nodes.append(p("ちなみに彼女が読んでいた石坂さんの本、あすなる愛媛ではこういう知識を仲人が直接お伝えしながら一緒に婚活を進めていきます。"))
    nodes.append(sp())
    nodes.append(p("「一人で頑張るのはしんどいな」と思っている方は、ぜひ無料相談に来てください。"))

    # CTA
    nodes.append(sp())
    nodes.append(p("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan"))

    return nodes


# ── 画像生成 → Wixインポート ───────────────────────────────────────────────────

def generate_and_import(prompt_text, filename):
    print(f"  DALL-E 3 生成中: {filename}")
    resp = client.images.generate(
        model="dall-e-3",
        prompt=prompt_text,
        size="1792x1024",
        quality="standard",
        n=1,
    )
    dall_e_url = resp.data[0].url
    print(f"  生成完了。Wixにインポート中...")

    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/import",
        headers=wix_headers(),
        json={"url": dall_e_url, "displayName": filename, "mimeType": "image/png"},
        timeout=30,
    )
    if not r.ok:
        print(f"  インポート失敗: {r.status_code} {r.text[:200]}")
        return None

    data = r.json()
    file_id = (data.get("file") or {}).get("id") or data.get("fileId")
    if not file_id:
        return None

    for i in range(20):
        time.sleep(3)
        chk = requests.get(f"{WIX_BASE}/site-media/v1/files/{file_id}",
                           headers=wix_headers(), timeout=15)
        if chk.ok:
            fd = chk.json().get("file", {})
            if fd.get("state") in ("READY", "OK"):
                url = fd.get("url", "")
                m = re.search(r"/media/([^?#\s]+)", url)
                print(f"  インポート完了: {url[:60]}...")
                return {"url": url, "id": m.group(1) if m else file_id,
                        "height": 1024, "width": 1792, "filename": filename}
            print(f"  待機中... ({fd.get('state')}, {i+1}/20)")
    print("  タイムアウト")
    return None


# ── メイン ────────────────────────────────────────────────────────────────────

def main():
    today = "2026-04-28"
    title = "動画アップしました！サポートなしで婚活した友人の、リアルすぎる体験談。"

    eyecatch_prompt = (
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A Japanese woman sitting at a cozy cafe table, smiling warmly while talking and sharing her story, "
        "a book and a cup of tea on the table, East Asian appearance, black hair, relaxed and confident mood, "
        "soft window light."
    )

    print("\n[1/3] アイキャッチ画像を生成中...")
    img1 = generate_and_import(eyecatch_prompt, f"{today}_video_eyecatch.png")

    print("\n[2/3] richContentを構築してWixに下書き投稿中...")
    nodes = build_nodes()

    draft_post = {
        "title":       title,
        "memberId":    MEMBER_ID,
        "richContent": {"nodes": nodes},
        "categoryIds": [CATEGORY_ID],
    }

    if img1:
        m = re.search(r"/media/([^?#\s]+)", img1["url"])
        draft_post["media"] = {
            "custom": True,
            "wixMedia": {"image": {
                "id":       m.group(1) if m else img1["id"],
                "url":      img1["url"],
                "height":   img1["height"],
                "width":    img1["width"],
                "filename": img1["filename"],
            }},
        }

    resp = requests.post(
        f"{WIX_BASE}/blog/v3/draft-posts",
        headers=wix_headers(),
        json={"draftPost": draft_post},
        timeout=30,
    )

    if not resp.ok:
        print(f"Wix投稿失敗: {resp.status_code}\n{resp.text[:500]}")
        return

    draft_id = resp.json().get("draftPost", {}).get("id")
    print(f"\n[3/3] 完了！")
    print(f"  Wix下書きID: {draft_id}")
    print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")
    return draft_id


if __name__ == "__main__":
    main()
