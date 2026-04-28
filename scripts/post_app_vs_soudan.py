#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
アプリvs結婚相談所 比較記事 - Wix投稿スクリプト
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
CATEGORY_ID = "641187e4-a409-4c2f-9639-ecc548f26f15"  # 無料相談の前に読む

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

def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}

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

def h(text, level=2):
    return {"type": "HEADING", "id": nid(),
            "nodes": [{"type": "TEXT", "id": nid(), "nodes": [],
                        "textData": {"text": text, "decorations": []}}],
            "headingData": {"level": level}}

def heading_block(text, level=2):
    return [sp(), divider_node(), sp(), h(text, level)]

def img_node(file_info, caption=""):
    url = file_info["url"]
    m = re.search(r"/media/([^?#\s]+)", url)
    wix_uri = f"wix:image://v1/{m.group(1)}/img.png" if m else url
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": wix_uri}}, "caption": caption}}


# ── richContent 構築 ───────────────────────────────────────────────────────────

def build_nodes(img2=None, img3=None):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # イントロ
    nodes.append(p("「結婚相談所って高いでしょ。アプリで十分じゃないの？」"))
    nodes.append(sp())
    nodes.append(p("よく聞かれます。そして正直に言うと——その質問への答え、「場合による」んですよね。"))
    nodes.append(sp())
    nodes.append(p("アプリが合う人もいるし、結婚相談所が合う人もいる。どちらが正解というわけじゃない。"))
    nodes.append(sp())
    nodes.append(p("でも「アプリは安い」「結婚相談所は高い」というイメージ、実はかなり表面的な話で、もう少し深く比べると見え方が変わってきます。"))
    nodes.append(sp())
    nodes.append(p("今日は結婚相談所の仲人という立場を一度置いといて（笑）、できるだけフラットにデータを並べてみます。"))

    # Section 1: コスト比較
    nodes.extend(heading_block("まずお金の話から正直に"))

    nodes.extend(heading_block("マッチングアプリにかかるリアルな費用", level=3))
    nodes.append(p("主要アプリ（ペアーズ・Omiai・withなど）の男性月額は3,000〜5,000円が相場です。"))
    nodes.append(sp())
    nodes.append(p("ただこれ、「基本料金」の話なんですよね。いいねの追加購入、メッセージ機能の課金、ブースト機能……アプリによっては基本料金以外の課金要素がついていて、気づいたら月1万円近くになっていた、という声はよく聞きます。"))
    nodes.append(sp())
    nodes.append(p("そしてもう一つ、男性に多いのが「複数アプリの掛け持ち」です。1つのアプリに出会いが限られると感じると、2つ・3つと広げていく。そうなると月2〜3万円。6ヶ月続けると15〜20万円になる計算です。"))
    nodes.append(sp())
    nodes.append(p("女性は多くのアプリで無料〜低価格ですが、失っているのは「時間」です。あるアプリ調査によると、利用者の9割が「マッチングアプリ疲れ」を経験していて、メッセージに月平均18時間を費やし、平均利用期間6.4ヶ月で合計約115時間という数字も出ています（バチェラーデート社調査）。"))

    # 画像2
    if img2:
        nodes.append(sp())
        nodes.append(img_node(img2, "マッチングアプリの隠れたコスト"))
        nodes.append(sp())

    nodes.extend(heading_block("結婚相談所にかかる費用", level=3))
    nodes.append(p("入会金・月会費・成婚料の合計で、相談所によりますが30〜100万円の範囲が多いです。高く見えますが、サポート込み・身元確認済み・相手も全員結婚前提、という条件がついてきます。"))

    # Section 2: 成婚率
    nodes.extend(heading_block("成婚率を比べると"))
    nodes.append(p("ペアーズの成婚率は約2.2%という分析があります。一方、結婚相談所の成婚率は20〜30代で約26%というデータもあります（IBJ調べ）。"))
    nodes.append(sp())
    nodes.append(p("ただしこの数字、単純に比較できないところもあって——アプリは「結婚じゃなくて恋人が欲しい人」も入っているし、結婚相談所は「結婚前提の人だけ」が入っています。そもそも母集団が違う。数字の読み方には注意が必要です。"))
    nodes.append(sp())
    nodes.append(p("それでも「真剣に結婚を考えている人同士が集まっている確率」は、結婚相談所のほうが圧倒的に高いのは事実です。"))

    # 画像3
    if img3:
        nodes.append(sp())
        nodes.append(img_node(img3, "アプリと結婚相談所、それぞれの出会い"))
        nodes.append(sp())

    # Section 3: メリット・デメリット
    nodes.extend(heading_block("それぞれのメリット・デメリット"))

    nodes.extend(heading_block("マッチングアプリ", level=3))
    nodes.append(p("よいところは、気軽に始められて自分のペースで進められること。相手の数が多いのも魅力ですし、アプリ内で相性を確かめながらゆっくり距離を縮めていけます。「まだ結婚かどうかわからないけど、まず誰かと出会いたい」という段階の方には向いています。"))
    nodes.append(sp())
    nodes.append(p("難しいところは、相手の本気度がわからないこと。身元確認が甘いアプリも多く、プロフィール写真と実物が違った、途中で連絡が来なくなった、という経験をした方も少なくないです。全部自分でやる必要があるので、うまくいかないとき「何が問題なのか」が見えにくいのも、じわじわ消耗するポイントです。"))

    nodes.extend(heading_block("結婚相談所", level=3))
    nodes.append(p("よいところは、全員が独身証明・収入証明など身元確認済みで、結婚を前提に会っていること。うまくいかないときに相談できる仲人がいること。感情的になっているとき、一歩引いた視点でアドバイスしてもらえる存在がいるのは、思ったより心強いです。"))
    nodes.append(sp())
    nodes.append(p("難しいところは、費用が高いこと。そして「結婚相談所に入る」という心理的なハードルです。「自分がそこに入るのか」という気持ち、すごくよくわかります。アプリのような「何万人からフリーに選ぶ」感覚はないので、自由度が狭く感じる方もいます。"))

    # Section 4: まとめ
    nodes.extend(heading_block("結局、どっちが向いているの？"))
    nodes.append(p("こう整理するとわかりやすいかもしれません。"))
    nodes.append(sp())
    nodes.append(p("アプリが向いているのは、出会いの数を広くとりたい・まだ結婚を決めていない・自分でガンガン動ける・費用をとにかく抑えたい、という方です。"))
    nodes.append(sp())
    nodes.append(p("結婚相談所が向いているのは、真剣に結婚を考えている・忙しくて効率よく動きたい・一人で進めるのが不安・「なんかいつもうまくいかない」という繰り返しパターンを変えたい、という方です。"))
    nodes.append(sp())
    nodes.append(p("どちらも「出会いのための手段」です。大事なのは手段じゃなくて、「その先にどんな関係を築くか」ですよね。"))
    nodes.append(sp())
    nodes.append(p("もしどちらにしようか迷っている方がいたら、ぜひ一度無料相談に来てください。あなたの状況を聞いた上で、正直にどちらが向いていそうか一緒に考えます——「うちに入ってください」じゃなくて、本当に（笑）。"))

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
    today = "2026-04-29"
    title = "マッチングアプリvs結婚相談所、本当のコストを正直に比べてみました。"

    image_prompts = [
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A split scene: on the left, a person swiping on a smartphone alone at night; "
         "on the right, a warm consultation scene with two people talking at a cozy desk. "
         "Balanced and neutral mood, East Asian appearance, black hair, soft lighting."),
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese man looking thoughtfully at multiple smartphone screens showing different apps, "
         "with subtle cost/money icons floating around, East Asian appearance, black hair, "
         "slightly overwhelmed but curious expression, soft blue and warm tones."),
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "Two paths illustrated side by side: one showing a person navigating many online profiles alone, "
         "another showing a couple meeting warmly with a supportive counselor present. "
         "Both paths look positive and valid, East Asian appearance, black hair, hopeful mood."),
    ]

    print("\n[1/3] 画像を生成中...")
    img1 = generate_and_import(image_prompts[0], f"{today}_app_vs_soudan_eyecatch.png")
    img2 = generate_and_import(image_prompts[1], f"{today}_app_vs_soudan_img2.png")
    img3 = generate_and_import(image_prompts[2], f"{today}_app_vs_soudan_img3.png")

    print("\n[2/3] richContentを構築してWixに下書き投稿中...")
    nodes = build_nodes(img2=img2, img3=img3)

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
        return None

    draft_id = resp.json().get("draftPost", {}).get("id")
    print(f"\n[3/3] 完了！")
    print(f"  Wix下書きID: {draft_id}")
    print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")
    return draft_id


if __name__ == "__main__":
    main()
