"""
【男性向け】デートでファミレスに連れて行っていませんか？ 女性が見ているのは、料理じゃなくて"気持ち"です。
カテゴリ: 恋愛経験が少ない人の婚活（69d23361-4fe7-4af6-a69e-2276e1f08417）
公開予定: 2026-06-19（木）下書き保存のみ
"""
import os, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["69d23361-4fe7-4af6-a69e-2276e1f08417"]

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "1c7a4d95-e95b-492a-93e2-da1c8a63ab9b",  # デート
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "021e7932-59b1-43ae-9c76-4b00cd73b587",  # 好印象
]

RELATED_POST_IDS = [
    "d82eba55-ad05-41f3-b558-a17ab1646c52",  # 優しいのに選ばれない男性の減点行動
    "78d9e1c5-9567-4c4c-a7d8-9b318a131ee9",  # 「どこ行こうか」から、ふたりは始まる
    "8dc13d85-b85f-4247-8a8b-8ed90bad6bdc",  # 媚びるな、危険
]

TITLE   = '【男性向け】デートでファミレスに連れて行っていませんか？ 女性が見ているのは、料理じゃなくて"気持ち"です。'
EXCERPT = "仮交際中のデートでファミレスを選んでいませんか？悪気がないのはわかります。でも女性はその選択から「私のことどうでもいいのかな」と連想してしまう。仲人・心理カウンセラー中嶋美知が、女性のリアルな気持ちを正直にお伝えします。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian couple in their 30s, "
            "beautiful Japanese woman with elegant refined features and model-like appearance, "
            "man in neat dark casual jacket, sitting at a charming small Italian restaurant "
            "with warm ambient lighting, woman smiling brightly looking impressed, "
            "cozy intimate atmosphere, shallow depth of field, "
            "clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-19_famires_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman with elegant refined features, model-like appearance, clear skin, "
            "two women friends having lunch at a stylish modern cafe, "
            "beautifully plated food on the table, women laughing and enjoying conversation, "
            "bright airy interior with plants, shallow depth of field, "
            "clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-19_famires_women_lunch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian man in his 30s, "
            "neat casual outfit, looking at his smartphone screen browsing restaurant options, "
            "sitting at a desk in a bright clean room, focused and determined expression, "
            "modern minimalist interior, shallow depth of field, "
            "clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-19_famires_man_searching.png",
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


