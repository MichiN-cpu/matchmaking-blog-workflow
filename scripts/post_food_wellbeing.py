#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食事とウェルビーイング・関係性 - Wix投稿スクリプト
"""

import os, re, time, uuid, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_ID = "3f5f378d-a4f4-47e0-90a7-ab4daa27504e"  # 仮交際

client = OpenAI(api_key=OPENAI_KEY)

def wix_headers():
    return {"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID, "Content-Type": "application/json"}

def nid(): return str(uuid.uuid4())[:8]

def sp():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}
    ], "paragraphData": {}}

def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"}}

def make_text_nodes(text):
    result, pos = [], 0
    for m in re.compile(r'https?://\S+').finditer(text):
        if m.start() > pos:
            result.append({"type": "TEXT", "id": nid(), "nodes": [],
                           "textData": {"text": text[pos:m.start()], "decorations": []}})
        result.append({"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": m.group(0), "decorations": [
                           {"type": "LINK", "linkData": {"link": {"url": m.group(0), "target": "BLANK"}}}]}})
        pos = m.end()
    if pos < len(text):
        result.append({"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": text[pos:], "decorations": []}})
    return result or [{"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}]

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

def build_nodes(img2=None, img3=None):
    n = []

    # 冒頭挨拶
    n.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    n.append(sp())
    n.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    n.append(sp())

    # イントロ
    n.append(p("先日の記事で、友人の「結婚後に食事が丁寧になった」という話を書きました。"))
    n.append(sp())
    n.append(p("国産食材を選ぶようになった。野菜が増えた。食卓を一緒に囲む喜びを知った——そんな変化の話だったんですが、実はこれ、科学的にもものすごく理にかなっていたんですよ。"))
    n.append(sp())
    n.append(p("でね、今回はその「食事と関係性の科学」をテーマに動画を作りました！"))
    n.append(sp())
    n.append(p("▼動画はこちらからご覧ください（下に埋め込んでいます）"))
    n.append(sp())
    n.append(p("今日は動画の内容を少しだけ先取りしてお届けします。"))

    # Section 1
    n.extend(heading_block("野菜を食べると、「魅力」が上がる"))
    n.append(p("まず、これを知ってほしいんですよ。"))
    n.append(sp())
    n.append(p("野菜や果物をちゃんと食べている人は、幸福度が上がるだけじゃなくて、好奇心や創造性まで高まるという研究結果があるんです（Głąbska et al., 2020）。"))
    n.append(sp())
    n.append(p("好奇心旺盛で、話が面白くて、なんか生き生きしている人——それって、婚活でもパートナーシップでも、一緒にいたくなる人の特徴ですよね。"))
    n.append(sp())
    n.append(p("「魅力的になりたい」と思ったとき、ファッションや話術を磨くのもいいけれど、毎日の野菜を1皿増やすことも、意外と直結しているんですよ。"))

    if img2:
        n.append(sp())
        n.append(img_node(img2, "野菜・果物と気持ちの関係"))
        n.append(sp())

    # Section 2
    n.extend(heading_block("「イライラ」は性格じゃなくて、血糖値かもしれない"))
    n.append(p("これ、特に大事な話なので聞いてほしいんです。"))
    n.append(sp())
    n.append(p("甘いものや白いご飯を食べた後に血糖値が急上昇して、その後急降下する——いわゆる「血糖値スパイク」の状態になると、脳の前頭前野（自分を落ち着かせる部分）の機能が落ちて、イライラしやすく、怒りっぽくなるんですよ。"))
    n.append(sp())
    n.append(p("「なんか最近、彼（彼女）と些細なことでぶつかる」という場合、もしかしたらランチに砂糖たっぷりのものを食べていたせいかもしれないんです（笑）。"))
    n.append(sp())
    n.append(p("血糖値を安定させる食事（ベジファースト・低GI食品・欠食しない）は、パートナーとの不必要な衝突を防ぐ関係性の戦略でもあります。"))

    # Section 3
    n.extend(heading_block("コーヒーはブラックで。エナジードリンクはやめて。"))
    n.append(p("少し驚いた話もご紹介します。"))
    n.append(sp())
    n.append(p("日本人を対象とした大規模調査（JPHC-NEXT）によると、ブラックコーヒーを飲む人はうつ病リスクが約1.7%低いという結果が出ています。カフェインの抗炎症・抗酸化作用が脳を守ってくれているようです。"))
    n.append(sp())
    n.append(p("一方で、砂糖入りコーヒーはうつ病リスクを上昇させ、エナジードリンクは月1杯でもメンタルに良くない影響が出るというデータも。"))
    n.append(sp())
    n.append(p("同じカフェインでも、糖分が入るだけでこんなに違う。「甘い缶コーヒーが習慣」という方、ちょっと見直してみると気持ちが変わるかもしれませんよ。"))

    if img3:
        n.append(sp())
        n.append(img_node(img3, "飲み物の選び方とメンタルヘルス"))
        n.append(sp())

    # Section 4
    n.extend(heading_block("一緒に食べることが、関係性をつくる"))
    n.append(p("カナダの大規模研究では、大切な人と食事を共にする頻度が高い人ほど、相手への思いやり（向社会的行動）が増えるという結果が出ています。"))
    n.append(sp())
    n.append(p("「食卓を囲む」って、ただご飯を食べることじゃないんですよね。目を合わせて、今日の話をして、「おいしいね」って言い合う——その積み重ねが、関係性の土台をつくっていく。"))
    n.append(sp())
    n.append(p("友人が「彼と一緒に食卓を囲むようになってから変わった」と言っていた理由が、これで腑に落ちた気がしました。"))

    # Section 5
    n.extend(heading_block("女性の方にとくに知ってほしいこと"))
    n.append(p("日本人女性の多くが「隠れ貧血（フェリチン値不足）」の状態にあると言われています。"))
    n.append(sp())
    n.append(p("そしてこの隠れ貧血、憂鬱感・集中力の低下・疲れやすさと深く関係しているんです。"))
    n.append(sp())
    n.append(p("「なんか気持ちが上がらない」「やる気が出ない」——そういうとき、性格や環境のせいだと思いがちですが、実は鉄分不足が原因かもしれない。赤身肉・レバー・貝類などを意識的に摂ること、あるいは一度フェリチン値を調べてみることをおすすめします。"))
    n.append(sp())
    n.append(p("そしてパートナーの男性に知ってほしいのは——彼女の「なんかしんどい」は、性格や気持ちの問題じゃなくて、栄養学的な課題である可能性があるということ。一緒に食事を考えてあげられる男性は、それだけで頼もしいです。"))

    # Section 6
    n.extend(heading_block("幸せホルモンは、食べ物からつくられる"))
    n.append(p("最後にこれ。"))
    n.append(sp())
    n.append(p("精神安定のセロトニンは、バナナ・大豆・牛乳に含まれるトリプトファンからつくられます。"))
    n.append(sp())
    n.append(p("愛着や信頼感に関わるオキシトシンは、ビタミンD（魚類・日光浴）がサポートします。"))
    n.append(sp())
    n.append(p("やる気と喜びのドーパミンは、乳製品・卵に含まれるアミノ酸が材料です。"))
    n.append(sp())
    n.append(p("「幸せは心がけ次第」という話をよく聞くけど、その心の状態をつくっているのは、毎日の食事でもあるんです。"))

    # アウトロ
    n.extend(heading_block("食事から始める、ウェルビーイングな婚活"))
    n.append(p("動画ではこの内容をもっと詳しくお話しています。ぜひご覧ください♪"))
    n.append(sp())
    n.append(p("婚活中の方——自分を整えることが、出会いを変えます。"))
    n.append(sp())
    n.append(p("特別なことじゃなくていい。毎日の野菜を1皿増やして、食卓を大切にして、飲み物をちょっと見直してみる。そういう小さな積み重ねが、あなたの気持ちを整えて、出会いの質を上げていきます。"))
    n.append(sp())
    n.append(p("食べるものが、あなたをつくる。あなたの関係性をつくる——そう思っています。"))

    # CTA
    n.append(sp())
    n.append(p("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan"))
    return n

def generate_and_import(prompt_text, filename):
    print(f"  DALL-E 3 生成中: {filename}")
    resp = client.images.generate(model="dall-e-3", prompt=prompt_text,
                                   size="1792x1024", quality="standard", n=1)
    dall_e_url = resp.data[0].url
    print(f"  生成完了。Wixにインポート中...")
    r = requests.post(f"{WIX_BASE}/site-media/v1/files/import", headers=wix_headers(),
                      json={"url": dall_e_url, "displayName": filename, "mimeType": "image/png"}, timeout=30)
    if not r.ok:
        return None
    data = r.json()
    file_id = (data.get("file") or {}).get("id") or data.get("fileId")
    if not file_id:
        return None
    for i in range(20):
        time.sleep(3)
        chk = requests.get(f"{WIX_BASE}/site-media/v1/files/{file_id}", headers=wix_headers(), timeout=15)
        if chk.ok:
            fd = chk.json().get("file", {})
            if fd.get("state") in ("READY", "OK"):
                url = fd.get("url", "")
                m = re.search(r"/media/([^?#\s]+)", url)
                print(f"  インポート完了: {url[:60]}...")
                return {"url": url, "id": m.group(1) if m else file_id,
                        "height": 1024, "width": 1792, "filename": filename}
            print(f"  待機中... ({fd.get('state')}, {i+1}/20)")
    return None

def main():
    today = "2026-04-29"
    title = "食べるものが、関係性を変える。——科学が教えてくれた、ウェルビーイングな食事の話。"

    prompts = [
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese couple enjoying a beautiful healthy meal together at a cozy dining table, "
         "colorful vegetables and wholesome food, warm candlelight, East Asian appearance, black hair, "
         "intimate and nourishing mood."),
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A cheerful arrangement of colorful fresh vegetables and fruits on a wooden table, "
         "surrounded by warm natural light, no people, abundant and inviting, "
         "soft green and orange tones, wellness aesthetic."),
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A split illustration: on the left a black coffee cup and healthy nuts/snacks; "
         "on the right an energy drink crossed out with a gentle red X, "
         "clean minimal background, soft educational but friendly tone."),
    ]

    print("\n[1/3] 画像を生成中...")
    img1 = generate_and_import(prompts[0], f"{today}_food_eyecatch.png")
    img2 = generate_and_import(prompts[1], f"{today}_food_img2.png")
    img3 = generate_and_import(prompts[2], f"{today}_food_img3.png")

    print("\n[2/3] Wixに下書き投稿中...")
    nodes = build_nodes(img2=img2, img3=img3)

    draft_post = {"title": title, "memberId": MEMBER_ID,
                  "richContent": {"nodes": nodes}, "categoryIds": [CATEGORY_ID]}
    if img1:
        m = re.search(r"/media/([^?#\s]+)", img1["url"])
        draft_post["media"] = {"custom": True, "wixMedia": {"image": {
            "id": m.group(1) if m else img1["id"], "url": img1["url"],
            "height": img1["height"], "width": img1["width"], "filename": img1["filename"],
        }}}

    resp = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(),
                         json={"draftPost": draft_post}, timeout=30)
    if not resp.ok:
        print(f"投稿失敗: {resp.status_code}\n{resp.text[:300]}")
        return

    draft_id = resp.json().get("draftPost", {}).get("id")

    related = ["8dc13d85-b85f-4247-8a8b-8ed90bad6bdc",
               "0c004668-d23a-40d3-a971-385f8dc6d799",
               "fe3d5fee-62be-4fdc-a23c-774eb57ff158"]
    excerpt = "野菜で魅力が上がる・血糖値スパイクがケンカを増やす・共食が関係性をつくる・隠れ貧血と気持ちの関係——食事と婚活・パートナーシップの科学を、わかりやすくお届けします。"
    requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(),
                   json={"draftPost": {"excerpt": excerpt, "relatedPostIds": related},
                         "fieldMask": "excerpt,relatedPostIds"}, timeout=30)

    print(f"\n[3/3] 完了！")
    print(f"  Wix下書きID: {draft_id}")
    print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")
    return draft_id

if __name__ == "__main__":
    main()
