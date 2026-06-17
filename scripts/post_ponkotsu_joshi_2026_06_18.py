"""
【女性向け】「気がきく女子」をお休みしてみない？ ポンコツ女子のすすめ
カテゴリ: 仮交際（3f5f378d-a4f4-47e0-90a7-ab4daa27504e）
公開予定: 2026-06-18（水）下書き保存のみ
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
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "ec8941b1-d8b5-4e10-b909-4ad0029cd881",  # 女性の幸せ
]

RELATED_POST_IDS = [
    "36915afc-e0aa-4b34-898b-106f66f11f33",  # 仮交際中、彼からLINEが来ない
    "78d9e1c5-9567-4c4c-a7d8-9b318a131ee9",  # 「どこ行こうか」から、ふたりは始まる
    "0c004668-d23a-40d3-a971-385f8dc6d799",  # 結婚してから、自分がどんどん好きになっていった
]

TITLE   = "【女性向け】「気がきく女子」をお休みしてみない？ ポンコツ女子のすすめ"
EXCERPT = "気がきく女子ほど婚活で空回りしていませんか？先回りして全部やってしまうと、彼の出番がなくなります。仲人・心理カウンセラー中嶋美知が自身の失敗談をもとに、ポンコツ女子のすすめをお伝えします。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
            "sitting at a stylish cafe looking relaxed and slightly playful, "
            "resting her chin on her hand with a natural smile, "
            "modern bright cafe interior, shallow depth of field, "
            "clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-18_ponkotsu_eyecatch.png",
        "caption": "力を抜いて、ちょっとポンコツで",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian couple, "
            "beautiful Japanese woman with elegant refined features and model-like appearance, "
            "man in casual neat outfit, woman looking up at man admiringly "
            "while he shows her something on his phone, both smiling naturally, "
            "modern city street background, shallow depth of field, "
            "clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-18_ponkotsu_couple_street.png",
        "caption": "「すごい！さすが！」って素直に喜ぶだけでいい",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian couple in a cozy kitchen, "
            "man cooking pasta while woman sits at the counter watching with a warm genuine smile, "
            "beautiful Japanese woman with elegant refined features, "
            "casual comfortable home clothes, Sunday afternoon atmosphere, "
            "bright natural light from window, shallow depth of field, "
            "clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-18_ponkotsu_kitchen.png",
        "caption": "完璧じゃないからこそ、二人で補い合える",
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


def build_nodes(url_eyecatch, url_couple, url_kitchen):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # 導入
    nodes.append(p("今日はね、ちょっと耳が痛い話かもしれません。"))
    nodes.append(sp())
    nodes.append(p_bold("テーマは、「気がきく女子をやめて、ポンコツ女子になろう」です。"))
    nodes.append(sp())
    nodes.append(p("えっ？って思いましたよね（笑）"))
    nodes.append(sp())
    nodes.append(p("気がきく女子のほうがモテるに決まってるじゃん！って。"))
    nodes.append(sp())
    nodes.append(p("うん、私もそう思ってたんです。"))
    nodes.append(sp())
    nodes.append(p("でもね、かつての私のしくじりエピソードを聞いてもらえますか。"))
    nodes.append(sp())

    if url_eyecatch:
        nodes.append(image_node(url_eyecatch, "力を抜いて、ちょっとポンコツで"))
        nodes.append(sp())

    # セクション1: 私のしくじりエピソード
    nodes.extend(section("私が「気をきかせすぎた」話"))
    nodes.append(sp())
    nodes.append(p("婚活していたときのことなんですけどね。"))
    nodes.append(sp())
    nodes.append(p("遠距離のお相手と、あるイベントに一緒に行こうって話になったの。"))
    nodes.append(sp())
    nodes.append(p("彼が私の住んでいるエリアのほうに来てくれるっていう流れで、2人ともはじめての場所、はじめてのイベント。"))
    nodes.append(sp())
    nodes.append(p("「どういう場所かな？」「そこまでの道、よくわかんないね」なんて話をして、「じゃあまた計画立てようね」って電話を切ったのね。"))
    nodes.append(sp())
    nodes.append(p("でもさ、地理的には私のほうが地元じゃないですか。"))
    nodes.append(sp())
    nodes.append(p("だから私がある程度調べてあげたほうがいいよね、って思ったんです。"))
    nodes.append(sp())
    nodes.append(p("待ち合わせ場所、イベント前の食事のお店、道順、時間の目安……。"))
    nodes.append(sp())
    nodes.append(p("その日のうちにぜんぶ調べて、翌日LINEで「ここが候補で、こういう道順で、時間はこれくらいかな」って、まとめて送ったの。"))
    nodes.append(sp())
    nodes.append(p("返事は「いいね！ありがとう！」って。"))
    nodes.append(sp())
    nodes.append(p("うん、そうなるよね。当然ですよね。"))
    nodes.append(sp())
    nodes.append(p("——でもね。"))
    nodes.append(sp())
    nodes.append(p_bold("そこから、ちょいちょいあった電話が、減っちゃったの。"))
    nodes.append(sp())
    nodes.append(p("電話ってさ、ほんとたいした話しないんですよ。"))
    nodes.append(sp())
    nodes.append(p("毎日毎日いろんなことが起きるわけじゃないし、ほんとにたわいもないことをぐだぐだ……というかうだうだしゃべってるだけ。"))
    nodes.append(sp())
    nodes.append(p("他の用事しながらしゃべったりとかね。"))
    nodes.append(sp())
    nodes.append(p("でも、そのなんとなくしゃべってる感じが、心地よくて楽しみだったの。"))
    nodes.append(sp())
    nodes.append(p("なのに——イベントの日程が決まって、待ち合わせもタイムスケジュールも全部決まったら、電話がなくなった。"))
    nodes.append(sp())
    nodes.append(p("よく考えたら、当然なんですよね。"))
    nodes.append(sp())
    nodes.append(p_bold("だって、電話する口実がなくなっちゃったんだもん。"))
    nodes.append(sp())
    nodes.append(p("「しまった……」って思いました。"))
    nodes.append(sp())
    nodes.append(p("私が先走って気をきかせて、段取りよく全部決めちゃったばっかりに、彼が「ここどうかな？」「調べてみたよ」って活躍できるシーンが、まるっとなくなっちゃったの。"))
    nodes.append(sp())

    # セクション2: ミニ診断
    nodes.extend(section("あなたにも、心当たりありませんか"))
    nodes.append(sp())
    nodes.append(p("こんなこと、思い当たることはありませんか。"))
    nodes.append(sp())
    nodes.append(p("デートの行き先、いつも自分から調べて提案している。"))
    nodes.append(sp())
    nodes.append(p("「彼に手間をかけさせちゃ悪いな」と、先回りして段取りしている。"))
    nodes.append(sp())
    nodes.append(p("LINEの返事がないと不安になって、つい追加で情報を送ってしまう。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    # セクション3: 右利き比喩
    nodes.extend(section('気をきかせるのは、“右利き”みたいなもの'))
    nodes.append(sp())
    nodes.append(p("こういう先回りって、がんばってやっていると思っていないことが多いんですよね。"))
    nodes.append(sp())
    nodes.append(p("右利きの人が、右手でお箸を持つように。"))
    nodes.append(sp())
    nodes.append(p("もう無意識なんです。"))
    nodes.append(sp())
    nodes.append(p("「相手に迷惑かけちゃいけない」「私がやったほうが早い」「ちゃんとしてる私でいなきゃ」——そんな気持ちが、いつの間にか自動反応になっている。"))
    nodes.append(sp())
    nodes.append(p("これは性格じゃなくて、長い時間をかけて身についた反応パターンなんです。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、意識して「お休み」することができるんですよね。"))
    nodes.append(sp())

    # セクション4: なぜ出番が大事か
    nodes.extend(section("なぜ、彼の「出番」を残すことが大事なのか"))
    nodes.append(sp())
    nodes.append(p("心理学者エドワード・デシとリチャード・ライアンの「自己決定理論」では、人が幸せを感じるために必要な3つの欲求があると言われています。"))
    nodes.append(sp())
    nodes.append(p_bold("そのうちのひとつが、有能感——「自分は役に立っている」「自分がいることで何かが良くなっている」と感じられること。"))
    nodes.append(sp())
    nodes.append(p("これ、男性に限った話じゃないんですが、特に婚活中の男性にとっては大きいんですよね。"))
    nodes.append(sp())
    nodes.append(p("お見合いして、仮交際になって、「この人と一緒にいる意味があるのかな」「自分は必要とされているのかな」って、男性も不安を感じているんです。"))
    nodes.append(sp())
    nodes.append(p("そんなとき、彼女のために何かを調べたり、道を確認したり、お店を提案したりする——その小さな「貢献」のたびに、脳からはオキシトシンが分泌されます。"))
    nodes.append(sp())
    nodes.append(p("オキシトシンは「絆のホルモン」とも呼ばれていて、誰かのために何かをしたとき、守ったとき、感謝されたときにじわっと出るもの。"))
    nodes.append(sp())
    nodes.append(p_bold("つまりね、彼が何かしてくれるたびに、彼の中で「この人を大事にしたい」という気持ちが育っているんです。"))
    nodes.append(sp())
    nodes.append(p("それなのに、こちらが全部やってしまったら——その育つチャンスを、知らないうちに摘み取ってしまっていることになる。"))
    nodes.append(sp())
    nodes.append(p("もったいないと思いませんか。"))
    nodes.append(sp())

    if url_couple:
        nodes.append(image_node(url_couple, "「すごい！さすが！」って素直に喜ぶだけでいい"))
        nodes.append(sp())

    # セクション5: 「してくれない」の正体
    nodes.extend(section("「してくれない」の正体"))
    nodes.append(sp())
    nodes.append(p("「彼が電話くれないんです」「考えてくれないんです」「動いてくれないんです」「私ばっかりやっている気がします」——そんな相談をいただくことが、ほんとうに多いんですよ。"))
    nodes.append(sp())
    nodes.append(p("溺愛してくれるカップルを見て「いいなぁ」って憧れる気持ちも、よくわかります。"))
    nodes.append(sp())
    nodes.append(p("でもね、ちょっと立ち止まって考えてみてほしいんです。"))
    nodes.append(sp())
    nodes.append(p_bold("彼が「してくれない」のは、彼が冷たいからじゃなくて——あなたが気をきかせすぎて、彼の出番が残っていないから、ということはないですか。"))
    nodes.append(sp())
    nodes.append(p("社会学者アーヴィング・ゴフマンは、人間関係には「お互いが役割を演じ合う舞台」のような側面があると言っています。"))
    nodes.append(sp())
    nodes.append(p("片方が完璧に段取りしてくれるなら、もう片方は「観客」になるしかないんですよね。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、観客じゃなくて一緒に舞台に立てるように、不完全な部分をあえて残しておくことが、二人の関係には大事なんです。"))
    nodes.append(sp())

    # セクション6: 母の話
    nodes.extend(section("母を見て思うこと"))
    nodes.append(sp())
    nodes.append(p("うちの母もね、すごく器用な人だったんです。"))
    nodes.append(sp())
    nodes.append(p("何でもできて、しかも早い。"))
    nodes.append(sp())
    nodes.append(p("だから家のこと、ぜーんぶ自分でやってたの。"))
    nodes.append(sp())
    nodes.append(p("庭木の手入れも、家の補修も、網戸の張り替えも。"))
    nodes.append(sp())
    nodes.append(p("町内会のことも、親戚まわりのことも、私たち子どもの学校のPTAも、全部。"))
    nodes.append(sp())
    nodes.append(p("ずーっと動いていてね。"))
    nodes.append(sp())
    nodes.append(p("で、父はどうなったかというと——何もしなくなったんです。"))
    nodes.append(sp())
    nodes.append(p("何もしないから何もわからないし、何もできなくなって、「おーい、お茶」って言って持ってこさせるような人になっちゃった。"))
    nodes.append(sp())
    nodes.append(p("母はよく「お父さんは何もしない」って文句を言っていたけれど……正直なところ、出番がなかったよね、と今なら思うんです。"))
    nodes.append(sp())
    nodes.append(p("家族システム論という考え方があるんですが、家族の中で誰かが「できる人」の役割を強く担いすぎると、他のメンバーは自然と「できない人」の役割に押し出されてしまうと言われています。"))
    nodes.append(sp())
    nodes.append(p("母は気がきく人で、有能な人だった。"))
    nodes.append(sp())
    nodes.append(p("だけど、それが結果として父の居場所をなくしてしまった——そういう側面は、たしかにあったんだろうなぁと思います。"))
    nodes.append(sp())

    # セクション7: ポンコツ女子のすすめ
    nodes.extend(section("「ポンコツ女子」のすすめ"))
    nodes.append(sp())
    nodes.append(p("そんな未来を作らないためにも、ね。"))
    nodes.append(sp())
    nodes.append(p("今から少しだけ、力を抜いてみませんか。"))
    nodes.append(sp())
    nodes.append(p("頼って、甘えて、ちょっとポンコツで。"))
    nodes.append(sp())
    nodes.append(p("「ここ、どう行ったらいいかなぁ？」って聞いてみる。"))
    nodes.append(sp())
    nodes.append(p("「私、こういうの決めるの苦手でさ……」って頼ってみる。"))
    nodes.append(sp())
    nodes.append(p("彼が調べてくれたら、「すごい！」「さすが！」「ありがとうね、助かる〜！」って、素直に喜ぶ。"))
    nodes.append(sp())
    nodes.append(p("それだけで、彼の居場所ができるんです。"))
    nodes.append(sp())
    nodes.append(p("気がきく女子は、たしかに賢くて素敵ですよ。"))
    nodes.append(sp())
    nodes.append(p("さくっと何でもできちゃうのは、ほんとうにすごいことだと思います。"))
    nodes.append(sp())
    nodes.append(p("だけど、それがうまくハマるシーンと、そうじゃないシーンがあるんですよね。"))
    nodes.append(sp())
    nodes.append(p("婚活中の仮交際って、まさに「そうじゃないシーン」のほうが多いんじゃないかなぁと、私は思うんです。"))
    nodes.append(sp())
    nodes.append(p("自分がいなきゃだめだなぁ。"))
    nodes.append(sp())
    nodes.append(p("この人には俺が頼りになるだろう。"))
    nodes.append(sp())
    nodes.append(p("——そう思わせてくれる女性の隣で、男性は自分の存在価値を感じられるんです。"))
    nodes.append(sp())
    nodes.append(p("そしてね、その「必要とされている」という実感が、彼の中に安心を生んで、もっと一緒にいたいという気持ちにつながっていく。"))
    nodes.append(sp())
    nodes.append(p("じんわり、でもたしかに。"))
    nodes.append(sp())

    if url_kitchen:
        nodes.append(image_node(url_kitchen, "完璧じゃないからこそ、二人で補い合える"))
        nodes.append(sp())

    nodes.append(p("想像してみてください。"))
    nodes.append(sp())
    nodes.append(p("疲れて帰ってきた夜、「今日さ、こんなことがあってね」ってたわいもない話をしながら、一緒にごはんを食べている。"))
    nodes.append(sp())
    nodes.append(p("彼が「これ、俺が作ろうか？」って言ってくれて、ちょっと不格好だけど一生懸命つくったパスタを「おいしい！」って食べている、そんな日曜日の昼下がり。"))
    nodes.append(sp())
    nodes.append(p("完璧じゃなくていいんです。"))
    nodes.append(sp())
    nodes.append(p("むしろ、完璧じゃないからこそ、二人で補い合える。"))
    nodes.append(sp())
    nodes.append(p("その「補い合い」が、結婚生活の土台になっていくんですよね。"))
    nodes.append(sp())

    # 今週の一歩
    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日から一つだけ、試してみてください。"))
    nodes.append(sp())
    nodes.append(p("次に彼と会う約束をするとき、お店や道順を調べるのをぐっとこらえて、「どこがいいかな？」って聞いてみる。"))
    nodes.append(sp())
    nodes.append(p("彼が提案してくれたら、完璧じゃなくても「いいね！楽しみ！」って返す。"))
    nodes.append(sp())
    nodes.append(p("それだけでいいんです。"))
    nodes.append(sp())
    nodes.append(p("仮交際のときからね。"))
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
    print("=== ポンコツ女子のすすめ 投稿スクリプト ===\n")

    # 1. 画像生成＆アップロード
    urls = []
    for img in IMAGE_PROMPTS:
        url = generate_and_upload_image(img["prompt"], img["filename"])
        urls.append(url)

    url_eyecatch = urls[0]
    url_couple   = urls[1]
    url_kitchen  = urls[2]

    # 2. richContent構築
    print("\n[richContent構築中...]")
    rich_content = build_nodes(url_eyecatch, url_couple, url_kitchen)

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

    # 5. カバー画像を更新（別PATCHで）
    if url_eyecatch:
        print("\n[カバー画像を更新中...]")
        ok = update_cover_image(post_id, url_eyecatch)
        print(f"  → {'成功' if ok else '失敗'}")

    # 6. SEO description を更新（別PATCHで）
    print("\n[SEO descriptionを更新中...]")
    ok = update_seo(post_id)
    print(f"  → {'成功' if ok else '失敗'}")

    print(f"\n✅ 完了！\n下書きID: {post_id}")
    print("Wixブログ管理画面で確認してください。")
    print("⚠️ 画像が正しく表示されているか、必ず確認をお願いします。")


if __name__ == "__main__":
    main()
