"""
【男性向け】"弱音を吐けない"をやめた男性から、家庭は安定していく。
カテゴリ: 真剣交際（5414dab5-ded7-4b15-a88a-d679d6fd3c71）
下書き保存のみ（公開日時未定）
"""
import os, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["5414dab5-ded7-4b15-a88a-d679d6fd3c71"]  # 真剣交際

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "0ddde006-b527-4852-8056-8cdb87174e82",  # 真剣交際
    "c249fe67-ef22-410a-a395-309db2116a0b",  # 結婚
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "403b3ca5-a5d4-4628-930d-def9e17625f2",  # 男性の自信
]

RELATED_POST_IDS = [
    "c24ea7ec-7798-4cb9-a240-cf0ee30cd479",  # 仮交際→真剣交際のドキドキが怖いあなたへ
    "3ffbacad-ee5c-4751-974d-a081fead88f7",  # 彼女のご両親に挨拶へ行く男性へ
    "8b815244-5096-4f80-8dac-e0b0545a03f4",  # 夫婦の中に「3人の自分」がいる
]

TITLE   = '【男性向け】"弱音を吐けない"をやめた男性から、家庭は安定していく。'
EXCERPT = "「弱音を吐いたら情けない」——そう思って一人で抱え込んでいませんか。それ、性格じゃなくて反応パターンなんです。愛媛・松山の結婚相談所が伝える、\"支える人\"が支えられてもいい理由。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "Japanese man in his 30s, neat business casual, sitting alone at a kitchen table late at night, "
            "thoughtful contemplative expression looking down at a cup of coffee, warm lamp light, "
            "quiet reflective mood, clean modern room, "
            "shallow depth of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-06_yowane_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "Japanese couple in their 30s, sitting close together on a sofa at home, "
            "man speaking with a slightly vulnerable open expression, woman listening warmly and attentively, "
            "facing each other, clean bright modern living room, "
            "shallow depth of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-06_yowane_disclosure.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft evening lighting, East Asian appearance, "
            "beautiful Japanese woman with elegant refined features, model-like appearance, clear skin, "
            "Japanese man and woman in their 30s, sitting together at a kitchen table looking at a notebook "
            "and calculator together, relaxed collaborative atmosphere, gentle smiles, "
            "clean bright modern kitchen, shallow depth of field, "
            "professional lifestyle photography, no text"
        ),
        "filename": "2026-07-06_yowane_hope.png",
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

    nodes.append(p("今日は、婚活中の男性会員さんから本当によく聞く話をしたいんです。"))
    nodes.append(sp())
    nodes.append(p("「将来、家族を養えるだろうか」「自分が支えなきゃいけないのに、こんな不安を口にしていいんだろうか」——真剣交際が進めば進むほど、こういう気持ちが強くなる方、多いんですよね。"))
    nodes.append(sp())
    nodes.append(p("面白いのは、この不安、口には出さないんです。パートナーにも、友人にも。私にだけ、ぽつりと漏らしてくれる。「情けないから言えなくて」って。"))
    nodes.append(sp())
    nodes.append(p("結論から言いますね。それ、あなたの器が小さいからでも、頼りなさのサインでもありません。"))
    nodes.append(sp())

    if url1:
        nodes.append(image_node(url1, "一人で抱えることは、頑張りの証じゃない。"))
        nodes.append(sp())

    nodes.extend(section("不安は「性格」じゃなくて「反応パターン」"))
    nodes.append(sp())
    nodes.append(p("右利きの人が左手で箸を持つと不自由に感じるように、私たちには長年かけて身についた「慣れた反応の仕方」があります。"))
    nodes.append(sp())
    nodes.append(p_bold("「弱音を吐かない」「一人で抱え込む」というのも、実はその人の性格じゃなくて、反応パターンのひとつなんです。"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("彼女に将来のお金の話を振られると、なんとなく話をそらしてしまう。仕事の悩みを聞かれても「大丈夫、大丈夫」で終わらせてしまう。本当は不安なのに、それを認めたら\"男として終わり\"な気がしてしまう。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話、きっと楽になります。"))
    nodes.append(sp())

    nodes.extend(section("なぜ男性は「一人で抱える」を選びがちなのか"))
    nodes.append(sp())
    nodes.append(p("社会学の世界には「覇権的男性性」という考え方があります。社会学者コンネルが提唱したもので、簡単に言うと「男性は強くあるべき、弱さを見せてはいけない、経済的に一家を支えるべき」という規範が、社会の中でずっと\"標準\"として扱われてきた、という指摘です。"))
    nodes.append(sp())
    nodes.append(p("これ自体は誰かが悪いわけじゃなくて、私たちがそう育てられ、そう学習してきた文化的な癖なんですよね。"))
    nodes.append(sp())
    nodes.append(p("心理学の分野では、感情をうまく言葉にできない、あるいは言葉にすることを避ける傾向を「アレキシサイミア(失感情症)」的な傾向と呼ぶことがあります。これは病気ではなく、多くの場合「感情を出すな」と教えられて育った結果、感情を扱う練習の機会が単純に少なかっただけなんです。"))
    nodes.append(sp())
    nodes.append(p_bold("つまり、「弱音を吐けない」のも「一人で抱え込む」のも、あなたの弱さじゃなくて、練習不足の反応パターン。だったら、練習すれば変えられます。"))
    nodes.append(sp())

    nodes.extend(section("抱え込むことの、見えないコスト"))
    nodes.append(sp())
    nodes.append(p("ここでちょっと、体の話もさせてください。"))
    nodes.append(sp())
    nodes.append(p("心身の健康の研究分野では、感情や悩みを表に出さずに抱え込み続けることが、慢性的なストレス反応につながり、免疫機能や心血管の健康にまで影響することがわかっています。孤立や孤独が健康リスクを高めるという大規模な研究(ホルト=ランスタッドら)もあるくらいです。"))
    nodes.append(sp())
    nodes.append(p("つまり「一人で抱える」は、精神論の話だけじゃなくて、実際に体にも負担がかかっている状態なんですよね。頑張り屋の男性ほど、これに気づかないまま無理を重ねてしまいます。"))
    nodes.append(sp())

    if url2:
        nodes.append(image_node(url2, "一つ話すだけで、支え合いは始まる。"))
        nodes.append(sp())

    nodes.extend(section("「支える人」も、支えられていい"))
    nodes.append(sp())
    nodes.append(p("ここで、婚活中・交際中にできる具体的な一歩の話をしますね。"))
    nodes.append(sp())
    nodes.append(p("まず、あなたが一人で抱えている気がかりを、紙に書き出してみてください。お金のこと、仕事のこと、将来の親の介護のこと、彼女に嫌われたくないという気持ち。全部です。"))
    nodes.append(sp())
    nodes.append(p("コミュニケーション学には「自己開示の返報性」という考え方があります。誰かが自分の内側を見せると、相手も自然と自分の内側を見せやすくなる、という現象です。あなたが弱さを一つ見せることで、彼女もまた、あなたに安心して寄りかかれるようになる。支え合うというのは、本来そういうものなんですよね。"))
    nodes.append(sp())
    nodes.append(p("ただ、ひとつだけ大事な注意点があります。結婚相談所を通じて出会った相手は、あなたと同じように、迷いや不安を抱えていることが多いんです。真剣交際の途中で、彼女自身の気持ちがまだ固まりきっていないタイミングもあります。"))
    nodes.append(sp())
    nodes.append(p("そういうときに、あなたの不安をそのまま彼女にぶつけてしまうと、うまくいくこともあれば、逆に彼女の迷いを大きくしてしまうこともあるんですよね。"))
    nodes.append(sp())
    nodes.append(p("うちの結婚相談所には、「AI美知仲人コーチ」というLINEの相談相手もいます。夜中にふと不安になったとき、お見合い前日の夜、彼女からのLINEにどう返そうか迷ったとき——そんなときは、まずAI仲人美知に話しかけてみてください。24時間いつでも、会話は仲人を含め誰にも知られません。「こんな小さなことで」と思わなくて大丈夫です。"))
    nodes.append(sp())
    nodes.append(p_bold("そのうえで、彼女に伝えるかどうかという大事な判断は、私たち仲人と一緒に考えましょう。だからこそ、気がかりを最初に話す相手は、彼女ではなく——まずAI仲人美知、そして仲人にしてほしいんです。"))
    nodes.append(sp())
    nodes.append(p("仲人なら、彼女が今どのくらいの状態にいるかを踏まえて、「今なら話しても大丈夫」「もう少し待ったほうがいい」というタイミングを一緒に考えられます。一人で抱えなくていいというのは、いきなり彼女に全部話すという意味じゃないんです。"))
    nodes.append(sp())
    nodes.append(p("「頼りがいがある」というのは、全部を一人で背負えることではありません。本当に頼りがいがある男性は、必要なときに「実はちょっと不安なんだ」と誰かに言える男性です。"))
    nodes.append(sp())

    nodes.extend(section("その先にある、穏やかな家庭"))
    nodes.append(sp())
    nodes.append(p("想像してみてください。"))
    nodes.append(sp())
    nodes.append(p("仕事で疲れて帰ってきた夜、玄関で「今日ちょっとしんどかった」とひとこと言える。それを聞いた彼女が、何も解決してくれなくても、ただ「そうだったんだね」と隣に座ってくれる。"))
    nodes.append(sp())
    nodes.append(p("将来のお金の話も、二人で数字を見ながら「じゃあこうしていこうか」と、一人で抱えていたときよりずっと軽い気持ちで話せている。"))
    nodes.append(sp())
    nodes.append(p("その関係は、あなたが「強い自分」を演じ続けた先にあるものじゃなくて、弱さを見せてもいいと決めた先にある景色です。"))
    nodes.append(sp())

    if url3:
        nodes.append(image_node(url3, "一人で背負っていたものが、二人のものになる。"))
        nodes.append(sp())

    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、頭の中にある気がかりを一つだけ、まずAI仲人美知に話しかけるか、私たち仲人に話してみてください。彼女に直接伝えるかどうか、どう伝えるかは、そのあとで一緒に考えればいいんです。一人で抱え込まなくていい、という最初の一歩は、そこから始まります。"))
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


def main():
    print("=== 弱音を吐けないをやめた男性から家庭は安定していく 投稿スクリプト ===\n")

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