def build_nodes(url_eyecatch, url_women, url_man):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # 導入
    nodes.append(p("今日はね、ちょっと辛口です。"))
    nodes.append(sp())
    nodes.append(p("でも、これを知っているか知らないかで婚活の結果が変わるかもしれないので、正直にお話しします。"))
    nodes.append(sp())
    nodes.append(p_bold("テーマは、デートでファミレスに連れて行っていませんか？ です。"))
    nodes.append(sp())

    if url_eyecatch:
        nodes.append(image_node(url_eyecatch, '「あなたのために選んだよ」が伝わるお店へ'))
        nodes.append(sp())

    # セクション1: はっきり言います
    nodes.extend(section('まず、はっきり言います'))
    nodes.append(sp())
    nodes.append(p('女性慣れしていない男性、女性とお付き合いした経験がない男性、男子校で育って周りに女性がいなかった男性——女性がどういうことで喜ぶか、わかっていないんじゃないかなと思うことがあるんです。'))
    nodes.append(sp())
    nodes.append(p('女性の生態がわからない。'))
    nodes.append(sp())
    nodes.append(p('それはね、悪いことじゃないんですよ。経験がなければ知らなくて当然です。'))
    nodes.append(sp())
    nodes.append(p_bold('だけど、知らないなら仲人に聞いてください。'))
    nodes.append(sp())
    nodes.append(p('女性に慣れていないなら、仲人に聞いてください。'))
    nodes.append(sp())
    nodes.append(p('お付き合いしたことがないなら、仲人に聞いてください。'))
    nodes.append(sp())
    nodes.append(p('聞くことは恥ずかしいことじゃないんです。聞かないまま失敗するほうが、ずっともったいない。'))
    nodes.append(sp())

    # セクション2: 未婚女性の頭の中
    nodes.extend(section('未婚女性の頭の中に「ファミレス」はない'))
    nodes.append(sp())
    nodes.append(p('まず前提をお伝えしますね。'))
    nodes.append(sp())
    nodes.append(p_bold('未婚の女性が、女友達同士で「ランチ行こう」「夜ごはん食べに行こう」となったとき、ファミレスを提案する女性は、まずいません。'))
    nodes.append(sp())
    nodes.append(p('なぜだと思いますか。'))
    nodes.append(sp())
    nodes.append(p('女性は、女性同士であっても——おしゃべりがしたい、おいしいものが食べたい、映える料理が見たい、噂になっている人気のお店が気になる、ロケーションが良い場所に友達を連れて行ってあげたい、食器や内装が素敵なお店が好き……そういう感覚があるんですよね。'))
    nodes.append(sp())
    nodes.append(p('友達同士で「このお店いいよね」「ここ素敵だね」って言い合える場所に行きたい。'))
    nodes.append(sp())
    nodes.append(p('これが、女性にとっての「食事に行く」のベースラインです。'))
    nodes.append(sp())
    nodes.append(p('ファミレスをけなしているわけじゃないんです。ただ、未婚女性が求めているものが、ファミレスにはほぼ揃っていないんですよね。'))
    nodes.append(sp())

    if url_women:
        nodes.append(image_node(url_women, '女性にとって「食事に行く」のベースライン'))
        nodes.append(sp())

    # セクション3: ファミリーレストランの本質
    nodes.extend(section('ファミレスは「ファミリー」のためのレストラン'))
    nodes.append(sp())
    nodes.append(p('ファミレスの椅子って、隣に小さなお子さんを安心して座らせておけるように設計されています。'))
    nodes.append(sp())
    nodes.append(p('ドリンクバーで子どもたちが気兼ねなくジュースを取りに行ける。'))
    nodes.append(sp())
    nodes.append(p('食器も高価なものじゃないから、万が一落としても大丈夫。'))
    nodes.append(sp())
    nodes.append(p('周りに気を使わずに過ごせるように、レイアウトもお食事の内容もファミリー向けに配慮されている。'))
    nodes.append(sp())
    nodes.append(p_bold('だからこそ、ファミリーレストランなんです。'))
    nodes.append(sp())
    nodes.append(p('家族ができて、お子さんが小さいうちは、ファミレスはほんとうにありがたい場所です。'))
    nodes.append(sp())
    nodes.append(p('でも、仮交際中のデートと、家族でのお食事では——目的も用途も、まるっきり違うんですよね。'))
    nodes.append(sp())

    # セクション4: 女性の頭の中で起きること（ミニ診断含む）
    nodes.extend(section('女性の頭の中で起きること'))
    nodes.append(sp())
    nodes.append(p('こんなこと、思い当たることはありませんか。'))
    nodes.append(sp())
    nodes.append(p('デートの食事は「安さ」「近さ」「入りやすさ」で選んでいる。'))
    nodes.append(sp())
    nodes.append(p('彼女が何を食べたいか、聞いたことがない。'))
    nodes.append(sp())
    nodes.append(p('「どこでもいいよ」と言われたら、本当にどこでもいいんだと思っている。'))
    nodes.append(sp())
    nodes.append(p('——どれか一つでも心当たりがあれば、ちょっとだけ立ち止まって読んでみてください。'))
    nodes.append(sp())
    nodes.append(p('女性はね、デートでワクワクしたいんです。'))
    nodes.append(sp())
    nodes.append(p('「どんなところに連れて行ってくれるのかなぁ」って、楽しみにしているんですよね。'))
    nodes.append(sp())
    nodes.append(p('その気持ちの奥には、さっき話した「おいしさ」「見た目」「ときめき」が前提としてあるから、正直なところファミレスだと——「この人、私を楽しませようとは思ってくれていないのかな」って考えちゃうんです。'))
    nodes.append(sp())
    nodes.append(p('で、「楽しませようと思ってくれていない」ということは、「私のことどうでもいいのかな」って連想してしまう。'))
    nodes.append(sp())
    nodes.append(p('さらに——これがずっと続くのかな。デリカシーがないのかな。記念日もファミレスなのかな。家族のためにお金を使えない人なのかな。自分のことしか考えていない人なのかな。'))
    nodes.append(sp())
    nodes.append(p('……なんて考えが、どんどん広がっちゃうんですよね。'))
    nodes.append(sp())

    # セクション5: なぜそこまで考えが飛ぶのか
    nodes.extend(section('なぜそこまで考えが飛ぶのか'))
    nodes.append(sp())
    nodes.append(p('ここは脳のしくみの話なんですが、人間の脳は情報の空白を埋めたがる性質を持っています。'))
    nodes.append(sp())
    nodes.append(p('認知心理学では「補完バイアス」と呼ばれるものに近いのですが、データがないとき、人は想像や推測で空白を埋めようとするんです。'))
    nodes.append(sp())
    nodes.append(p('ファミレスのデートは、多くの未婚女性にとって完全な想定外なんですよね。'))
    nodes.append(sp())
    nodes.append(p('想定外ということは、経験値がない。経験値がないということは、データがない。データがないということは——空白を埋めるしかない。'))
    nodes.append(sp())
    nodes.append(p_bold('そして大抵の場合、人は空白を不安や悪い想像で埋めるんです。'))
    nodes.append(sp())
    nodes.append(p('「きっと無頓着な人なんだ」「私のことを大事に思っていないんだ」「この先ずっとこうなんだ」——実際には何一つ確認していないのに、脳が勝手にストーリーを作ってしまう。'))
    nodes.append(sp())
    nodes.append(p('男性に悪気がないことは、よく存じています。'))
    nodes.append(sp())
    nodes.append(p('でも、悪気がなくても伝わり方はコントロールできるんですよね。知らなかっただけなら、今日から変えればいいんです。'))
    nodes.append(sp())

    # セクション6: もったいない
    nodes.extend(section('こんなことで、もったいない'))
    nodes.append(sp())
    nodes.append(p('こんなこと言うとね、「ファミレス好きの女性だっているじゃないか」って思う方もいらっしゃるかもしれません。'))
    nodes.append(sp())
    nodes.append(p('もちろんです。'))
    nodes.append(sp())
    nodes.append(p('男性が好きな牛丼屋さん、ラーメン屋さん、賂やかな居酒屋さんが好きな女性もいて、喜んでくれることもありますよ。'))
    nodes.append(sp())
    nodes.append(p('だけど、いつもいつもそれだと——ちょっとどうかなぁと思うんです。'))
    nodes.append(sp())
    nodes.append(p('男性もそうだと思うけれど、女性も「1人で生きるよりも、2人のほうがもっと幸せで、もっと楽しくなる。今より素敵に輝く時間がある」って信じているから、婚活をしているんです。'))
    nodes.append(sp())
    nodes.append(p('正直に言ってしまうと、ランチや晩ごはんがファミレスだと、1人でいるときよりも輝きがちょっと小さくなっちゃうような気がするの。'))
    nodes.append(sp())
    nodes.append(p('こんなことで「この人は違うな」と思われてしまうのは、ほんとうにもったいないですよね。'))
    nodes.append(sp())

    # セクション7: 安くていいじゃないか
    nodes.extend(section('「安くていいじゃないか」と思う方へ'))
    nodes.append(sp())
    nodes.append(p('ファミレスは安くて助かる。駐車場も広くてありがたい。'))
    nodes.append(sp())
    nodes.append(p('その通りです。それは本当にそう。'))
    nodes.append(sp())
    nodes.append(p('でもね、ちょっと考えてみてほしいんです。'))
    nodes.append(sp())
    nodes.append(p_bold('何のために、2人で食事をするんですか？'))
    nodes.append(sp())
    nodes.append(p_bold('どうして、デートに誘うんですか？'))
    nodes.append(sp())
    nodes.append(p('彼女の笑顔が見たいからですよね。'))
    nodes.append(sp())
    nodes.append(p('彼女を幸せにして、一緒にいる自分も幸せな気持ちに満たされたいからじゃないでしょうか。'))
    nodes.append(sp())
    nodes.append(p('2人で一緒にいる幸せを味わいたいからじゃないでしょうか。'))
    nodes.append(sp())
    nodes.append(p('だったら——彼女が喜ぶ場所、女性が喜ぶ場所に連れて行ってあげて、とびきり幸せそうな彼女を見つめる時間。'))
    nodes.append(sp())
    nodes.append(p_bold('それが、デートです。'))
    nodes.append(sp())
    nodes.append(p('高いお店じゃなくてもいいんですよ。個人経営の小さなカフェでも、地元で評判のイタリアンでも、ちょっと景色のいいレストランでも。'))
    nodes.append(sp())
    nodes.append(p_bold('大事なのは金額じゃなくて、「あなたのために選んだよ」という気持ちが伝わること。'))
    nodes.append(sp())
    nodes.append(p('社会学者アーヴィング・ゴフマンの「印象管理」という考え方があるのですが、人は行動を通じて相手に「自分がどんな人か」を無意識に伝えているんです。'))
    nodes.append(sp())
    nodes.append(p('お店選びも、立派な印象管理なんですよね。'))
    nodes.append(sp())
    nodes.append(p('「あなたと過ごす時間を大事に思っています」——それが伝わるお店を選ぶだけで、彼女の中のあなたへの安心感が、ぐっと変わります。'))
    nodes.append(sp())

    if url_man:
        nodes.append(image_node(url_man, 'わからないなら、調べる。聞く。それだけで変わる'))
        nodes.append(sp())

    # セクション8: わからないなら聞いていい
    nodes.extend(section('わからないなら、聞いていい'))
    nodes.append(sp())
    nodes.append(p('右利きの人が左手でお笸を持つくらい、慣れないことは難しいものです。'))
    nodes.append(sp())
    nodes.append(p('「安くて便利な場所」を自然に選んでしまうのは、性格じゃなくてこれまでの経験値で身についた反応パターン。'))
    nodes.append(sp())
    nodes.append(p('だから、変えようと思えば変えられるんです。'))
    nodes.append(sp())
    nodes.append(p('ネットで「デート レストラン 松山」って検索してもいい。'))
    nodes.append(sp())
    nodes.append(p('食べログやGoogleマップで評価の高いお店を調べてもいい。'))
    nodes.append(sp())
    nodes.append(p_bold('そしてなにより——仲人に聞いてください。'))
    nodes.append(sp())
    nodes.append(p('「どんなお店がいいですか？」って。'))
    nodes.append(sp())
    nodes.append(p('恥ずかしいことじゃないんです。むしろ、聞ける人が一番強い。'))
    nodes.append(sp())

    # 希望への着地
    nodes.append(p('想像してみてください。'))
    nodes.append(sp())
    nodes.append(p('あなたが彼女のために選んだお店で、彼女が「わぁ、素敵！」って目を輝かせている。'))
    nodes.append(sp())
    nodes.append(p('「ここ、すごくいいね」「よく見つけたね」って言ってくれる。'))
    nodes.append(sp())
    nodes.append(p('そのとき、あなたの中にも「彼女を喜ばせることができた」っていう温かい気持ちが広がっていくはずです。'))
    nodes.append(sp())
    nodes.append(p('脳科学的にも、誰かを喜ばせたときにはオキシトシンやドーパミンが分泌されて、自分自身も幸せを感じるようにできているんですよね。'))
    nodes.append(sp())
    nodes.append(p('彼女の笑顔が、あなたの幸せになる。'))
    nodes.append(sp())
    nodes.append(p('その好循環の入口が、お店選びひとつにあるんです。'))
    nodes.append(sp())

    # 今週の一歩
    nodes.extend(section('今週の一歩'))
    nodes.append(sp())
    nodes.append(p('次のデートまでに、一つだけやってみてください。'))
    nodes.append(sp())
    nodes.append(p('「デート レストラン」で検索して、雰囲気の良さそうなお店を3つピックアップしてみる。'))
    nodes.append(sp())
    nodes.append(p('わからなかったら、仲人に「どんなお店がいいですか？」って聞く。'))
    nodes.append(sp())
    nodes.append(p('それだけで、次のデートが変わります。'))
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
    print("=== ファミレスデート記事 投稿スクリプト ===\n")

    # 1. 画像生成＆アップロード
    urls = []
    for img in IMAGE_PROMPTS:
        url = generate_and_upload_image(img["prompt"], img["filename"])
        urls.append(url)

    url_eyecatch = urls[0]
    url_women    = urls[1]
    url_man      = urls[2]

    # 2. richContent構築
    print("\n[richContent構築中...]")
    rich_content = build_nodes(url_eyecatch, url_women, url_man)

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

    print(f"\n✅ 完了！\n下書きID: {post_id}")
    print("Wixブログ管理画面で確認してください。")
    print("⚠️ 画像が正しく表示されているか、必ず確認をお願いします。")


if __name__ == "__main__":
    main()
