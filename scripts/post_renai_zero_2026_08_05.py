"""
恋愛経験ゼロでも結婚相談所で結婚できるの？　そう不安になっているあなたへ
カテゴリ: 恋愛経験が少ない人の婚活／無料相談の前に読む
2026-08-05
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "69d23361-4fe7-4af6-a69e-2276e1f08417",  # 恋愛経験が少ない人の婚活
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む
]
TAG_IDS = [
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "a3a015e3-7f09-4a9f-b5c4-2c59a74bac7c",  # 自己肯定感
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "aa4700b5-badc-4875-91eb-d0026633922e",  # 婚活カウンセリング
]
RELATED_POST_IDS = [
    "7f515e8f-b0bf-46bd-87e6-e45799651ddf",  # 最後のひとりに出会うまで、ぜんぶ「失敗」
    "c1d689f6-05f4-48af-aa03-05f7d450302e",  # 性格は、今日から変えられる
    "fc45007d-dda4-487e-a7e4-af38ac063665",  # 言葉にしなくていい。触れるだけで、消えていく
]

TITLE = "恋愛経験ゼロでも結婚相談所で結婚できるの？　そう不安になっているあなたへ"
EXCERPT = "恋愛経験が一度もない方にとって、結婚相談所は高いハードルに感じるかもしれません。テクニックや誰かの真似ではなく、素直なあなたのままで婚活する\"素直婚\"という考え方と、その理由についてお話しします。"
FOCUS_KEYWORD = "恋愛経験がない 結婚相談所 婚活"

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

    nodes.append(p("今日は、これまで一度も恋愛やお付き合いをしたことがない、という方に向けてお話ししたいと思います。"))
    nodes.append(sp())
    nodes.append(p("愛媛・松山で婚活を考えている方の中にも、「結婚相談所なんて、私にはハードルが高すぎる」と感じていらっしゃる方、少なくないんじゃないかなと思うんです。"))
    nodes.append(sp())
    nodes.append(p("恋愛経験がないまま今の年齢まで来てしまった。仕事と家の行き帰りだけで、また何年も過ぎていってしまいそうな気がしている。頭のどこかで「奇跡的な出会いが、運命の出会いがあったら」って期待している自分もいる。でも同時に、それが現実的じゃないことも、もうわかっている。"))
    nodes.append(sp())
    nodes.append(p("——そんな感覚、心当たりありませんか。"))
    nodes.append(sp())

    nodes.append(p("どうお付き合いしたらいいのかわからない。何を話したらいいのかもわからない。だから、勇気が出ない。"))
    nodes.append(sp())
    nodes.append(p("恋愛本を読んでみたり、駆け引きのテクニックを調べてみたり。でも「私にできるかな」「難しそうだな」という不安と戸惑いが生まれて、結局動けないまま終わってしまう。"))
    nodes.append(sp())
    nodes.append(p("——そんなサイクルを、もう何年も繰り返してきた方も、いらっしゃるんじゃないでしょうか。"))
    nodes.append(sp())

    nodes.extend(section_heading("それは、あなたの魅力の問題じゃありません"))
    nodes.append(sp())
    nodes.append(p("これ、性格のせいでも、あなたに魅力がないからでもないんです。"))
    nodes.append(sp())
    nodes.append(p("右利きの人が、意識しなくても自然に右手を使うのと同じように、私たちには「慣れた反応」というものがあります。「テクニックを身につけないと、うまくいかない」——そう思い込んでしまうのも、実はその一つ。恋愛経験がないほど、この思い込みは強くなりやすいんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("テクニックじゃなく、素直なあなたのままで"))
    nodes.append(sp())
    nodes.append(p("あすなる愛媛がお勧めしているのは、テクニックでも、誰かのような愛され方・愛し方でもありません。素直なあなた自身で婚活する、ということです。私たちはこれを\"素直婚\"と呼んでいます。"))
    nodes.append(sp())
    nodes.append(p_bold("飾ったり、演じたり、誰かの真似をしたりしなくていい。あなたらしく愛し、愛されればいいんです。"))
    nodes.append(sp())

    nodes.extend(section_heading('恋愛経験がなくても、もう"種"はある'))
    nodes.append(sp())
    nodes.append(p("「でも私、恋愛したことがないから、愛し方なんてわからない」——そう思われるかもしれません。"))
    nodes.append(sp())
    nodes.append(p("でも、これまでの人生の中で、恋愛以外の場面で、少しでも心を通わせられた人はいませんでしたか。家族でも、友人でも、たった一人でもいい。もしその経験があるなら、それはもう、あなたらしい親密さの育て方の\"種\"なんです。"))
    nodes.append(sp())
    nodes.append(p("私は、その種を聞かせていただいて、一緒に育てていくお手伝いをしたいと思っています。"))
    nodes.append(sp())

    nodes.extend(section_heading("自分ではわからないことを、客観的に見るプロ"))
    nodes.append(sp())
    nodes.append(p("自分のことって、自分ではよくわからないものなんですよね。客観的に、他の人から見た方がよくわかることって、実はたくさんあります。特に心理の専門家は、そういうところを見るプロなんです。"))
    nodes.append(sp())
    nodes.append(p("不安も、戸惑いも、そのまま話してくれたらいいんです。期待も、望みも。これまでの失敗や後悔も。これからどうなりたいか、こんな生活にしたいという思いも。「私には向いてないかもしれない」「これは無理かもしれない」という疑問も、全部、素直に出してもらえたらいいんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("科学的にも、理にかなっています"))
    nodes.append(sp())
    nodes.append(p("これ、心理学的にも理にかなっているんです。イギリスの精神科医ジョン・ボウルビィが提唱した愛着理論では、人が誰かと安心して深い関係を築けるかどうかは、実は恋愛経験の有無ではなく、それ以前に家族や身近な人との間で築かれた「安全基地」の経験がベースになっている、と言われています。つまり、恋愛経験がゼロでも、誰か一人とでも安心できる関係を築けたことがあるなら、その土台はもう、あなたの中にあるということなんです。"))
    nodes.append(sp())
    nodes.append(p("それに、恋愛経験がないことを、自分の魅力のなさのせいだと思ってしまう方も多いんですが、社会学的に見ると、今の時代は職場や地域でのつながりが薄くなり、自然な出会いの機会自体が、一昔前よりずっと少なくなっています。経験が積めなかったのは、個人の問題というより、社会の構造が変わったことも大きいんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("実際に、こんな事例もあります"))
    nodes.append(sp())
    nodes.append(p("実際に、恋愛経験が一度もなかった会員様が、〇〇ヶ月でご成婚退会された事例もあります。特別なテクニックを身につけたわけではありません。不安なことも、わからないことも、そのまま素直にお話ししてくださったことが、そのまま前に進む力になっていました。"))
    nodes.append(sp())

    nodes.append(p("飾らなくていい。無理しなくていい。等身大のあなたのまま、力を抜いて微笑み合えるパートナーを、一緒に見つけていきましょう。"))
    nodes.append(sp())
    nodes.append(p("朝、なんでもない会話を交わす。疲れて帰った夜に、ただ隣にいてもらえるだけでほっとする。そんな穏やかな毎日は、テクニックの先にあるものじゃなくて、素直な自分のままで築いていけるものだと、私は思っています。"))
    nodes.append(sp())

    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("もし今、これまでの人生で「この人になら、少し心を開けたな」と思える瞬間が一つでも思い浮かんだら、それがどんな瞬間だったか、今日、少しだけ思い出してみてください。それだけで十分です。"))
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
