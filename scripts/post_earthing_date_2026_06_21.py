"""
カフェよりも、裸足の海辺で距離が縮まる。婚活デートに"アーシング"のすすめ。
カテゴリ: 仮交際（3f5f378d-a4f4-47e0-90a7-ab4daa27504e）
公開予定: 下書き保存のみ
"""
import os, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["3f5f378d-a4f4-47e0-90a7-ab4daa27504e"]

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "1c7a4d95-e95b-492a-93e2-da1c8a63ab9b",  # デート
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    "5b192801-25d6-4067-98d5-c7405fc91d17",  # 松山市
    "3a325f22-036a-4027-bb73-c77a217c2dc5",  # アーシング
    "f9b538ec-747a-48d0-9165-8295a8c2ed3a",  # 自律神経
]

RELATED_POST_IDS = [
    "78d9e1c5-9567-4c4c-a7d8-9b318a131ee9",  # 「どこ行こうか」から、ふたりは始まる
    "105946cf-1d0c-4385-97d2-c8158b3c76e5",  # 食べるものが、関係性を変える
    "0c004668-d23a-40d3-a971-385f8dc6d799",  # 結婚してから、自分がどんどん好きになっていった
]

TITLE   = 'カフェよりも、裸足の海辺で距離が縮まる。婚活デートに"アーシング"のすすめ。'
EXCERPT = "婚活デートはいつもカフェやレストランで向かい合い。緊張して疲れていませんか？松山市の梅津寺海岸で体験した「アーシング」が、心も体もゆるむ新しいデートの形でした。横並びで海を見ながら、自然と心の距離が縮まる理由を、心理カウンセラー仲人がお伝えします。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian couple in their 30s, "
            "beautiful Japanese woman with elegant refined features and model-like appearance, clear skin, "
            "handsome Japanese man in casual summer outfit, "
            "walking barefoot together on a sandy beach at sunset, relaxed happy expressions, "
            "waves gently touching their feet, summer sky with soft clouds, "
            "side by side walking, natural romantic atmosphere, "
            "shallow depth of field, clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-21_earthing_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian couple in their 30s, "
            "beautiful Japanese woman with elegant refined features, model-like appearance, clear skin, "
            "couple sitting side by side on a beach mat on sand, "
            "holding takeaway coffee cups, looking at the calm sea together, "
            "relaxed casual summer clothes, parasol providing shade, "
            "peaceful serene beach atmosphere, shallow depth of field, "
            "clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-21_earthing_couple_beach.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, "
            "close-up of bare feet on wet sand at the shoreline, "
            "gentle waves washing over toes, pink healthy skin, "
            "natural beach setting, summer day, "
            "grounding earthing wellness concept, "
            "shallow depth of field, clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-21_earthing_feet.png",
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


