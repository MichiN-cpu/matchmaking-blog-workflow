"""
「この人で本当にいいのかな」——真剣交際に進むときに、その不安が生まれたあなたへ
カテゴリ: 真剣交際／仮交際
2026-08-06
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "5414dab5-ded7-4b15-a88a-d679d6fd3c71",  # 真剣交際
    "3f5f378d-a4f4-47e0-90a7-ab4daa27504e",  # 仮交際
]
TAG_IDS = [
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "0ddde006-b527-4852-8056-8cdb87174e82",  # 真剣交際
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "25417c41-e15f-4447-8e02-1e9b7ff48aec",  # 受け身
]
RELATED_POST_IDS = [
    "bb53a374-57aa-46b7-b92a-2f9295a6ab53",  # 迷いが消えていく人は、実は"最悪"を先に決めている
    "d9f205bf-f8ee-45af-894e-62b0cb82d5dc",  # 心から幸せに成婚退会していく女性は男性のここを見ている
    "8b815244-5096-4f80-8dac-e0b0545a03f4",  # 夫婦の中に「3人の自分」がいる
]

TITLE = "「この人で本当にいいのかな」——真剣交際に進むときに、その不安が生まれたあなたへ"
EXCERPT = "仮交際から真剣交際へ進むとき、「本当にこの人でいいのかな」と不安になるのは、実はとても自然なことです。婚活中のマリッジブルーの正体と、不安に振り回されず主体的に進んでいくための考え方をお伝えします。"
FOCUS_KEYWORD = "真剣交際 不安 マリッジブルー"

def wix_headers():
    return {"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID, "Content-Type": "application/json"}

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
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": [{"type": "BOLD", "fontWeightValue": 700}]}}
    ], "paragraphData": {}}

def heading(text):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": 2}}

def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {"lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"}}

def section_heading(text):
    return [sp(), divider_node(), sp(), heading(text)]

def link_node_centered(text, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]}}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}

def build_nodes():
    nodes = []
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    nodes.append(p("仮交際から真剣交際に進むとき、「本当にこの人でいいのかな」という気持ちが、ふと浮かんでくることがあります。今日はその正体についてお話ししたいと思います。"))
    nodes.append(sp())
    nodes.append(p("真剣交際に進むというのは、これからの二人が結婚に向けて具体的に話を進めていく、という宣言でもあります。お互いの家族へのご挨拶、結婚式のこと、婚約指輪や結婚指輪、親族へのご挨拶、お金のやりくり。いろんなことが一気に具体的になっていきます。人によっては住み慣れた街を離れることになるかもしれませんし、同じ街に住み続けるとしても、ご実家暮らしの方なら「家を出る」という大きな変化があります。男性なら、これから支えていく責任のようなものを感じることもあると思います。"))
    nodes.append(sp())
    nodes.append(p("これだけのことが一度に頭や心に浮かぶのに、全員が万歳、ウキウキと迷いなく結婚まで進んでいくというのは、むしろ珍しいことなんじゃないかなと思います。小さな揺れも、大きな揺れも、あって当然です。"))
    nodes.append(sp())

    nodes.extend(section_heading("それ、実は日常でも起きています"))
    nodes.append(sp())
    nodes.append(p("こういう揺れって、実は日常でもよく起きていませんか。私自身、旅行の前に「もう、めんどくさいな……なんで行くことにしたんだろう」って思うことが、毎回のようにあります。友人との食事会でも、時々「家を出るのが面倒だな」「行くって言わなきゃよかったかな」と思うことさえあります。"))
    nodes.append(sp())
    nodes.append(p("楽しみにしていたはずのことでも、直前になると小さな抵抗感が出てくる。それが結婚のような大きな出来事になれば、なおさらですよね。"))
    nodes.append(sp())
    nodes.append(p("先方のご親族に受け入れてもらえるだろうか。ご家庭の文化が大きく違うんじゃないか。そんなことがすごく大きく、大層なことのように見えてくる。慣れるまでは未知の世界なので、そう思うのも当然です。"))
    nodes.append(sp())

    nodes.extend(section_heading("不安から、思考がすり替わる"))
    nodes.append(sp())
    nodes.append(p("ただ、こういう時に勘違いしやすいことがあるんです。不安が出てきた、自分の未来に迷いが生まれた——そこから、「これはもしかして、相手を好きじゃないのかも」「そもそも私、結婚したかったんだっけ」というふうに、思考がすり替わってしまうことがあります。"))
    nodes.append(sp())
    nodes.append(p_bold("これ、実は「痛みを避けるための思考のスライド」なんです。ここに気づいていただきたいんです。"))
    nodes.append(sp())
    nodes.append(p("不安から意識がそちらにスライドしてしまうと、せっかく「この人とやっていけそう」と思えていた相手から、後ずさりしたり、逃避したりして、また振り出しに戻ってしまう。これを繰り返している方も、実はいらっしゃいます。方向性としては、少しもったいないんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("受け身か、主体的か"))
    nodes.append(sp())
    nodes.append(p("もっと言うと、お見合いをする段階、あるいは仮交際に進む段階から、まるで結婚を決めるかのような大きな不安を口にされる方もいます。これはある意味、まだ現実になっていない未来に、想像で先回りして飲み込まれている状態です。その根っこにあるのは、結婚後の自分の生活が「相手次第」だという、受け身の考え方です。"))
    nodes.append(sp())
    nodes.append(p("自分がどんな結婚生活をしたいかを決めていれば、その生活を一緒に作れる人を選んでいく——そう考えると、お見合いも、仮交際も、真剣交際も、すべて主体的に進んでいくことができます。逆に「良い人が見つかったら幸せになれる」という受け身の考えがベースにあると、不安や恐怖はどうしても大きくなってしまうんです。"))
    nodes.append(sp())
    nodes.append(p("これ、実はその人の性格の問題ではないと思っています。小さい頃から読み聞かされてきた童話の影響もあるんじゃないでしょうか。シンデレラも、白雪姫も、相手が迎えに来てくれて、相手が動いてくれて、幸せになる物語でした。だから「女性はそういうものだ」と、知らないうちに思い込んでしまうのも、無理はないんです。"))
    nodes.append(sp())
    nodes.append(p("でも実際に、幸せな結婚生活を送っている女性たちを見ていると、自分から望む結婚生活を作り上げていっています。自分がどうしてほしいか、どんな未来を過ごしたいか。それを相手と話しているんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("不安は、不確かさから生まれる"))
    nodes.append(sp())
    nodes.append(p("未来は誰にもわかりません。世の中の状況だって変わっていきます。だからこそ、怖いと思っていることを、まず認めて、洗い出してみることが大切です。「もしこうなったら、二人で話し合って決めよう」ということもあれば、「もし相手がこうなったら、私はこうしよう」と一人で決めておくことも、不安を減らして安心を増やす材料になります。"))
    nodes.append(sp())
    nodes.append(p("不安というのは、不確かさから生まれるものです。相手任せ、状況任せにしていると、不確かさはいつまでも減らないので、不安も怖さも、そのまま続いてしまいます。"))
    nodes.append(sp())
    nodes.append(p("これ、心理学的にも裏付けがあります。アメリカの心理学者たちが結婚前の\"迷い\"について調査した研究では、結婚式の前に迷いを感じていた人は、決して少数派ではなかったことがわかっています。大事なのは、迷いがあること自体ではなく、それにどう向き合うか、という指摘なんですね。"))
    nodes.append(sp())

    nodes.extend(section_heading("一人で抱えないで"))
    nodes.append(sp())
    nodes.append(p("誰にとっても、まったく新しい世界に進むのは怖いものです。それでも前に進んでいける人は、「自分がどうするか」を決めています。お相手も、きっと同じように不安を感じているはずです。それを分かち合うことこそが、夫婦としてのスタートなんじゃないでしょうか。"))
    nodes.append(sp())
    nodes.append(p("まずは言いやすいところから、自分の気持ちを伝えてみてください。「そうなんだね」と聞いてもらう。そして、もし必要なら、その不安をどうしてほしいかまで伝えてみましょう。ただ聞いてほしいのか。優しく「大丈夫だよ」と言ってほしいのか。一緒に対策を考えたいのか。それは、あなたが伝えないと、相手にはわからないんです。"))
    nodes.append(sp())
    nodes.append(p("不安な気持ちをそのまま伝えて、してほしい対応まで言葉にする——これは心理学やコミュニケーション学で言う「アサーティブ・コミュニケーション」そのものです。自分も相手も尊重しながら、正直に伝える。これができる関係は、結婚後もずっと役に立ちます。"))
    nodes.append(sp())
    nodes.append(p("一人で不安を抱え込まないでください。仲人にも相談してください。先に結婚した友人や、ご両親も、結婚の先輩です。話を聞いてみてください。そしてもちろん、公認心理師の私にも、いつでも相談してください。"))
    nodes.append(sp())

    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("もし今、心の中に小さな不安があるなら、それを一つだけ、紙に書き出してみてください。そして「もしそうなったら、私はどうしたいか」を、一言だけ考えてみてください。それだけで十分です。"))
    nodes.append(sp())

    nodes.append(link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan", "https://www.asunaru.jp/soudan"))
    return nodes

def main():
    nodes = build_nodes()
    rich_content = {"nodes": nodes, "metadata": {"version": 1}}

    body = {
        "draftPost": {
            "title": TITLE,
            "richContent": rich_content,
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "relatedPostIds": RELATED_POST_IDS,
            "excerpt": EXCERPT,
            "memberId": MEMBER_ID,
        }
    }
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(), json=body, timeout=30)
    if not r.ok:
        print(f"下書き作成失敗: {r.status_code} {r.text[:500]}")
        return
    draft_id = r.json().get("draftPost", {}).get("id")
    print(f"下書き作成完了: {draft_id}")

    seo_patch = {
        "draftPost": {
            "seoData": {
                "tags": [
                    {"type": "title", "children": TITLE},
                    {"type": "meta", "props": {"name": "description", "content": EXCERPT}},
                ],
                "settings": {"preventAutoRedirect": False, "keywords": [{"term": FOCUS_KEYWORD, "isMain": True}]},
            }
        },
        "fieldMask": "seoData",
    }
    rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=seo_patch, timeout=30)
    print("SEOメタ更新完了" if rp.ok else f"SEOメタ更新失敗: {rp.status_code} {rp.text[:300]}")
    print(f"\n下書きID: {draft_id}")
    print(f"管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")

if __name__ == "__main__":
    main()
