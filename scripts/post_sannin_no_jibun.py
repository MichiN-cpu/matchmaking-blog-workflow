#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
夫婦の中に「3人の自分」がいる - Wix投稿スクリプト
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
CATEGORY_ID = "5414dab5-ded7-4b15-a88a-d679d6fd3c71"  # 真剣交際

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
    nodes.append(p("結婚って、交際期間とはまったくちがうんですよね。"))
    nodes.append(sp())
    nodes.append(p("一緒に住んで、毎日顔を合わせて、仕事も家事も人生の大きな決断も——全部ふたりで関わっていく。友人関係や職場とも違う、もっとずっと長くて、もっとずっと深い関係性なんです。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、交際中には見えなかったものが出てくる。"))
    nodes.append(sp())
    nodes.append(p("「え、こういう人だったの？」という驚きもあるし、「自分がこんな反応するとは思わなかった」という戸惑いも。もちろん、「こんな素敵な面があったんだ！」という喜びも、どんどん出てきます。"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("これまでの恋愛で、相手が思っていたより頑固で「こんなはずじゃなかった」と思ったことがある。"))
    nodes.append(p("好きな人といると、自分がこんなに甘えん坊になるとは思っていなかった。"))
    nodes.append(p("恋人とふたりでいると、なぜかテンションが子どもみたいになる。"))
    nodes.append(sp())
    nodes.append(p("——あるある、って思った方、それはまったく当たり前のことなんですよ。びっくりしなくて大丈夫。"))

    # Section 1
    nodes.extend(heading_block("一人の人間の中には、3人いる"))
    nodes.append(p("心理士エリック・バーンが提唱した「交流分析（TA）」という理論に、「PAC理論」というものがあります。人は誰でも、3つの心の状態を持っているという考え方です。"))
    nodes.append(sp())
    nodes.append(p("中嶋流にわかりやすく言うと——"))

    nodes.extend(heading_block("父性・男性性・行動・リーダーシップの自分", level=3))
    nodes.append(p("決める、引っ張る、守る、進める。物事を前に動かしていくエネルギーです。計画を立てて実行する、困難に立ち向かう、頼もしい存在であろうとする——そういう力の源。"))

    nodes.extend(heading_block("母性・女性性・欲求・感情・共感の自分", level=3))
    nodes.append(p("感じる、受け取る、つながる、癒す。人の痛みに寄り添えるのも、自分の感情と向き合えるのも、このエネルギーが動いているから。「もっとこうしたい」という欲求や願いも、ここから生まれます。"))

    nodes.extend(heading_block("子供・創造性・ユーモア・遊び心の自分", level=3))
    nodes.append(p("楽しむ、笑う、好奇心でわくわくする。アイデアが湧いてくるのも、突然おかしなことを言いたくなるのも、この子のしわざです（笑）。"))

    nodes.append(sp())
    nodes.append(p("この3人は、男性にも女性にも、全員の中にいます。"))
    nodes.append(sp())
    nodes.append(p("でね、面白いのが、仕事のときは「リーダーシップの自分」が前に出てたり、友人とのランチでは「遊び心の子供」が大はしゃぎしてたり——自然と使い分けているんですよね。"))
    nodes.append(sp())
    nodes.append(p("「キャラ変え」って言うじゃないですか。あれは嘘をついているわけじゃなくて、自分の中のいろんな自分が場面に応じて出てきているだけなんです。"))

    # 画像2
    if img2:
        nodes.append(sp())
        nodes.append(img_node(img2, "自分の中の3つのキャラクター"))
        nodes.append(sp())

    # Section 2
    nodes.extend(heading_block("3人に名前をつけてあげてほしい"))
    nodes.append(p("ここで一つ、提案があります。"))
    nodes.append(sp())
    nodes.append(p("あなたの中の3人に、それぞれ名前をつけてあげてほしいんです。"))
    nodes.append(sp())
    nodes.append(p("たとえばリーダーシップの自分には「所長」とか「キャプテン」。感情・共感の自分には「みっちゃん」とか「お母さん」。遊び心の自分には「ちびちゃん」とか「わちゃわちゃ係」（笑）。"))
    nodes.append(sp())
    nodes.append(p("名前をつけると、ちょっと不思議なことが起きます。"))
    nodes.append(sp())
    nodes.append(p("自分の中の感情や反応に、気づきやすくなるんですよ。「あ、今ちびちゃんが拗ねてる」「今は所長モードになりすぎてる」って、すこし距離を置いて自分を見られるようになる。"))
    nodes.append(sp())
    nodes.append(p('これは心理療法の一つ「Internal Family Systems（IFS）」でも使われる考え方で、内なる“部分”に名前と役割を与えることで自己理解が深まり、感情の暴走が穏やかになると言われています。'))
    nodes.append(sp())
    nodes.append(p('実はこれ、NLP（神経言語プログラミング）にも「パート（Part）」という同じような概念があります。人の内側には複数の“パート”が存在していて、それぞれが違う意図や欲求を持って動いている——という考え方です。NLPではパート同士が対立しているとき（たとえば「頑張りたいけど休みたい」という葛藤）に、パートに語りかけて統合していくアプローチをとります。名前をつけて対話する、というのは世界中の心理的アプローチが共通して持っている知恵なんですよ。'))

    # Section 3
    nodes.extend(heading_block("相手の3人も、ちゃんと見てあげてほしい"))
    nodes.append(p("そして、パートナーの3人も同じように慈しんでほしいんです。"))
    nodes.append(sp())
    nodes.append(p("「夫だから」「妻だから」という1つのフレームで相手を見ていると、そのフレームに合わない部分が出てきたとき、「え？なんで？」ってなりやすい。"))
    nodes.append(sp())
    nodes.append(p("でも「この人の中にも3人いるんだ」と思って見ると、「あ、今日は遊び心の子供が出てるんだな」「ちょっと疲れてリーダーシップが空回りしてる日なんだな」って、ちゃんと受け取れるようになります。"))
    nodes.append(sp())
    nodes.append(p("社会学者のゴッフマンは、人は場面ごとに異なる「役割」を演じながら生きていると言いました。それは嘘でも演技でもなく、人間として自然な姿。夫婦という関係の中でも、固定した「夫キャラ」「妻キャラ」だけでいようとすると、どこかで苦しくなってくるんですよ。"))

    # 画像3
    if img3:
        nodes.append(sp())
        nodes.append(img_node(img3, "ふたりで夢を実現していく"))
        nodes.append(sp())

    # Section 4
    nodes.extend(heading_block("多様な自分を見せ合えるふたりに"))
    nodes.append(p("人生のステージは変わります。子育て、介護、仕事の変化、体の変化——そのたびに、ふたりに求められる役割もエネルギーも変わっていく。"))
    nodes.append(sp())
    nodes.append(p("そのとき、「リーダーシップの自分」だけでいようとしたら疲れ果ててしまう。「感情・共感の自分」だけを出し続けたら消耗してしまう。"))
    nodes.append(sp())
    nodes.append(p("3人がいるから、バランスがとれる。"))
    nodes.append(sp())
    nodes.append(p("疲れたら遊び心の自分に戻っておどけて、大切な決断には父性・母性が力を出して、関係が冷えそうなときは感情と共感でまたつながって——そういう柔軟さが、長く豊かに生きるエネルギーになります。"))
    nodes.append(sp())
    nodes.append(p("そしてね、これはひとりでやるより、ふたりでやると何倍も面白いんですよ。"))
    nodes.append(sp())
    nodes.append(p("「今、キャプテンが出てきてるね」「あ、今わちゃわちゃ係だ（笑）」——お互いの中のキャラの名前を呼び合えるようになると、ちょっとした行き違いが笑いに変わったり、「今は所長に任せて」って自然に役割を手渡せたりします。"))
    nodes.append(sp())
    nodes.append(p("困ったことが起きたとき、「今どの自分が出てる？」「相手の中の誰が話してる？」って意識するだけで、ケンカの出口が見つかりやすくなる。"))
    nodes.append(sp())
    nodes.append(p("そしてふたりの夢を語るとき、遊び心の子供がアイデアを出して、リーダーシップがそれを形にして、感情・共感が「それ、すごくいい！」って温める——そんなふうに、6人がチームになって夢を実現していけるんです。"))
    nodes.append(sp())
    nodes.append(p("パートナーに、多様な自分を見せてあげてください。そして相手の多様さも、面白がって受け取ってほしい。"))
    nodes.append(sp())
    nodes.append(p("「こんな自分もいるんだよ」って、笑いながら話せる関係が、一番あたたかい家庭だと私は思っています♬"))

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
    today = "2026-04-28"
    title = "夫婦の中に「3人の自分」がいる。それを知るだけで、関係がやわらかくなる。"

    image_prompts = [
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese couple sitting together warmly, each showing a different emotional facet — "
         "one playful, one nurturing — surrounded by soft light, East Asian appearance, black hair, "
         "cozy indoor setting, gentle and harmonious mood."),
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese person with three soft glowing auras around them representing different inner selves — "
         "a strong leader figure, a warm nurturing figure, and a playful childlike figure, "
         "East Asian appearance, black hair, dreamlike pastel background."),
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese couple laughing and pointing at a shared vision board or map of dreams together, "
         "teamwork and joy, East Asian appearance, black hair, warm energetic colors, hopeful mood."),
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
    print(f"\n  Wix下書きID: {draft_id}")
    return draft_id


if __name__ == "__main__":
    main()
