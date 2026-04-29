#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友人の結婚後の変化 - Wix投稿スクリプト
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
    n.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    n.append(sp())
    n.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    n.append(sp())

    n.append(p("先日、友人の婚活体験談を動画でご紹介しました。"))
    n.append(sp())
    n.append(p("3年間の婚活を経て、「好きから始まらなくていい」と気づきながら結婚へたどり着いた彼女の話です。"))
    n.append(sp())
    n.append(p("でね、動画の撮影後に彼女がぽつりぽつりと話してくれたことがあって。"))
    n.append(sp())
    n.append(p("「結婚してから、自分が変わったなぁって思うことがいっぱいあるんだよね」"))
    n.append(sp())
    n.append(p("その言葉が、ずっと心に残っていて。今日はその話を書かせてください。"))

    n.extend(heading_block("行動範囲が、ふわっと広がった"))
    n.append(p("結婚前の彼女は、県外への遠出がちょっとハードルが高かったそうです。"))
    n.append(sp())
    n.append(p("「遠いし、どうしようかな」ってためらっていたことが、今はぜんぜん気にならなくなった。ふたりで気軽にドライブに出かけられるようになって、行ったことのない場所がどんどん増えていると。"))
    n.append(sp())
    n.append(p("これ、すごくよくわかるんですよね。"))
    n.append(sp())
    n.append(p("一人だと「面倒だな」と思っていたことが、一緒に行く人がいるだけで急に「行ってみようか」に変わる。行動半径がふわっと広がる感覚。これって、パートナーという存在が「世界を広げてくれる」ということだと思うんです。"))
    n.append(sp())
    n.append(p("社会心理学者のアーサー・アロンは「自己拡張理論」という考え方を提唱しています。親密な関係を通じて、相手の視点・知識・行動範囲が自分の中に取り込まれ、自分自身が拡張されていく——という理論です。彼女が体験していたのは、まさにこれだったんじゃないかなと思います。"))

    if img2:
        n.append(sp())
        n.append(img_node(img2, "結婚で広がる行動範囲と新しい体験"))
        n.append(sp())

    n.extend(heading_block("食事が、丁寧になった"))
    n.append(p("もう一つ彼女が話してくれたのが、食事の変化でした。"))
    n.append(sp())
    n.append(p("国産の食材を選ぶようになった。野菜をたくさん食べるようになった。以前より食事を丁寧に、大切に考えるようになったと。"))
    n.append(sp())
    n.append(p("かつての一人暮らしのときは、そこまで気にしていなかったそうです。でも彼と一緒に食卓を囲む中で、食べることへの向き合い方が変わっていった。"))
    n.append(sp())
    n.append(p("「誰かのために作る」「誰かと一緒に食べる」——それだけで、食事ってこんなに変わるんですよね。"))
    n.append(sp())
    n.append(p("栄養学的にも、食事の質が上がると体調が整って気持ちも安定しやすくなると言われています。彼女の声が明るくなったのは、そういう積み重ねもあるんじゃないかなって。"))

    n.extend(heading_block("良いものに、囲まれるようになった"))
    n.append(p("それから、家具や身の回りのものの選び方も変わったと言っていました。"))
    n.append(sp())
    n.append(p("以前の彼女だったら「高いからなぁ」と手が出せなかったものも、彼が「いいものを長く使えばいいよ」と言って一緒に選んでくれる。"))
    n.append(sp())
    n.append(p("そうやって気に入ったものに囲まれていると、毎日の気持ちがぜんぜん違うんですよね。"))
    n.append(sp())
    n.append(p("「安いから」ではなく「好きだから」「長く使いたいから」という基準で選ぶようになった——これって、自分を大切にすることへのハードルが下がったということだと思うんです。「私にはこれくらいでいい」が「私にはいいものを」に変わっていく。それは単なる消費行動の変化じゃなくて、自己肯定感の変化でもあります。"))

    if img3:
        n.append(sp())
        n.append(img_node(img3, "良いものに囲まれる暮らし"))
        n.append(sp())

    n.extend(heading_block("キャッシュレスになった（笑）"))
    n.append(p("ちょっと笑ってしまったのが「キャッシュレス生活になった」という変化（笑）。"))
    n.append(sp())
    n.append(p("彼のライフスタイルに影響を受けて、知らなかった便利さを知った。小さいことだけど、こういう「へえ、そういう世界があるんだ」という発見の積み重ねが、日々を面白くするんですよね。"))

    n.extend(heading_block("違う文化の融合が、結婚の醍醐味"))
    n.append(p("彼女の話を聞きながら、私がずっと思っていたことが言葉になった気がしました。"))
    n.append(sp())
    n.append(p("結婚って、「同じ人間が二人になる」んじゃなくて、「違う文化を持った二人が融合する」ことなんですよね。"))
    n.append(sp())
    n.append(p("食の好み、お金の使い方、行動の範囲、生活のリズム——どれも違うふたりが一緒に暮らし始めて、お互いの良いところを取り合いながら、新しい文化をつくっていく。"))
    n.append(sp())
    n.append(p("彼女は結婚を通じて、自分がより豊かになっていった。自分の知らなかった世界を知って、自分をより大切にするようになった。"))
    n.append(sp())
    n.append(p("それって、素敵じゃないですか。"))
    n.append(sp())
    n.append(p("婚活中の方に伝えたいのは——「自分に合う人を探す」だけじゃなくて、「一緒に新しい自分になれる人を探す」という視点です。"))
    n.append(sp())
    n.append(p("あなたの世界を広げてくれる人が、きっといます。"))
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
                return {"url": url, "id": m.group(1) if m else file_id, "height": 1024, "width": 1792, "filename": filename}
            print(f"  待機中... ({fd.get('state')}, {i+1}/20)")
    return None

def main():
    today = "2026-04-29"
    title = "「結婚してから、自分がどんどん好きになっていった」——友人が教えてくれた、変化の話。"

    prompts = [
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese couple driving together on a scenic road trip, smiling and enjoying the journey, "
         "East Asian appearance, black hair, warm sunlight, open road ahead, hopeful and free mood."),
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese couple cooking together at home, fresh vegetables and produce on the kitchen counter, "
         "warm domestic scene, East Asian appearance, black hair, cozy and nurturing mood."),
        ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
         "A Japanese couple choosing furniture together in a warm home, surrounded by quality items they love, "
         "East Asian appearance, black hair, soft interior lighting, content and happy mood."),
    ]

    print("\n[1/3] 画像を生成中...")
    img1 = generate_and_import(prompts[0], f"{today}_henka_eyecatch.png")
    img2 = generate_and_import(prompts[1], f"{today}_henka_img2.png")
    img3 = generate_and_import(prompts[2], f"{today}_henka_img3.png")

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

    # excerpt + related posts (仮交際カテゴリから)
    related = ["8dc13d85-b85f-4247-8a8b-8ed90bad6bdc",
               "98e9d8cd-841a-40be-bc14-0ab36f37a867",
               "fe3d5fee-62be-4fdc-a23c-774eb57ff158"]
    excerpt = "結婚後、行動範囲が広がり、食事が丁寧になり、良いものに囲まれるようになった——友人が話してくれた変化の数々。違う文化を持つふたりが融合していく、それが結婚の醍醐味だと気づかされました。"
    requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(),
                   json={"draftPost": {"excerpt": excerpt, "relatedPostIds": related},
                         "fieldMask": "excerpt,relatedPostIds"}, timeout=30)

    print(f"\n[3/3] 完了！")
    print(f"  Wix下書きID: {draft_id}")
    print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")
    return draft_id

if __name__ == "__main__":
    main()
