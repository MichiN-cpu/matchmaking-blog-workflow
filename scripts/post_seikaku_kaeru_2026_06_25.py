"""
【男性向け】性格は、今日から変えられる。——「俺はこういう人間だから」を卒業する、いちばんシンプルな方法。
カテゴリ: 恋愛経験が少ない人の婚活（69d23361-4fe7-4af6-a69e-2276e1f08417）
公開予定: 2026-06-26（木）下書き保存のみ
"""
import os, uuid, base64, requests, time
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["69d23361-4fe7-4af6-a69e-2276e1f08417"]

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "021e7932-59b1-43ae-9c76-4b00cd73b587",  # 好印象
    "aa4700b5-badc-4875-91eb-d0026633922e",  # 婚活カウンセリング
]

RELATED_POST_IDS = [
    "d82eba55-ad05-41f3-b558-a17ab1646c52",  # 優しいのに選ばれない男性の減点行動
    "49bc08d5-9927-48c8-a37a-9124b0c43fce",  # 行動より先に"あるもの"を変えている
    "8dc13d85-b85f-4247-8a8b-8ed90bad6bdc",  # 媚びるな、危険
]

TITLE   = '【男性向け】性格は、今日から変えられる。——「俺はこういう人間だから」を卒業する、いちばんシンプルな方法。'
EXCERPT = "「こういう性格だから仕方ない」と思っていませんか。でも性格って、実は振る舞いのパターンに過ぎません。愛媛の心理カウンセラー仲人が、性格を行動から変えていくいちばんシンプルな方法をお話しします。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "Japanese man in his 30s, neat dark suit with dress shirt, confident relaxed posture, "
            "genuine warm smile, standing in a modern bright café interior, "
            "clean bright modern atmosphere, shallow depth of field, "
            "professional lifestyle photography, no text"
        ),
        "filename": "2026-06-25_seikaku_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "Japanese man in his 30s, business casual, sitting at a café table "
            "with excellent upright posture, making eye contact with someone across the table, "
            "confident and calm expression, clean bright modern café, "
            "shallow depth of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-06-25_seikaku_posture.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft morning lighting, East Asian appearance, "
            "beautiful Japanese woman with elegant refined features, model-like appearance, clear skin, "
            "Japanese couple in their 30s, sitting side by side at a bright kitchen counter, "
            "both holding coffee mugs, relaxed weekend morning atmosphere, "
            "casual comfortable clothing, gentle smiles, looking at each other naturally, "
            "clean modern kitchen interior, shallow depth of field, "
            "professional lifestyle photography, no text"
        ),
        "filename": "2026-06-25_seikaku_hope.png",
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

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # 導入
    nodes.append(p("今日はちょっと、ストレートなお話をさせてください。"))
    nodes.append(sp())
    nodes.append(p("「俺はこういう性格だから」って、言ったことありませんか。"))
    nodes.append(sp())
    nodes.append(p("お見合いの後、「自分は口下手だから会話が続かなかった」。仮交際のデートで「自分は暗いからうまくいかない」。婚活がうまくいかない原因を、性格のせいにして。"))
    nodes.append(sp())
    nodes.append(p("——そしてその次にこう思うんですよね。「でも、性格は変えられないし」って。"))
    nodes.append(sp())
    nodes.append(p("でもね。ちょっと立ち止まって考えてみてほしいんです。"))
    nodes.append(sp())
    nodes.append(p("「変えられない」って言っているということは、裏を返せば「変えたい」ということですよね。"))
    nodes.append(sp())
    nodes.append(p_bold("今日はその「変えたい」に、本気で応えます。"))
    nodes.append(sp())

    if url1:
        nodes.append(image_node(url1, "「なりたい自分」は、振る舞いから始まる。"))
        nodes.append(sp())

    # セクション1: 性格って何？
    nodes.extend(section("そもそも「性格」って、何でしょう"))
    nodes.append(sp())
    nodes.append(p("「あの人は明るい性格だ」「自分は暗い性格だ」って、日常的に使う言葉です。"))
    nodes.append(sp())
    nodes.append(p("でも、ちょっと考えてみてください。「明るい性格」って、何を見てそう判断していますか。"))
    nodes.append(sp())
    nodes.append(p("たとえば、目の前にこういう人がいたとします。"))
    nodes.append(sp())
    nodes.append(p("口角を上げて、目尻が柔らかくて、顔をちゃんと上げていて、目の前の相手をやさしく見つめている。いわゆるニコニコした状態ですよね。"))
    nodes.append(sp())
    nodes.append(p("——その人を見たら、「明るそうな人だなぁ」って思いませんか。思いますよね。"))
    nodes.append(sp())
    nodes.append(p("声が大きくて、ハキハキと挨拶してくれて、シャキッとしている人がいたら。「爽やかだなぁ」「しっかりしてるなぁ」って感じますよね。"))
    nodes.append(sp())
    nodes.append(p("カフェに入って、席について3秒で注文を決める人。「決断力あるなぁ」って思うでしょう。"))
    nodes.append(sp())
    nodes.append(p("じゃあその人が、家に帰ったらどうなっているか。"))
    nodes.append(sp())
    nodes.append(p("もしかしたら、むすっとしているかもしれない。声も小さく、ぼそぼそと、顔も上げずに話しているかもしれない。注文ひとつ決めるのに、ネットで1時間も2時間も検索しているかもしれない（笑）"))
    nodes.append(sp())
    nodes.append(p("——その姿を見ても「明るくて爽やかで決断力ある人だ」と思いますか？"))
    nodes.append(sp())
    nodes.append(p("思わないですよね。"))
    nodes.append(sp())
    nodes.append(p_bold("つまりね。私たちが「性格」と呼んでいるものって、その人の振る舞い・言動のパターンを見て、周りが判断しているだけなんです。"))
    nodes.append(sp())

    # セクション2: 相対的
    nodes.extend(section("しかも、それは「相対的」なものです"))
    nodes.append(sp())
    nodes.append(p("もうひとつ大事なことがあります。"))
    nodes.append(sp())
    nodes.append(p("さっきの「爽やかでハキハキした人」のすぐ隣に、もっと声が大きくて、もっと表情豊かで、笑いも交えながら挨拶してくれる人がいたとします。"))
    nodes.append(sp())
    nodes.append(p("カフェに入る前からもう注文を決めている人がいたとしたら。"))
    nodes.append(sp())
    nodes.append(p("……さっきの人、急に「そこまで明るくないかも」「そこまで決断力あるってほどでもないかも」って見えてきませんか？"))
    nodes.append(sp())
    nodes.append(p("そうなんですよね。性格には、明確な基準がないんです。"))
    nodes.append(sp())
    nodes.append(p("「ここを満たせば明るい人」「ここを満たせば決断力がある人」なんて、どこにも定義されていない。"))
    nodes.append(sp())
    nodes.append(p("社会学者のアーヴィング・ゴフマンは、人は日常生活の中で常に「役割」を演じている——つまり、場面ごとに振る舞いを変えていると指摘しました。職場での自分、友達といるときの自分、家族の前の自分。全部違いますよね。"))
    nodes.append(sp())
    nodes.append(p("もし性格がひとつの固定されたものなら、どの場面でも同じ振る舞いになるはずです。でも実際は、場面によって全然違う自分が出てくる。"))
    nodes.append(sp())
    nodes.append(p("だからこそ私は、こう考えています。"))
    nodes.append(sp())
    nodes.append(p_bold("性格は固定されたものではなく、振る舞いのパターンでしかない。"))
    nodes.append(sp())
    nodes.append(p("そしてパターンだからこそ、変えることができるんです。"))
    nodes.append(sp())

    if url2:
        nodes.append(image_node(url2, "姿勢ひとつ、目線ひとつで、「印象」は変わる。"))
        nodes.append(sp())

    # セクション3: ミニ診断
    nodes.extend(section("こんなこと、心当たりはありませんか"))
    nodes.append(sp())
    nodes.append(p("お見合いのあと、「もっと明るくできたらよかったのに」と思ったことがある。"))
    nodes.append(sp())
    nodes.append(p("デートの帰り道、「もっと堂々としていたら違ったかもしれない」と振り返ったことがある。"))
    nodes.append(sp())
    nodes.append(p("「こういう性格だから仕方ない」と言いながら、本当はどこかで「変われるなら変わりたい」と思っている。"))
    nodes.append(sp())
    nodes.append(p("——ひとつでも「あるかも」と感じた方は、このあとの話が、きっと力になります。"))
    nodes.append(sp())

    # セクション4: 右利き比喩
    nodes.extend(section("「性格だから仕方ない」も、実はパターンです"))
    nodes.append(sp())
    nodes.append(p("右利きの人が、何も考えなくても右手でお箸を持つように。私たちは長年の習慣で、ある振る舞いのパターンを自動的に繰り返しています。"))
    nodes.append(sp())
    nodes.append(p("声のトーン、姿勢、表情の作り方、人と話すときの目線の置き方。"))
    nodes.append(sp())
    nodes.append(p("これは「生まれつきの性格」なんかじゃなくて、長い年月をかけて身についた反応パターンなんですよね。"))
    nodes.append(sp())
    nodes.append(p_bold("不安は性格ではなく、反応パターンです。「暗い」も「口下手」も「優柔不断」も——全部、繰り返してきたパターン。"))
    nodes.append(sp())
    nodes.append(p("そしてパターンだからこそ、新しいパターンを練習すれば、書き換えることができるんです。"))
    nodes.append(sp())

    # セクション5: 科学的根拠
    nodes.extend(section("「ふりをすれば、そうなる」は科学的事実です"))
    nodes.append(sp())
    nodes.append(p("「振る舞いを変えれば性格が変わるなんて、そんな簡単な話じゃないだろう」って思いますよね。"))
    nodes.append(sp())
    nodes.append(p('「それってただの "ふり" でしょ。見せかけでしょ。実際の自分はそうじゃないのに」って。'))
    nodes.append(sp())
    nodes.append(p("でもね。ここが面白いところなんです。"))
    nodes.append(sp())
    nodes.append(p("心理学者ダリル・ベムの自己知覚理論（1972年）によると、人は自分の行動を観察して「自分はこういう人間だ」と判断していることがわかっています。つまり、明るく振る舞っていれば、「あれ、自分って案外明るい人間なのかも」と感じるようになるんです。自分自身に対しても、振る舞いが性格をつくっている。"))
    nodes.append(sp())
    nodes.append(p("さらに最近の大きな研究——138件の実験を統合したメタ分析（Coles et al., 2022）では、表情を変えると実際に感情が変わることが確認されました。笑顔を作ると、本当に気分が明るくなる。「顔面フィードバック仮説」と呼ばれるものです。"))
    nodes.append(sp())
    nodes.append(p("もうひとつ面白い研究があります。ノースウェスタン大学のアダムとガリンスキー（2012年）が行った実験では、同じ白衣を着ていても、「これは医者の白衣です」と説明された人と「これはペンキ屋さんの白衣です」と説明された人では、注意力テストの結果が違ったんです。着ているものの「意味づけ」が変わるだけで、実際のパフォーマンスが変わる。"))
    nodes.append(sp())
    nodes.append(p_bold("つまり——ふりをしているうちに、ふりじゃなくなるんです。"))
    nodes.append(sp())
    nodes.append(p("「振る舞いを変える」ことは、最もシンプルで、最も科学的に裏付けのある性格の変え方なんですよね。"))
    nodes.append(sp())

    # セクション6: 具体的に何をするか
    nodes.extend(section("婚活で、具体的に何をすればいいか"))
    nodes.append(sp())
    nodes.append(p("じゃあ実際に、どうするか。"))
    nodes.append(sp())
    nodes.append(p_bold("まず、あなたがなりたい「自分」を具体的にしてください。"))
    nodes.append(sp())
    nodes.append(p("「明るい人になりたい」でもいいし、「落ち着いた人になりたい」でもいい。「決断力のある人」でも「爽やかな人」でもいい。"))
    nodes.append(sp())
    nodes.append(p("次に、その人はどう振る舞うかを、一つひとつ想像してみてください。"))
    nodes.append(sp())
    nodes.append(p("その人の姿勢は？座り方は？歩き方は？"))
    nodes.append(sp())
    nodes.append(p("目線はどこを見ている？声のトーンは？速さは？"))
    nodes.append(sp())
    nodes.append(p("どんな言葉を選ぶ？相手にどう挨拶する？"))
    nodes.append(sp())
    nodes.append(p("服装は？髪型は？持ち物は？"))
    nodes.append(sp())
    nodes.append(p("女性のエスコートはどうする？ドアは開ける？椅子は引く？"))
    nodes.append(sp())
    nodes.append(p("動きはゆっくり？テキパキ？"))
    nodes.append(sp())
    nodes.append(p("これ、全部「外側」のことなんですよね。"))
    nodes.append(sp())
    nodes.append(p("性格の「中身」なんて、いじる必要はないんです。振る舞いという「外側」を変えれば、相手から見たあなたの印象は変わります。そして先ほどの研究が示しているように、やっているうちにあなた自身の内側も、ちゃんとついてくるんです。"))
    nodes.append(sp())

    # セクション7: 仲人フィードバック
    nodes.extend(section("仲人がいるなら、使い倒してください"))
    nodes.append(sp())
    nodes.append(p("もしあなたが結婚相談所に入っていて、仲人がいるなら。"))
    nodes.append(sp())
    nodes.append(p("お見合いやデートの後にフィードバックをもらえる環境にいるなら。"))
    nodes.append(sp())
    nodes.append(p("これ、ものすごいアドバンテージですからね。"))
    nodes.append(sp())
    nodes.append(p("だって、「自分がなりたい自分に見えていたかどうか」を聞ける相手がいるわけです。"))
    nodes.append(sp())
    nodes.append(p("「今日の自分、落ち着いた人に見えてましたか？」って聞いてみてください。正直に答えてくれる仲人なら、「ここはよかったけど、ここはもうちょっとこうしたほうがいい」って具体的に教えてくれます。"))
    nodes.append(sp())
    nodes.append(p("それを受けて調整して、また試して、またフィードバックをもらう。"))
    nodes.append(sp())
    nodes.append(p("そうやって少しずつ「なりたい自分」に近づいていけばいいだけの話なんです、ぶっちゃけ。"))
    nodes.append(sp())
    nodes.append(p("一人で鏡に向かって練習するより、ずっと早いですよ。"))
    nodes.append(sp())

    # セクション8: わかっているのにできない
    nodes.extend(section("もし「わかっているのにできない」なら"))
    nodes.append(sp())
    nodes.append(p("ここまで読んで、「なるほど、振る舞いを変えればいいのか」と頭では理解できたとします。"))
    nodes.append(sp())
    nodes.append(p("でも、いざやろうとしたときに——体が動かない。言葉が出ない。わかっているのに、いつもの自分に戻ってしまう。"))
    nodes.append(sp())
    nodes.append(p("そういうこともあるんですよね。"))
    nodes.append(sp())
    nodes.append(p("それは「意志が弱い」のではなくて、心の中に何らかのブレーキがかかっている可能性があります。"))
    nodes.append(sp())
    nodes.append(p("過去の経験——たとえば「目立ったら叩かれた」「自分を出したら否定された」——そういう記憶が、無意識の防衛パターンとして残っていて、新しい振る舞いをブロックしているのかもしれません。"))
    nodes.append(sp())
    nodes.append(p("神経科学の観点で言うと、脳の扁桃体が「この行動は危険だ」と判断して、体を動かす前にブレーキをかけてしまうことがあります。これは生存本能としては正しい反応なのですが、婚活の場面では足かせになってしまうんですよね。"))
    nodes.append(sp())
    nodes.append(p_bold("そういうときは、公認心理師である私に相談してください。"))
    nodes.append(sp())
    nodes.append(p("心理的なブレーキ、一緒に外していきましょう。"))
    nodes.append(sp())

    # 希望への着地
    nodes.extend(section("あなたが「変わった」先にある景色"))
    nodes.append(sp())
    nodes.append(p("想像してみてください。"))
    nodes.append(sp())
    nodes.append(p("お見合いの席で、背筋を伸ばして、自然な笑顔で「よろしくお願いします」と言えている自分。"))
    nodes.append(sp())
    nodes.append(p("仮交際のデートで、「次はここに行きませんか」とさらっと提案できている自分。"))
    nodes.append(sp())
    nodes.append(p("帰りの電車で、「今日、けっこういい感じだったかも」とふわっと思える自分。"))
    nodes.append(sp())
    nodes.append(p("そしていつか——「あなたと一緒にいると安心する」と言ってもらえる日が来ます。"))
    nodes.append(sp())
    nodes.append(p("休みの日、並んでコーヒーを飲みながら「来週、何する？」と話している。そんな穏やかな朝がやってくる。"))
    nodes.append(sp())
    nodes.append(p("その「性格」は、生まれつきのものじゃない。あなたが自分で選んで、自分で育てたものです。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、誰にも奪えない。本当の自信になるんですよね。"))
    nodes.append(sp())

    if url3:
        nodes.append(image_node(url3, "「あなたと一緒にいると安心する」——その一言が聞ける未来。"))
        nodes.append(sp())

    # 今週の一歩
    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("明日、誰かと会うとき——仕事の同僚でも、コンビニの店員さんでも、誰でもいいです。"))
    nodes.append(sp())
    nodes.append(p("いつもより少しだけ口角を上げて、いつもより少しだけ声のトーンを明るくして、「おはようございます」と言ってみてください。"))
    nodes.append(sp())
    nodes.append(p("それだけでいいんです。性格を変える一歩って、そのくらい小さなことから始まりますから。"))
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
    print("=== 性格は変えられる 投稿スクリプト ===\n")

    # 0. 新規タグ作成
    print("[タグ作成中...]")
    new_tag = create_tag("性格")
    if new_tag:
        TAG_IDS.append(new_tag)

    # 1. 画像生成＆アップロード
    urls = []
    for img in IMAGE_PROMPTS:
        url = generate_and_upload_image(img["prompt"], img["filename"])
        urls.append(url)

    url1 = urls[0]
    url2 = urls[1]
    url3 = urls[2]

    # 2. richContent構築
    print("\n[richContent構築中...]")
    rich_content = build_nodes(url1, url2, url3)

    # 3. 下書き作成
    print("\n[Wix下書き作成中...]")
    post_id = create_draft(rich_content)
    if not post_id:
        print("失敗。終了します。")
        return

    print(f"  → 下書きID: {post_id}")

    # 4. カバー画像を設定
    if url1:
        print("\n[カバー画像を設定中...]")
        ok = update_cover(post_id, url1)
        print(f"  → {'成功' if ok else '失敗'}")

    # 5. excerpt・関連記事を更新
    print("\n[excerpt・関連記事を更新中...]")
    ok = update_excerpt_related(post_id)
    print(f"  → {'成功' if ok else '失敗'}")

    # 6. SEO descriptionを更新
    print("\n[SEO descriptionを更新中...]")
    ok = update_seo(post_id)
    print(f"  → {'成功' if ok else '失敗'}")

    print(f"\n✅ 完了！\n下書きID: {post_id}")
    print("Wixブログ管理画面で確認してください。")
    print("⚠️ 画像が正しく表示されているか、必ず確認をお願いします。")


if __name__ == "__main__":
    main()
