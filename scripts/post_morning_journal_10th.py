#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
モーニングジャーナル第10期 参加募集ブログ - Wix投稿スクリプト
"""

import os, re, time, uuid, requests, base64

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_ID = "fc247847-d52b-438c-ab23-95bae771dc0a"  # お知らせ

IMG_DIR = os.path.expanduser("~/matchmaking-blog-workflow/drafts/images")

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

def p_center(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": make_text_nodes(text),
            "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}

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

def create_tag(label):
    r = requests.post(f"{WIX_BASE}/blog/v3/tags", headers=wix_headers(),
                      json={"tag": {"label": label}}, timeout=15)
    if r.ok:
        tag_id = r.json().get("tag", {}).get("id")
        print(f"  タグ作成: {label} ({tag_id})")
        return tag_id
    print(f"  タグ作成失敗 ({label}): {r.text[:100]}")
    return None

def generate_and_upload(prompt, filename):
    print(f"  画像生成中: {filename}")
    local_path = os.path.join(IMG_DIR, filename)

    # Generate with gpt-image-1
    r = requests.post("https://api.openai.com/v1/images/generations",
                      headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
                      json={"model": "gpt-image-1", "prompt": prompt,
                            "size": "1536x1024", "quality": "medium", "n": 1},
                      timeout=120)
    if not r.ok:
        print(f"  画像生成失敗: {r.text[:200]}")
        return None

    img_bytes = base64.b64decode(r.json()["data"][0]["b64_json"])
    with open(local_path, 'wb') as f:
        f.write(img_bytes)
    print(f"  ローカル保存: {local_path}")

    # Get Wix upload URL
    up_url_r = requests.get(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        params={"mimeType": "image/png", "fileName": filename},
        timeout=30)
    if not up_url_r.ok:
        print(f"  Wix upload URL取得失敗: {up_url_r.status_code} {up_url_r.text[:200]}")
        return None

    up_data = up_url_r.json()
    upload_url   = up_data.get("uploadUrl")
    upload_token = up_data.get("uploadToken")
    if not upload_url:
        print(f"  uploadUrl not found: {up_data}")
        return None

    # PUT binary to upload URL
    up_headers = {"Content-Type": "image/png"}
    if upload_token:
        up_headers["Authorization"] = upload_token
    put_r = requests.put(upload_url, data=img_bytes, headers=up_headers, timeout=60)
    if not put_r.ok:
        print(f"  PUT失敗: {put_r.status_code} {put_r.text[:200]}")
        return None

    put_data = put_r.json()
    file_id = (put_data.get("file") or {}).get("id") or put_data.get("fileId")
    if not file_id:
        print(f"  file_id not found in: {str(put_data)[:200]}")
        return None

    # Poll until READY
    for i in range(20):
        time.sleep(3)
        chk = requests.get(f"{WIX_BASE}/site-media/v1/files/{file_id}", headers=wix_headers(), timeout=15)
        if chk.ok:
            fd = chk.json().get("file", {})
            if fd.get("state") in ("READY", "OK"):
                url = fd.get("url", "")
                m = re.search(r"/media/([^?#\s]+)", url)
                print(f"  Wixアップロード完了: {url[:60]}...")
                return {"url": url, "id": m.group(1) if m else file_id,
                        "height": 1024, "width": 1536, "filename": filename}
            print(f"  待機中... ({fd.get('state')}, {i+1}/20)")
    return None

def build_nodes(img2=None, img3=None):
    n = []

    # 冒頭挨拶
    n.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    n.append(sp())
    n.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    n.append(sp())

    # イントロ
    n.append(p("6月26日から、モーニングジャーナル第10期がスタートします！！"))
    n.append(sp())
    n.append(p("今日は、この会を9期続けてきてわかった「朝の15分が人生を変える理由」を、科学と私の実体験を交えながら、じっくりお伝えしますね。"))

    # ミニ診断
    n.extend(heading_block("ちょっと、聞いてもいいですか。"))
    n.append(p("夜、横になってからつい悩みごとが浮かんできて、なかなか頭が静まらなかったり。"))
    n.append(sp())
    n.append(p("スマホのLINEを何度も確認して、なんとなく時間が過ぎてしまったり。"))
    n.append(sp())
    n.append(p("翌朝、ギリギリに起きてバタバタしながら「あ〜また今日も…」ってため息をついてしまったり。"))
    n.append(sp())
    n.append(p("——そんなこと、ありませんか？"))
    n.append(sp())
    n.append(p("これ、あなたの意志が弱いんじゃなくて、夜の脳の特性なんですよね。右利きの人が無意識に右手を使うように、夜になるとネガティブな思考に引き寄せられる「反応パターン」が自然と動き出してしまう。だから夜に頑張ろうとしても、なかなかうまくいかないのは当然なんです。"))

    # モーニングジャーナルとは
    n.extend(heading_block("モーニングジャーナルって何？"))
    n.append(p("毎朝5:45〜6:00の15分間、Zoomで繋いで好きなことを黙々と書く会です。"))
    n.append(sp())
    n.append(p("書く内容は自由。今感じていること、昨日の感謝、これからの夢、なんでも。5:45〜はひたすら黙々と書き書きTIME、5:58〜は書けた私たちをみんなで労いあうTIME。それだけです。"))
    n.append(sp())
    n.append(p("「なんでわざわざZoomで繋ぐの？」ってよく聞かれるんですけど（笑）、これがミソなんですよ。一人でやると続かなくても、誰かと繋がっていると書ける。仲間の存在が「場のエネルギー」になってくれるんです。"))

    if img2:
        n.append(sp())
        n.append(img_node(img2, "毎朝Zoomで繋がりながら、静かに書く時間"))
        n.append(sp())

    # 科学的根拠
    n.extend(heading_block("脳科学的に説明できること"))
    n.append(p("私たちの体には「概日リズム（サーカディアンリズム）」という24時間の生体時計があります。朝の光を浴びて早起きすることで、覚醒ホルモンが適切に分泌され、集中力と判断力が整ってくる。夜遅くまでスマホを見たり、ネガティブな思考に引きずられたりするのは、この生体リズムが乱れているサインでもあるんです。"))
    n.append(sp())
    n.append(p("さらに、心理学者ペネベーカーの研究では、想いを「書いて外に出すこと（エモーショナル・ディスクロージャー）」が、ストレス軽減・感情の安定・免疫機能の向上につながることが示されています。書くことは、単なるアウトプットじゃない。心の解毒であり、自己認識を深めるプロセスなんです。"))
    n.append(sp())
    n.append(p("朝の静かな時間に書くのには、もう一つ理由があります。脳には「デフォルトモードネットワーク（DMN）」という、ぼんやりしているときに活発になる回路があります。朝、まだ忙しさに引っ張られる前のこの時間は、DMNが最もクリエイティブに動く時間帯。アイデアが浮かびやすく、自分の本音が出やすい。参加者さんから「旅行中も書きたくなった」「朝から充実感がある」「イライラ・もやもやが減った」と言っていただけるのは、きっとそのせいだと思っています。"))

    # 見た目の変化
    n.extend(heading_block("もう一つ、正直に言うと。"))
    n.append(p("朝型になると、見た目が変わります。"))
    n.append(sp())
    n.append(p("夜ちゃんと眠れて、朝スッキリ起きられる。それだけで顔のむくみが取れて、肌のトーンが上がって、表情が明るくなる。これは私自身が実感していることです（9期続けて、朝の自分の顔がだいぶ好きになってきた笑）。"))
    n.append(sp())
    n.append(p("夜のLINEのやりとりも「明日の朝に返すね」って言えるようになって。そして翌朝、爽やかな気持ちで「行ってらっしゃい」が送れる。朝型の生活って、人間関係まで変えてくれる気がしています。"))

    if img3:
        n.append(sp())
        n.append(img_node(img3, "朝の静けさが、一日の土台をつくる"))
        n.append(sp())

    # 今週の一歩
    n.extend(heading_block("今日からできる一歩"))
    n.append(p("今夜、いつもよりLINEを閉じる時間を30分早めてみてください。それだけで、明日の朝が少し違って感じられるはず。"))

    # 申し込み情報
    n.extend(heading_block("第10期 参加詳細"))
    n.append(p("第10期：2026年6月26日（木）スタート・100日間"))
    n.append(sp())
    n.append(p("参加費：1,500円（税込）"))
    n.append(sp())
    n.append(p("時間：毎朝5:45〜6:00（Zoom）"))
    n.append(sp())
    n.append(p("途中からでも、途中で挫けてもまたスタートでOK！"))
    n.append(sp())
    n.append(p_center("⬇️ お申し込みはこちらから ⬇️ https://cocokara2525.base.shop/items/81637029"))
    n.append(sp())
    n.append(p("一緒に最高の朝を作りましょう♪　待ってます！！"))

    # あすなるCTA
    n.append(sp())
    n.append(p_center("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan"))

    return n


def main():
    today = "2026-06-12"
    title = "【男女共通】第10期スタート！毎朝5時45分に、自分に帰ってくる15分のはなし。"

    base_prompt = (
        "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
        "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
        "real-world setting, professional lifestyle photography style, "
        "shallow depth of field, clean bright modern atmosphere, no text, no warm tones"
    )

    prompts = [
        f"{base_prompt}. Sitting at a wooden desk near a large window in early morning, writing peacefully in an open notebook, serene and focused expression, morning light.",
        f"{base_prompt}. Smiling gently while using a laptop in early morning, soft warm morning light on face, cozy and energized expression.",
        "Photorealistic, cinematic quality, a cup of coffee and an open notebook with a pen on a white desk near a bright morning window, soft natural daylight, fresh and clean atmosphere, no people, no text, no warm tones.",
    ]

    # 1. Create new tags
    print("\n[1/5] タグ作成...")
    tag_ids = []
    for label in ["朝活", "モーニングジャーナル"]:
        tid = create_tag(label)
        if tid:
            tag_ids.append(tid)
    tag_ids += [
        "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
        "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
        "d5599216-6bdd-47df-9af3-07d1c15c1539",  # 願いを叶える
    ]

    # 2. Generate & upload images
    print("\n[2/5] 画像生成・アップロード...")
    img1 = generate_and_upload(prompts[0], f"{today}_morning_journal_eyecatch.png")
    img2 = generate_and_upload(prompts[1], f"{today}_morning_journal_img2.png")
    img3 = generate_and_upload(prompts[2], f"{today}_morning_journal_img3.png")

    # 3. Build richContent nodes
    print("\n[3/5] 記事ノード組み立て...")
    nodes = build_nodes(img2=img2, img3=img3)

    # 4. Create Wix draft post
    print("\n[4/5] Wix下書き投稿...")
    draft_post = {
        "title": title,
        "memberId": MEMBER_ID,
        "richContent": {"nodes": nodes},
        "categoryIds": [CATEGORY_ID],
        "tagIds": tag_ids,
    }

    if img1:
        m = re.search(r"/media/([^?#\s]+)", img1["url"])
        draft_post["media"] = {"custom": True, "wixMedia": {"image": {
            "id": m.group(1) if m else img1["id"],
            "url": img1["url"],
            "height": img1["height"],
            "width": img1["width"],
            "filename": img1["filename"],
        }}}

    resp = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(),
                         json={"draftPost": draft_post}, timeout=30)
    if not resp.ok:
        print(f"投稿失敗: {resp.status_code}\n{resp.text[:300]}")
        return
    draft_id = resp.json().get("draftPost", {}).get("id")
    print(f"  下書きID: {draft_id}")

    # 5. Update excerpt + related posts
    print("\n[5/5] excerpt・関連記事更新...")
    rp_resp = requests.post(f"{WIX_BASE}/blog/v3/posts/query", headers=wix_headers(),
                            json={"filter": {"categoryIds": {"$hasSome": [CATEGORY_ID]}},
                                  "paging": {"limit": 5}}, timeout=15)
    related = []
    if rp_resp.ok:
        posts = rp_resp.json().get("posts", [])
        related = [post["id"] for post in posts if post.get("id") != draft_id][:3]

    excerpt = "毎朝5:45〜6:00の15分、Zoomで繋いで書くだけ。9期続けてわかった「朝の習慣が人生を変える理由」を、脳科学と実体験を交えてお伝えします。第10期は6月26日スタート！"
    patch_body = {"draftPost": {"excerpt": excerpt}, "fieldMask": "excerpt"}
    if related:
        patch_body["draftPost"]["relatedPostIds"] = related
        patch_body["fieldMask"] += ",relatedPostIds"

    pr = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
                        headers=wix_headers(), json=patch_body, timeout=15)
    print(f"  excerpt更新: {'OK' if pr.ok else pr.text[:100]}")

    print(f"\n✅ 完了！")
    print(f"  下書きID: {draft_id}")
    print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")
    return draft_id


if __name__ == "__main__":
    main()
