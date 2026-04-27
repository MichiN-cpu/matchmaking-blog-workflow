#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本当の意味で優しい男性の見極め方 - Wix投稿スクリプト
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
CATEGORY_ID = "3f5f378d-a4f4-47e0-90a7-ab4daa27504e"  # 仮交際

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
    nodes.append(p("「優しい人がいい」って、婚活中の女性にいちばんよく聞くご希望なんですよね。"))
    nodes.append(sp())
    nodes.append(p("そりゃそうですよね。パートナーには、自分のことを大切にしてほしい。それは誰もが自然に求めることだと思います。"))
    nodes.append(sp())
    nodes.append(p("でね、実はここに一つ、大事な落とし穴があって。"))
    nodes.append(sp())
    nodes.append(p("「優しい」に見えるけれど、じつは優しくない——そんな男性が、意外と多いんですよ。"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("出会った最初のころはとても紳士的だったのに、関係が深まると話を流されるようになった。"))
    nodes.append(p("自分には優しいのに、飲食店の店員さんへの言葉遣いが少し気になる。"))
    nodes.append(p("なぜかいつも自分が謝ってばかりで、相手の不機嫌に振り回されている気がする。"))
    nodes.append(sp())
    nodes.append(p("——一つでも「あるかも」と思ったなら、今日の話をぜひ読んでほしいんです。"))
    nodes.append(sp())
    nodes.append(p("本当の意味で優しい男性を見極めるには、「どこを見るか」がとても大切です。"))

    # Section 1
    nodes.extend(heading_block("「愛想の良さ」と「本物の優しさ」は似て非なるもの"))
    nodes.append(p("社会学者のアーヴィング・ゴッフマンは、人間には「表の顔（front stage）」と「裏の顔（back stage）」があると言いました。"))
    nodes.append(sp())
    nodes.append(p("初対面や気を遣う相手の前では、誰だって良い顔をするものです。それ自体は悪いことじゃない。"))
    nodes.append(sp())
    nodes.append(p("問題は、その「表の顔」だけを見て判断してしまうことなんですよね。"))
    nodes.append(sp())
    nodes.append(p("愛想の良さと優しさは、まったく別物です。愛想は「相手に良く見られたい」という印象管理から生まれますが、本物の優しさはもっと深いところ——相手のことを本当に気にかけている、という内側の姿勢から来ています。"))

    # 画像2
    if img2:
        nodes.append(sp())
        nodes.append(img_node(img2, "本物の優しさを見極めるポイント"))
        nodes.append(sp())

    # Section 2
    nodes.extend(heading_block("本当に優しい人が見せる、3つのサイン"))
    nodes.append(p("心理学では「愛着スタイル（attachment style）」という概念があります。幼少期に築いた人との絆のパターンが、大人になっても人間関係に影響し続けるというものなんです。"))
    nodes.append(sp())
    nodes.append(p("安定した愛着スタイルを持つ人には、ちょっとした言動にそれが表れます。"))

    nodes.extend(heading_block("サイン① 「不機嫌」を武器にしない", level=3))
    nodes.append(p("怒ったり困ったりしたとき、黙り込んで相手に「何がいけなかったの？」と探らせる——これ、よくある関係の罠なんですよね。"))
    nodes.append(sp())
    nodes.append(p("本当に優しい人は、感情があっても、それを相手をコントロールするために使いません。「今ちょっと整理したい」と言語化できるか、もしくは少し時間を置いてちゃんと話し合えるか。そこをぜひ見てみてください。"))

    nodes.extend(heading_block("サイン② あなた以外への態度が温かい", level=3))
    nodes.append(p("「自分にだけ優しい」は要注意です。"))
    nodes.append(sp())
    nodes.append(p("神経科学の研究では、他者への共感は脳の前帯状皮質や島皮質と関係していて、特定の人への演技で選択的にオンにできるものではありません。飲食店の店員さん、通りすがりの人、自分より立場の弱い人への言葉遣いや態度に、その人の本性が出ます。"))

    nodes.extend(heading_block("サイン③ 「自分が損をする場面」でも思いやれる", level=3))
    nodes.append(p("優しさの本当のテストは、コストがかかるときです。"))
    nodes.append(sp())
    nodes.append(p("疲れているとき、自分のことで精一杯なとき、それでもあなたのことを気にかけてくれるか。これが「本物かどうか」のリトマス試験紙だと私は思っています。"))

    # Section 3
    nodes.extend(heading_block("見極めるには「時間」と「場面の多様性」が必要"))
    nodes.append(p("コミュニケーション学では「文脈（context）」の重要性がよく語られます。人の優しさも、一つの場面だけでは判断できない。"))
    nodes.append(sp())
    nodes.append(p("デートのときだけ、二人きりのときだけ——そこから場面を広げて、さらに「ストレスがかかっている状況」を見ることが大切なんです。"))
    nodes.append(sp())
    nodes.append(p("たとえば、計画が狂ったとき。待ち合わせに少し遅れてしまったとき。予約が取れなかったとき。"))
    nodes.append(sp())
    nodes.append(p("そういう「小さな逆境」に、どう振る舞うか。焦るか、柔軟に対応できるか。そこにその人の「地」が出ます。"))
    nodes.append(sp())
    nodes.append(p("かつての私もね、「優しそう！」という第一印象だけで判断してしまって、後から「あれ、なんか違う…」となった経験があります（笑）。それからは、焦らずじっくり見るようにしました。"))

    # Section 4
    nodes.extend(heading_block("いろんなデートをしてみてください"))
    nodes.append(p("食事やカフェだけが「デート」じゃないんですよね、ということをぜひ意識してほしいんです。"))
    nodes.append(sp())
    nodes.append(p("たとえば、大勢の人が出入りするイベント。屋内でも屋外でも。体を動かすアクティビティ。頭を使うゲームや体験系のもの。ちょっと奮発した高級なお店。逆にカジュアルで安くて気取らないお店。"))
    nodes.append(sp())
    nodes.append(p("場面を変えると、お互いの「素」が出てきます。"))
    nodes.append(sp())
    nodes.append(p("そうそう、意識してほしいのは「想定外をわざと作ること」です。"))
    nodes.append(sp())
    nodes.append(p("あなたが少しビビるような場所、普段やり慣れていないこと、どちらにとっても初めての体験——そういう場を一緒に過ごしてみてほしいんです。"))
    nodes.append(sp())
    nodes.append(p("そこで何が起きるか、というより、そのとき相手がどう動くか。"))
    nodes.append(sp())
    nodes.append(p("困ったとき、一緒に解決策を考えてくれるか。あなたが不安そうにしているとき、さりげなく背中を押してくれるか。逆に、相手が困っていたとき、あなたは自然に手を差し伸べられるか。"))
    nodes.append(sp())
    nodes.append(p("これって、恋愛心理学で「共同対処（co-regulation）」と呼ばれる関係の質に直結します。二人で一緒に感情やストレスを調整し合える関係は、長期的なパートナーシップの基盤になると言われているんですよ。"))
    nodes.append(sp())
    nodes.append(p("おすましした「良い子ちゃんデート」だけを重ねていると、表の顔しか見えない。でも、うまくいかない場面、想定外の出来事、ちょっとした困りごとを一緒に経験することで、その人の本質がはじめて見えてくる。"))
    nodes.append(sp())
    nodes.append(p("人生って、うまくいくことばかりじゃないじゃないですか。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、デートをプチ人生体験の場にしてみてほしいんです。一緒にドキドキして、一緒に笑って、一緒に「どうしよう」って言い合えるような相手——そういう人と歩む未来が、きっと豊かだと思います♬"))

    # 画像3
    if img3:
        nodes.append(sp())
        nodes.append(img_node(img3, "いろんなデートで相手の本質を見極める"))
        nodes.append(sp())

    # Section 5
    nodes.extend(heading_block("優しさは「言葉」より「行動の一貫性」にある"))
    nodes.append(p("オキシトシンというホルモンをご存知ですか。「愛情ホルモン」「絆のホルモン」とも呼ばれていて、信頼関係が深まるほど分泌されます。"))
    nodes.append(sp())
    nodes.append(p("でね、このオキシトシンって、一度きりの良いできごとより、“繰り返し積み重なった安心感”によって育まれるんですよ。"))
    nodes.append(sp())
    nodes.append(p("「好き」とか「大事にしたい」とか、言葉はいくらでも言える。でも、一度言ったことを何度も行動で示してくれるか——それが積み重なったとき、はじめて「本当に優しい人」と言えるんだと思います。"))
    nodes.append(sp())
    nodes.append(p("婚活中に「この人、優しそう」と感じた相手、ぜひ今日の3つのサインを思い出してみてください。"))
    nodes.append(sp())
    nodes.append(p("焦らず、場面を変えて、時間をかけて。"))
    nodes.append(sp())
    nodes.append(p("そうやって育んだ関係の中にこそ、本物のやさしさが育つ——そう信じています。"))

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
        print(f"  file_id取得失敗: {data}")
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
    today = "2026-04-27"
    title = "本当の意味で優しい男性の見極め方"

    image_prompts = [
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese couple walking together at an outdoor festival among a cheerful crowd, the man "
         "gently guiding the woman, East Asian appearance, black hair, warm smiles, casual elegant clothing."),
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese couple facing an unexpected situation together — a closed restaurant sign — "
         "the man smiling reassuringly and pointing at a new direction, East Asian appearance, black hair, "
         "cozy street background."),
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese couple laughing and helping each other during a fun outdoor activity, hiking or "
         "a park adventure, East Asian appearance, black hair, warm energetic mood, nature background."),
    ]

    print("\n[1/3] 画像を生成中...")
    img1 = generate_and_import(image_prompts[0], f"{today}_eyecatch.png")
    img2 = generate_and_import(image_prompts[1], f"{today}_img2.png")
    img3 = generate_and_import(image_prompts[2], f"{today}_img3.png")

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
        return

    draft_id = resp.json().get("draftPost", {}).get("id")
    print(f"\n[3/3] 完了！")
    print(f"  Wix下書きID: {draft_id}")
    print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")


if __name__ == "__main__":
    main()