def build_nodes(url_eyecatch, url_couple, url_feet):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # 導入
    nodes.append(p("婚活のデートって、カフェやレストランが多くないですか。"))
    nodes.append(sp())
    nodes.append(p("向かい合って座って、メニューを選んで、何を話そうかなって考えて。"))
    nodes.append(sp())
    nodes.append(p("それで相手の表情がちょっと曇ったかなと思うと、自分の話す内容が変わっていく。"))
    nodes.append(sp())
    nodes.append(p("意識していなくても、相手のリアクションひとつひとつに合わせて、気に沿うような言葉を選んでしまう。"))
    nodes.append(sp())
    nodes.append(p("無意識にそうなるんですよね。"))
    nodes.append(sp())
    nodes.append(p("結果として、帰り道にどっと疲れてしまう。"))
    nodes.append(sp())
    nodes.append(p("心理学ではこの状態を「印象管理（Impression Management）」と呼びます。"))
    nodes.append(sp())
    nodes.append(p('社会学者ゴッフマンの理論で、人は他者の前では常に"舞台に立っている"感覚で振る舞うとされています。'))
    nodes.append(sp())
    nodes.append(p('カフェの向かい合わせの席って、まさにその"舞台"なんですよね。'))
    nodes.append(sp())
    nodes.append(p("でもね、それとはまったく違うデートの形があるんです。"))
    nodes.append(sp())

    if url_eyecatch:
        nodes.append(image_node(url_eyecatch, "裸足の海辺で、いつもと違うデートを"))
        nodes.append(sp())

    # セクション1: アーシングデート
    nodes.extend(section('裸足で砂浜を歩く、"アーシング"デート'))
    nodes.append(sp())
    nodes.append(p("先日、松山市の梅津寺海岸で「ココカラダイガク」というコミュニティのイベントに参加してきたんです。"))
    nodes.append(sp())
    nodes.append(p("砂浜を裸足で歩いたり、波打ち際に足をつっこんだり、地面の中に足を潜らせてみたり。"))
    nodes.append(sp())
    nodes.append(p("おしゃべりしながら歩いたかと思えば、ゴロゴロ寝転んだり、砂に絵を描いたり、泥だんごを作ったり（笑）"))
    nodes.append(sp())
    nodes.append(p("「え、デートでそれ？」って思いましたよね。"))
    nodes.append(sp())
    nodes.append(p("でも、これが本当によかったんです。"))
    nodes.append(sp())

    # セクション2: アーシングとは
    nodes.extend(section("アーシングって、なに？"))
    nodes.append(sp())
    nodes.append(p("アーシング（Earthing/Grounding）は、裸足で大地に直接触れることで、体内に溜まった静電気や余分な電荷を放出する健康法です。"))
    nodes.append(sp())
    nodes.append(p("普段私たちは靴やコンクリートの上で暮らしていて、地球の表面にある自由電子を受け取れない状態になっています。"))
    nodes.append(sp())
    nodes.append(p("裸足で砂浜や土の上に立つと、大地の自由電子が体に入ってきて、体内の活性酸素を中和してくれると言われています。"))
    nodes.append(sp())
    nodes.append(p("神経科学の観点から言えば、アーシングは副交感神経（リラックスを司る神経）を優位にして、コルチゾール（ストレスホルモン）の分泌を整える効果が報告されています。"))
    nodes.append(sp())
    nodes.append(p("つまり、ただ裸足で砂浜にいるだけで、体が自然とリラックスモードに切り替わっていくわけです。"))
    nodes.append(sp())

    if url_feet:
        nodes.append(image_node(url_feet, "裸足で波打ち際に立つだけで、体が変わっていく"))
        nodes.append(sp())

    # セクション3: 私の体で起きたこと
    nodes.extend(section("私の体で起きたこと"))
    nodes.append(sp())
    nodes.append(p("私の場合、アーシングを始めて20分くらいで足の色がピンク色に変わってきました。"))
    nodes.append(sp())
    nodes.append(p("「あ、すごくあったまってるな」って体で感じたんですよね。"))
    nodes.append(sp())
    nodes.append(p("汗も出てきて、血流が明らかに変わったのがわかりました。"))
    nodes.append(sp())
    nodes.append(p("90分ほど続けた後の体の軽さといったら、もう全然違いました。"))
    nodes.append(sp())
    nodes.append(p("そしてね、一番驚いたのはその日の夜。"))
    nodes.append(sp())
    nodes.append(p_bold("朝までぐっすり眠れたんです。"))
    nodes.append(sp())
    nodes.append(p("普段はどうしても途中で目が覚めることがあるのに、アーシングした夜はそれがなかった。"))
    nodes.append(sp())
    nodes.append(p("自律神経が整うと、血流・消化・ホルモン分泌・睡眠など、体のあらゆる調整機能が本来のリズムを取り戻すんです。"))
    nodes.append(sp())
    nodes.append(p("婚活って、知らず知らずのうちに緊張やストレスが体に溜まっていきます。"))
    nodes.append(sp())
    nodes.append(p("その「なんとなくの疲れ」「なんとなくのだるさ」が、実は婚活の判断力やモチベーションにも影響しているかもしれない。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、体のメンテナンスとしてのアーシング、すごくおすすめです。"))
    nodes.append(sp())

    # セクション4: 横並びの心理学的効果
    nodes.extend(section("横並びだから、心の内が話せる"))
    nodes.append(sp())
    nodes.append(p("そしてね、アーシングデートの一番の魅力は「向かい合わなくていい」ということなんです。"))
    nodes.append(sp())
    nodes.append(p("砂浜を並んで歩く。海を見ながらぼーっとする。"))
    nodes.append(sp())
    nodes.append(p("これ、コミュニケーション学では「サイド・バイ・サイド（横並び）コミュニケーション」と言って、心理的な安全性が高い対話の形とされています。"))
    nodes.append(sp())
    nodes.append(p("向かい合って話すと、相手の目や表情が常に視界に入るので、無意識に「どう見られているか」を気にしてしまう。"))
    nodes.append(sp())
    nodes.append(p("でも横並びだと、視線は自然に前方の景色に向くので、自分の内側の言葉が出やすくなるんです。"))
    nodes.append(sp())
    nodes.append(p("車の中で深い話ができた経験、ありませんか？"))
    nodes.append(sp())
    nodes.append(p("あれと同じ原理です。"))
    nodes.append(sp())

    if url_couple:
        nodes.append(image_node(url_couple, "横並びで海を見るだけで、距離が縮まる"))
        nodes.append(sp())

    nodes.append(p("心理学の研究でも、横並びの配置は対面に比べて自己開示（本音を話すこと）が増えるとされています。"))
    nodes.append(sp())
    nodes.append(p("言葉を交わさなくても、同じ景色を見て、同じ波の音を聞いている。"))
    nodes.append(sp())
    nodes.append(p("それだけでペーシング（相手と呼吸やリズムを合わせること）が自然に起きて、距離が縮まっていく。"))
    nodes.append(sp())
    nodes.append(p("実はこれ、NLPでいう「ラポール形成」の最も自然な形なんですよね。"))
    nodes.append(sp())

    # セクション5: 男性へのアドバイス
    nodes.extend(section("男性へ。こっそり差がつくポイント"))
    nodes.append(sp())
    nodes.append(p("「砂浜デートって何を準備したらいいの？」って思った男性の方へ。"))
    nodes.append(sp())
    nodes.append(p("実はこのデート、ちょっとした気配りで大きくポイントが上がるんです。"))
    nodes.append(sp())
    nodes.append(p("レジャーシートは百均で買えます。これだけでも「あ、ちゃんと考えてくれたんだ」と思ってもらえます。"))
    nodes.append(sp())
    nodes.append(p("梅津寺海岸なら近くにカフェもありますから、「何か飲む？買ってくるよ」とさっと動けると、それだけで気遣いが伝わります。"))
    nodes.append(sp())
    nodes.append(p("手拭きや足拭きシート、汗を拭くタオル。"))
    nodes.append(sp())
    nodes.append(p('こういう"相手が必要としそうなもの"をさりげなく持っていけるかどうかが、カフェでは見えなかった魅力を見せるチャンスになります。'))
    nodes.append(sp())
    nodes.append(p("もしパラソルをお持ちなら、砂浜に刺してあげるのも素敵ですよね。"))
    nodes.append(sp())
    nodes.append(p("レストランのスマートな立ち居振る舞いより、こういう場面での自然な気遣いの方が、相手の記憶に残るものです。"))
    nodes.append(sp())

    # セクション6: 松山ローカル情報
    nodes.extend(section("松山にいるなら、梅津寺海岸へ"))
    nodes.append(sp())
    nodes.append(p("梅津寺海岸は、松山市内から伊予鉄で気軽に行ける砂浜です。"))
    nodes.append(sp())
    nodes.append(p("駅を降りたらすぐ目の前に海が広がっていて、この景色だけでも気持ちがふわっとゆるみます。"))
    nodes.append(sp())
    nodes.append(p("静かな波、対岸の山々、伊予鉄のオレンジの電車が通る風景。"))
    nodes.append(sp())
    nodes.append(p("「デートの行き先」としてはちょっと意外かもしれないけれど、だからこそ新鮮で、だからこそ心に残る。"))
    nodes.append(sp())

    # 希望への着地
    nodes.append(p("婚活に疲れてきたなと感じたとき。"))
    nodes.append(sp())
    nodes.append(p("次のデートどうしようって悩んでいるとき。"))
    nodes.append(sp())
    nodes.append(p("靴を脱いで、砂浜に立ってみてください。"))
    nodes.append(sp())
    nodes.append(p("大地が、あなたの緊張もストレスも、静かに受け取ってくれますから。"))
    nodes.append(sp())
    nodes.append(p("そしてふたり並んで、同じ海を見ている——その時間が、言葉よりも深いところでふたりをつないでくれます。"))
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


def main():
    print("=== アーシングデート記事 投稿スクリプト ===\n")

    # 1. 画像生成＆アップロード
    urls = []
    for img in IMAGE_PROMPTS:
        url = generate_and_upload_image(img["prompt"], img["filename"])
        urls.append(url)

    url_eyecatch = urls[0]
    url_couple   = urls[1]
    url_feet     = urls[2]

    # 2. richContent構築
    print("\n[richContent構築中...]")
    rich_content = build_nodes(url_eyecatch, url_couple, url_feet)

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

    # 5. SEO descriptionを更新
    print("\n[SEO descriptionを更新中...]")
    ok = update_seo(post_id)
    print(f"  → {'成功' if ok else '失敗'}")

    print(f"\n完了！\n下書きID: {post_id}")
    print("Wixブログ管理画面で確認してください。")
    print("⚠️ 画像が正しく表示されているか、必ず確認をお願いします。")


if __name__ == "__main__":
    main()
