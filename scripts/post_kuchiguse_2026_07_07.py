"""
【男女共通】「楽勝」が口癖になった人から、婚活はうまくいく。
カテゴリ: 無料相談の前に読む（641187e4-a409-4c2f-9639-ecc548f26f15）
下書き保存のみ（公開日時未定）
"""
import os, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["641187e4-a409-4c2f-9639-ecc548f26f15"]  # 無料相談の前に読む

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "e32aa046-3630-4653-aa5c-7c765507b399",  # 焦点化
]

RELATED_POST_IDS = [
    "43d9ae43-938c-47a0-b889-e5aa397b6e07",  # AI美知仲人コーチ、誕生しました NLPの心理技術で...
    "49bc08d5-9927-48c8-a37a-9124b0c43fce",  # 行動より先に"あるもの"を変えている｜潜在意識とメンタルイメージ
    "1418a8d9-ed79-4a1e-85fd-4c3fc644eae6",  # 矛盾したサインが止まらない──ダブルバインド
]

TITLE   = "【男女共通】「楽勝」が口癖になった人から、婚活はうまくいく。"
EXCERPT = "「しんどい」「めんどくさい」が口癖になっていませんか？その口癖、実は育った環境から無意識に学習したものかもしれません。NLPと脳科学の視点から、言葉を変えるだけで婚活の見え方が変わる理由と、今日からできる言い換えの練習法をご紹介します。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
            "relaxed Japanese couple in their 30s laughing together in a bright modern kitchen, "
            "candid joyful expression, facing each other, looking at each other not at camera, "
            "clean bright modern atmosphere, shallow depth of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-07_kuchiguse_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, "
            "view through a car windshield of a bright sunny Japanese city street, "
            "clean modern atmosphere, no people, no text, "
            "shallow depth of field, professional photography"
        ),
        "filename": "2026-07-07_kuchiguse_focus.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
            "Japanese couple in their 30s cooking together in a warm bright kitchen preparing traditional New Year food, "
            "smiling, facing each other, looking at each other not at camera, "
            "clean bright modern atmosphere, shallow depth of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-07_kuchiguse_newyear.png",
    },
]

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


def generate_and_upload_image(prompt, filename):
    print(f"\n[gpt-image-1] 生成中: {filename}")
    resp = client.images.generate(
        model="gpt-image-1", prompt=prompt, size="1536x1024", quality="high", n=1,
    )
    img_data = resp.data[0]
    if not img_data.b64_json:
        print("  b64_json取得失敗")
        return None
    img_bytes = base64.b64decode(img_data.b64_json)
    save_path = os.path.join(os.path.dirname(__file__), f"../drafts/images/{filename}")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(img_bytes)
    print("  生成完了。Wixにアップロード中...")
    return upload_image_binary(img_bytes, filename)


