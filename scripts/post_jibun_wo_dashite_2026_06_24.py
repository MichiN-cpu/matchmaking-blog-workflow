"""
【女性向け】最後のひとりに出会うまで、ぜんぶ「失敗」。——だったら、自分を出して失敗しよう。
カテゴリ: 仮交際（3f5f378d-a4f4-47e0-90a7-ab4daa27504e）
公開予定: 2026-06-25（水）下書き保存のみ
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["3f5f378d-a4f4-47e0-90a7-ab4daa27504e"]  # 仮交際

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "ec8941b1-d8b5-4e10-b909-4ad0029cd881",  # 女性の幸せ
]

RELATED_POST_IDS = [
    "64073f78-40d4-4695-ad8c-053ae2ff910e",  # 向かい合って話すだけが、デートじゃない
    "36915afc-e0aa-4b34-898b-106f66f11f33",  # 仮交際中、彼からLINEが来ない
    "78d9e1c5-9567-4c4c-a7d8-9b318a131ee9",  # 「どこ行こうか」から、ふたりは始まる
]

TITLE   = "【女性向け】最後のひとりに出会うまで、ぜんぶ「失敗」。——だったら、自分を出して失敗しよう。"
EXCERPT = "お見合いやデートで「いい子ちゃん」をしてしまう。相手に合わせすぎて、言いたいことが言えない——恋愛経験が少ない方ほど陥りやすいこの悩み。でも、最後のひとりに出会うまでは全部「失敗」なんだとしたら？愛媛の心理カウンセラー仲人が、会員さんとの対話から気づいた大切なことをお話しします。"
SEO_DESC = EXCERPT

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "../drafts/images")


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


def p(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "paragraphData": {}}


def p_bold(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": text,
            "decorations": [{"type": "BOLD", "boldData": {"bold": True}}]
        }}
    ], "paragraphData": {}}


def h(text, level=2):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": level}}


def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}


def section(heading_text):
    return [sp(), divider_node(), sp(), h(heading_text)]


def image_node(url, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": url}}, "caption": caption}}


def cta_node():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": "⬇️あなたに合った婚活を。無料相談はこちらから！⬇️",
            "decorations": [{"type": "LINK", "linkData": {
                "link": {"url": "https://www.asunaru.jp/soudan", "target": "BLANK"}
            }}]
        }}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}


def upload_image_binary(image_bytes, filename):
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "displayName": filename},
        timeout=30,
    )
    if not r.ok:
        print(f"  アップロードURL取得失敗: {r.status_code} {r.text[:200]}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        print(f"  uploadUrl取得失敗: {data}")
        return None
    sep  = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print(f"  アップロード失敗: {ru.status_code} {ru.text[:200]}")
        return None
    file_obj = ru.json().get("file", {})
    url = file_obj.get("url", "")
    if not url:
        print(f"  URL取得失敗: {ru.json()}")
        return None
    print(f"  → {url[:80]}...")
    return url


def upload_local_image(filename):
    path = os.path.join(IMAGE_DIR, filename)
    print(f"\n[アップロード中] {filename}")
    with open(path, "rb") as f:
        img_bytes = f.read()
    return upload_image_binary(img_bytes, filename)


def build_nodes(url_eyecatch, url_body1, url_body2):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # 導入：会員さんとの対話
    nodes.append(p("先日、ある会員さんとじっくりお話をしていたときのことなんです。"))
    nodes.append(sp())
    nodes.append(p("その方はね、とても話が弾む楽しい女性なんですよ。"))
    nodes.append(sp())
    nodes.append(p("自分の意見もしっかり持っていて、私との面談ではいろんな話ができる。"))
    nodes.append(sp())
    nodes.append(p("「この人と話していると面白いなぁ」って、仲人の私が毎回思うくらい。"))
    nodes.append(sp())
    nodes.append(p("でもね、お見合いやデートの場になると——それが出ない。"))
    nodes.append(sp())
    nodes.append(p("「つい相手に合わせちゃうんです」って言うんですよね。"))
    nodes.append(sp())
    nodes.append(p("気に入られたい。嫌われたくない。変なこと言って場の空気を壊したくない。"))
    nodes.append(sp())
    nodes.append(p("その気持ち、ものすごくわかるんです。"))
    nodes.append(sp())
    nodes.append(p("特に恋愛経験があまりない方だと、「正解の振る舞い」を探してしまうんですよね。"))
    nodes.append(sp())
    nodes.append(p('相手が喜びそうなことを言って、相手の話に合わせて、"いい子ちゃん"でいようとする。'))
    nodes.append(sp())
    nodes.append(p("でもそうすると、何回デートを重ねても、なんだかお互いのことが深まっていかないんです。"))
    nodes.append(sp())
    nodes.append(p("満足感も小さい。ウキウキもワクワクも中途半端。親密感も距離感も、思うように縮まらない。"))
    nodes.append(sp())
    nodes.append(p("こういう方、実はとても多いんですよね。"))
    nodes.append(sp())

    if url_eyecatch:
        nodes.append(image_node(url_eyecatch, "「自分を出す」って、こんなに楽しいことだったんだ。"))
        nodes.append(sp())

    # セクション1: 失敗しないようにやっていることが失敗
    nodes.extend(section("「失敗しないようにやっていること」が、失敗になっている"))
    nodes.append(sp())
    nodes.append(p("ちょっと立ち止まって考えてみてほしいんです。"))
    nodes.append(sp())
    nodes.append(p("私たちって、日々なんとなく「失敗しないように」動いていませんか。"))
    nodes.append(sp())
    nodes.append(p("仕事でも、人間関係でも、婚活でも。"))
    nodes.append(sp())
    nodes.append(p("無意識に、波風を立てない方向に、リスクの少ない方向に、自分を調整している。"))
    nodes.append(sp())
    nodes.append(p("でもね——今、思ったようにうまくいっていないとしたら。"))
    nodes.append(sp())
    nodes.append(p("それって、「失敗を避けようとしてやっていること」そのものが、実は失敗の方に傾いている行動だった、ということなんですよね。"))
    nodes.append(sp())
    nodes.append(p("心理学では、これを「安全行動（safety behavior）」と呼ぶことがあります。"))
    nodes.append(sp())
    nodes.append(p("不安を感じたとき、その不安を和らげるためにとる行動——たとえば「当たり障りのない話題だけ選ぶ」「自分の意見を言わない」「相手の顔色をうかがう」。"))
    nodes.append(sp())
    nodes.append(p("一見、安全に見える。"))
    nodes.append(sp())
    nodes.append(p("でも実は、これをやればやるほど「本当の自分を出したら嫌われる」という思い込みが強化されてしまう。"))
    nodes.append(sp())
    nodes.append(p("そして相手にも、あなたの本当の魅力が伝わらないまま時間だけが過ぎていくんです。"))
    nodes.append(sp())
    nodes.append(p("社会心理学者のマーク・スナイダーは、人には「セルフ・モニタリング」の傾向があると言いました。"))
    nodes.append(sp())
    nodes.append(p("周囲の期待に合わせて自分の振る舞いを調整する力のことです。"))
    nodes.append(sp())
    nodes.append(p("これ自体は社会生活で役立つ能力なんですが、婚活の場でこれが強く出すぎると——相手に見せているのは「あなた」ではなく、「相手が望むであろうあなた」になってしまうんです。"))
    nodes.append(sp())
    nodes.append(p("それでは、どれだけ回数を重ねても、本当の意味での出会いにはならない。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、もどかしいんですよね。"))
    nodes.append(sp())

    # セクション2: どうせ全部失敗
    nodes.extend(section("最後のひとりに出会うまで、どうせ全部「失敗」"))
    nodes.append(sp())
    nodes.append(p("さて、ここからが今日いちばん伝えたいことです。"))
    nodes.append(sp())
    nodes.append(p("会員さんとの話の中で、こんな話になったんです。"))
    nodes.append(sp())
    nodes.append(p("結婚相談所で婚活をしているということは、最後にご成婚退会するお相手——その「たったひとり」に出会うまで活動を続けるということですよね。"))
    nodes.append(sp())
    nodes.append(p("ということは、その最後のひとりに出会うまでに出会う人たちとは、結局どうなるかというと……「成功」ではない。"))
    nodes.append(sp())
    nodes.append(p("「成功か失敗か」の二択で言うなら、全部「失敗」に入っちゃうわけです。"))
    nodes.append(sp())
    nodes.append(p_bold("どうせ失敗なんですよ、最後のひとりにたどり着くまでは。"))
    nodes.append(sp())
    nodes.append(p("だったらね。"))
    nodes.append(sp())
    nodes.append(p("言いたいこと言わないで、相手に合わせて、ちょっと無理して、モヤモヤしたまま、不十分な楽しさで、中途半端なウキウキで、そういうデートを重ねて「失敗」するよりも——"))
    nodes.append(sp())
    nodes.append(p_bold("言いたいこと言って、自分を出して、それで「失敗」したほうがよくないですか？"))
    nodes.append(sp())
    nodes.append(p("もちろん、「言い方」は別ですよ。"))
    nodes.append(sp())
    nodes.append(p("優しく、楽しく、丁寧に。言い方はいくらでも工夫できる。"))
    nodes.append(sp())
    nodes.append(p("でも、言う中身は——自分が本当に思っていることを、ちゃんと出していい。"))
    nodes.append(sp())
    nodes.append(p("「私はこういうのが好きなんです」"))
    nodes.append(sp())
    nodes.append(p("「ここに行ってみたいなって思ってたんです」"))
    nodes.append(sp())
    nodes.append(p("「実は私、こういうの苦手で（笑）」"))
    nodes.append(sp())
    nodes.append(p("こういう「自分」を出して、それで合わなかったなら——それは「いい失敗」なんです。"))
    nodes.append(sp())
    nodes.append(p("だって、合わない人と早くわかったということだから。"))
    nodes.append(sp())
    nodes.append(p("逆に、そこで相手が「へえ、面白いね」って笑ってくれたなら——それが本当の出会いの始まりなんですよね。"))
    nodes.append(sp())

    if url_body1:
        nodes.append(image_node(url_body1, "「パスタがいいな」——その一言から、本当の出会いが始まる。"))
        nodes.append(sp())

    # セクション3: 反応パターン
    nodes.extend(section("不安は、性格じゃなくて反応パターン"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("デートで「何食べたい？」と聞かれて、本当はパスタが食べたいのに「なんでもいいよ」と答えてしまう。"))
    nodes.append(sp())
    nodes.append(p("相手の趣味に興味がないのに、「すごいですね！」とオーバーに反応してしまう。"))
    nodes.append(sp())
    nodes.append(p("帰り道、「今日も自分を出せなかったな」と、ひとりで落ち込む。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方。安心してください。"))
    nodes.append(sp())
    nodes.append(p("それは、あなたの性格ではありません。"))
    nodes.append(sp())
    nodes.append(p("右利きの人が何も考えずに右手でペンを持つように、「相手に合わせておけば安全」という反応が、長い時間をかけて体に染みついているだけなんです。"))
    nodes.append(sp())
    nodes.append(p("そしてね、反応パターンは変えられるんですよ。"))
    nodes.append(sp())
    nodes.append(p("いきなり「自分を全部出そう！」なんてしなくていい。"))
    nodes.append(sp())
    nodes.append(p("まずは、小さなところから。"))
    nodes.append(sp())
    nodes.append(p("「何食べたい？」って聞かれたら、「パスタかな」って言ってみる。"))
    nodes.append(sp())
    nodes.append(p("それだけでいいんです。"))
    nodes.append(sp())
    nodes.append(p("その一言が、古い反応パターンをゆるめる、最初の一歩になるから。"))
    nodes.append(sp())

    # セクション4: 自分を出せる人は愛される
    nodes.extend(section("「自分を出せる人」は、愛される"))
    nodes.append(sp())
    nodes.append(p("最後に、ちょっとだけ先の話をさせてください。"))
    nodes.append(sp())
    nodes.append(p("ブレネー・ブラウンという研究者が、何千人もの人にインタビューして見つけたことがあります。"))
    nodes.append(sp())
    nodes.append(p("「深い人間関係を持っている人たち」に共通していたのは、完璧であることでも、相手に合わせることでもなくて——自分の不完全さを見せる勇気を持っていることだったんです。"))
    nodes.append(sp())
    nodes.append(p("（興味のある方は、彼女の著書『本当の勇気は「弱さ」を認めること』（サンマーク出版）をぜひ読んでみてください。婚活に限らず、人間関係がすっと楽になるヒントがたくさん詰まっています。）"))
    nodes.append(sp())
    nodes.append(p("婚活でもね、同じなんですよ。"))
    nodes.append(sp())
    nodes.append(p("完璧な受け答えをする人より、「あ、ちょっと緊張してます（笑）」って正直に言える人のほうが、相手の心に残る。"))
    nodes.append(sp())
    nodes.append(p("会員さんと話していて、私は思ったんです。"))
    nodes.append(sp())
    nodes.append(p("この方が面談で見せてくれる——いろんなことを考えていて、自分の意見を持っていて、話していると楽しい、あの姿。"))
    nodes.append(sp())
    nodes.append(p("あれを、お見合いの場でもじゃんじゃん出してほしいなぁ、と。"))
    nodes.append(sp())
    nodes.append(p("そして会員さんも言ってくれました。"))
    nodes.append(sp())
    nodes.append(p("「確かにそうですね。最後のひとりに出会うまで、結局は失敗なんだから。臆さず、私を出していきたいと思います」って。"))
    nodes.append(sp())
    nodes.append(p("……ね、かっこいいでしょう。"))
    nodes.append(sp())

    if url_body2:
        nodes.append(image_node(url_body2, "自分を出せたとき、相手の笑顔も本物になる。"))
        nodes.append(sp())

    # 今週の一歩
    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("次のお見合いかデートで、「なんでもいいよ」を一回だけやめてみてください。"))
    nodes.append(sp())
    nodes.append(p("飲み物でも、行き先でも、なんでもいいんです。"))
    nodes.append(sp())
    nodes.append(p("「私は○○がいいな」って、たった一言。"))
    nodes.append(sp())
    nodes.append(p("言い方は柔らかくていい。でも中身は、自分の本音で。"))
    nodes.append(sp())

    # CTA
    nodes.append(cta_node())

    return {"nodes": nodes}


def create_draft(rich_content):
    body = {
        "draftPost": {
            "title": TITLE,
            "memberId": MEMBER_ID,
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "richContent": rich_content,
        }
    }
    r = requests.post(
        f"{WIX_BASE}/blog/v3/draft-posts",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"下書き作成失敗: {r.status_code} {r.text[:300]}")
        return None
    return r.json().get("draftPost", {}).get("id")


def update_excerpt_related(post_id):
    body = {
        "draftPost": {
            "excerpt": EXCERPT,
            "relatedPostIds": RELATED_POST_IDS,
        },
        "fieldMask": "excerpt,relatedPostIds"
    }
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{post_id}",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"excerpt/relatedPosts PATCH失敗: {r.status_code} {r.text[:300]}")
    return r.ok


def update_cover_image(post_id, cover_url):
    body = {
        "draftPost": {
            "media": {
                "wixMedia": {
                    "image": cover_url
                },
                "displayed": True,
                "custom": False,
            }
        },
        "fieldMask": "media"
    }
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{post_id}",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"coverMedia PATCH失敗: {r.status_code} {r.text[:300]}")
    return r.ok


def update_seo(post_id):
    body = {
        "draftPost": {
            "seoData": {"description": SEO_DESC}
        },
        "fieldMask": "seoData.description"
    }
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{post_id}",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"seoData PATCH失敗: {r.status_code} {r.text[:300]}")
    return r.ok


def main():
    print("=== 自分を出して失敗しよう 投稿スクリプト ===\n")

    # 1. ローカル画像をWixにアップロード
    url_eyecatch = upload_local_image("2026-06-24_eyecatch.png")
    url_body1    = upload_local_image("2026-06-24_body1.png")
    url_body2    = upload_local_image("2026-06-24_body2.png")

    # 2. richContent構築
    print("\n[richContent構築中...]")
    rich_content = build_nodes(url_eyecatch, url_body1, url_body2)

    # 3. 下書き作成
    print("\n[Wix下書き作成中...]")
    post_id = create_draft(rich_content)
    if not post_id:
        print("失敗。終了します。")
        return

    print(f"  → 下書きID: {post_id}")

    # 4. excerpt・関連記事を更新
    print("\n[excerpt・関連記事を更新中...]")
    ok = update_excerpt_related(post_id)
    print(f"  → {'成功' if ok else '失敗'}")

    # 5. カバー画像を更新
    if url_eyecatch:
        print("\n[カバー画像を更新中...]")
        ok = update_cover_image(post_id, url_eyecatch)
        print(f"  → {'成功' if ok else '失敗'}")

    # 6. SEO description を更新
    print("\n[SEO descriptionを更新中...]")
    ok = update_seo(post_id)
    print(f"  → {'成功' if ok else '失敗'}")

    print(f"\n✅ 完了！\n下書きID: {post_id}")
    print("Wixブログ管理画面で確認してください。")
    print("⚠️ 画像が正しく表示されているか、必ず確認をお願いします。")


if __name__ == "__main__":
    main()