def build_nodes(url1, url2, url3):
    nodes = []

    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    nodes.append(p("今日は、婚活そのものというより、その手前にある「口癖」の話をしたいんです。"))
    nodes.append(sp())
    nodes.append(p("「人と会うのってしんどいな」「連絡するのめんどくさいな」「今度の顔合わせ、大変そうだな」——こういう言葉、一日のうちに何回くらい使っていますか。"))
    nodes.append(sp())

    if url1:
        nodes.append(image_node(url1, "「楽勝」が口癖になると、婚活の景色も変わります"))
        nodes.append(sp())

    nodes.extend(section("口癖は「性格」じゃなくて、育った環境で学習したもの"))
    nodes.append(sp())
    nodes.append(p("実はこれ、性格の問題でも、婚活への意欲の問題でもないんです。多くの場合、育った環境の中で、周りの大人たちが使っていた言葉をそのまま学習しているだけなんですよね。"))
    nodes.append(sp())
    nodes.append(p_bold("右利きの人が、左手で箸を持つと不自由に感じるように、口癖もまた、幼い頃から繰り返し聞いて、繰り返し使ってきた「慣れた反応」のひとつです。"))
    nodes.append(sp())
    nodes.append(p("性格の欠陥ではなく、ただの学習結果。学習したものなら、学び直すこともできます。"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("人間関係のことになると、つい「めんどくさい」が口をついて出る。実家や義理の家族との付き合いを考えると、話す前から「大変そう」と身構えてしまう。お正月やお盆のような親戚の集まりが近づくと、楽しみより先に「しんどいな」が浮かんでくる。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるある」と思った方は、このあとの話、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section("「ぞろ目ナンバー」が急に増えて見える理由"))
    nodes.append(sp())
    nodes.append(p("少し面白い実験を紹介させてください。"))
    nodes.append(sp())
    nodes.append(p("「ぞろ目ナンバー、ぞろ目ナンバー」と頭の中でつぶやきながら車を走らせてみてください。不思議なことに、その日はやたらとぞろ目のナンバープレートが目につくはずです。もちろん、その日だけぞろ目の車が増えたわけではありません。"))
    nodes.append(sp())
    nodes.append(p_bold("そこに意識が向いたから、見えるようになっただけなんです。"))
    nodes.append(sp())
    nodes.append(p("脳には「網様体賦活系(もうようたいふかつけい)」という、無数の情報の中から今の自分に必要なものだけを拾い上げる仕組みがあります。私たちが日頃つぶやいている言葉は、この仕組みに「何を拾うか」の指令を出し続けているようなものなんですね。"))
    nodes.append(sp())

    if url2:
        nodes.append(image_node(url2, "言葉は、私たちが何に気づくかを方向づけています"))
        nodes.append(sp())

    nodes.append(p("だから「めんどくさい」を繰り返す人は、めんどくさい要素ばかりが目につくようになり、「楽勝」を繰り返す人は、楽勝な要素に自然と気づけるようになる。言葉は、単なる表現の道具ではなくて、私たちの知覚そのものを方向づけているんです。"))
    nodes.append(sp())
    nodes.append(p("心理学では、これに近い現象を社会的学習理論と呼びます。子どもは周りの大人の行動や言葉を観察し、真似ることで多くのことを身につけていく、という考え方です。「〇〇はしんどいものだ」という大人の口癖を繰り返し聞いて育てば、〇〇に人間関係が入ろうと、家事が入ろうと、結婚生活が入ろうと、疑うことなくその前提を引き継いでしまう。"))
    nodes.append(sp())
    nodes.append(p("家族社会学の視点で見ても、言葉の使い方は家庭という最小単位のコミュニティの中で世代を超えて受け継がれていく、ということがよく知られています。"))
    nodes.append(sp())

    nodes.extend(section("私自身の話をすると"))
    nodes.append(sp())
    nodes.append(p("正直に言うと、私自身もこの口癖の影響を強く受けてきた一人です。"))
    nodes.append(sp())
    nodes.append(p("私が育った環境では、お年玉をもらったら将来のために貯金をしておくのが当たり前でした。だから今でも、貯金がまったくない状態や、借金がある状態を想像すると、ぞわっとした恐怖に近い感覚が湧いてきます。"))
    nodes.append(sp())
    nodes.append(p("でも、知人の中には、今月の携帯代が払えるかどうかわからない状況でも、「まあなんとかなるっしょ」と笑いながら遊びに出かける人がいます。それくらい、人によって「大丈夫」の基準はまったく違うんですよね。どちらが正しいという話ではなく、それぞれが育った環境で学習した、ただの前提の違いなんです。"))
    nodes.append(sp())

    nodes.extend(section("対処法は、まず「言い換え」から"))
    nodes.append(sp())
    nodes.append(p("じゃあどうすればいいのか。答えはシンプルで、日頃使っている言葉を、少しずつ言い換えていくことです。"))
    nodes.append(sp())
    nodes.append(p("とはいえ、「めんどくさい」が口癖になっている人にいきなり「楽勝!」「余裕!」と言ってもらおうとすると、抵抗を感じる方が多いんです。無理もありません、今までの自分と違いすぎますから。"))
    nodes.append(sp())
    nodes.append(p_bold("そういうときは、少しだけ和らげた言葉から始めてみてください。「たぶん大丈夫」「きっと大丈夫」「ちょっと余裕かも」「意外と大丈夫かもしれない」「思ったより余裕ありそう」——このくらいの温度感なら、抵抗なく口に出せるはずです。"))
    nodes.append(sp())
    nodes.append(p("これは英語や新しい言語を学ぶときの感覚に似ています。いきなりネイティブのように話そうとせず、簡単なフレーズから口に慣らしていく。婚活における言葉の練習も、それと同じでいいんです。"))
    nodes.append(sp())

    nodes.extend(section("根本から変えるなら、「これは学習しただけ」と知ること"))
    nodes.append(sp())
    nodes.append(p("行動レベルの言い換えと同時に、もう一段深いところでやってほしいことがあります。それは、「めんどくさい」「しんどい」「大変」という言葉が、真実でも事実でもなく、過去に学習した前提にすぎないと知っておくことです。"))
    nodes.append(sp())
    nodes.append(p("〇〇はしんどいものだ、と思い込んでいる〇〇の部分に、人間関係が入っているかもしれませんし、コミュニケーションが入っているかもしれません。人に気持ちを伝えることかもしれませんし、誰かと一緒に生活することかもしれません。お母さん、お父さん、家族、結婚生活、夫婦生活、嫁姑関係、親戚付き合い、お正月という行事——人によって、当てはまるものは様々です。"))
    nodes.append(sp())
    nodes.append(p_bold("でも、それはあなたが選んで身につけた真実ではなく、周りにいた人たちの口癖を、無自覚にそのまま引き継いだだけのものなんです。だとしたら、意識的に別の言葉を選び直すことは、誰にでもできます。"))
    nodes.append(sp())

    nodes.extend(section("婚活の場面で、言葉を変えてみると"))
    nodes.append(sp())
    nodes.append(p("婚活の場面に当てはめてみましょう。"))
    nodes.append(sp())
    nodes.append(p("お見合いの前、「緊張する、しんどいな」とつぶやく代わりに、「まあ、なんとかなるかも」とつぶやいてみる。連絡のやり取りが続かなくて不安なとき、「もうめんどくさい、無理」の前に、「意外とこのままいけるかもしれない」を挟んでみる。相手の家族に挨拶する日が近づいて、「大変そう」が浮かんできたら、「思ったより気楽かもしれない」と言い添えてみる。"))
    nodes.append(sp())
    nodes.append(p_bold("言葉が変わると、拾う情報が変わります。拾う情報が変わると、見える景色が変わります。景色が変わると、婚活そのものへの構え方が、ふっと軽くなっていくんです。"))
    nodes.append(sp())

    if url3:
        nodes.append(image_node(url3, "「大変そう」から「楽勝かも」へ"))
        nodes.append(sp())

    nodes.extend(section("希望への着地——言葉が変わった先にある日常"))
    nodes.append(sp())
    nodes.append(p("この練習を続けていくと、変わるのは口癖だけではありません。"))
    nodes.append(sp())
    nodes.append(p("義理の家族との顔合わせの帰り道、「思ったより楽しかったね」と二人で笑い合える日が来ます。お正月の準備で忙しいはずなのに、「なんかこれ、楽勝じゃない?」とパートナーと軽口を叩きながら台所に立てる日が来ます。携帯代の引き落とし日が近づいても、「まあ、なんとかなるっしょ」と言いながら、隣で笑っている人がいる日が来ます。"))
    nodes.append(sp())
    nodes.append(p("しんどい、めんどくさい、大変——その言葉の代わりに、楽勝、余裕、なんとかなる、を選び続けた先には、そういう小さな日常が待っています。じんわり、でも確かに、景色が変わっていくんです。"))
    nodes.append(sp())

    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日から3日間だけ、「しんどい」「めんどくさい」「大変」と言いそうになったら、そのあとに小さくひとこと付け足してみてください。「——でも、たぶん大丈夫」。それだけで十分です。"))
    nodes.append(sp())

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


def update_cover(post_id, cover_url):
    file_id = cover_url.split("/media/")[-1] if "/media/" in cover_url else cover_url
    body = {
        "draftPost": {
            "media": {
                "wixMedia": {
                    "image": {
                        "id": file_id,
                        "url": cover_url,
                    }
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
        print(f"カバー画像PATCH失敗: {r.status_code} {r.text[:300]}")
    return r.ok


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


def update_seo(post_id):
    body = {
        "draftPost": {
            "seoData": {
                "tags": [{
                    "type": "meta",
                    "props": {"name": "description", "content": SEO_DESC},
                    "children": ""
                }]
            }
        },
        "fieldMask": "seoData"
    }
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{post_id}",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"seoData PATCH失敗: {r.status_code} {r.text[:300]}")
    return r.ok


def create_tag(label):
    r = requests.post(
        f"{WIX_BASE}/blog/v3/tags",
        headers=wix_headers(),
        json={"label": label},
        timeout=30,
    )
    if not r.ok:
        print(f"タグ作成失敗 ({label}): {r.status_code} {r.text[:200]}")
        return None
    tag_id = r.json().get("tag", {}).get("id")
    print(f"  新規タグ作成: {label} → {tag_id}")
    return tag_id


def main():
    print("=== 「楽勝」が口癖になった人から、婚活はうまくいく 投稿スクリプト ===\n")

    print("[タグ作成中...]")
    new_tag = create_tag("口癖")
    if new_tag:
        TAG_IDS.append(new_tag)

    urls = []
    for img in IMAGE_PROMPTS:
        url = generate_and_upload_image(img["prompt"], img["filename"])
        urls.append(url)

    url1, url2, url3 = urls[0], urls[1], urls[2]

    print("\n[richContent構築中...]")
    rich_content = build_nodes(url1, url2, url3)

    print("\n[Wix下書き作成中...]")
    post_id = create_draft(rich_content)
    if not post_id:
        print("失敗。終了します。")
        return

    print(f"  → 下書きID: {post_id}")

    if url1:
        print("\n[カバー画像を設定中...]")
        ok = update_cover(post_id, url1)
        print(f"  → {'成功' if ok else '失敗'}")

    print("\n[excerpt・関連記事を更新中...]")
    ok = update_excerpt_related(post_id)
    print(f"  → {'成功' if ok else '失敗'}")

    print("\n[SEO descriptionを更新中...]")
    ok = update_seo(post_id)
    print(f"  → {'成功' if ok else '失敗'}")

    print(f"\n完了。下書きID: {post_id}")
    print("Wixブログ管理画面で確認してください。")
    print("画像が正しく表示されているか、必ず確認をお願いします。")


if __name__ == "__main__":
    main()
