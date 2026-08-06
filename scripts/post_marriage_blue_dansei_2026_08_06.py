"""
「本当に俺で、この人を幸せにできるのかな」——真剣交際が近づくと、不安になるあなたへ
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
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
]
RELATED_POST_IDS = [
    "97989a04-0b1e-471f-929d-7d34528d6b32",  # "弱音を吐けない"をやめた男性から、家庭は安定していく
    "35d610c7-50ee-45ad-8d0a-310b7893b9b6",  # この人で本当にいいのかな（女性版・対の記事）
    "c1d689f6-05f4-48af-aa03-05f7d450302e",  # 性格は、今日から変えられる
]

TITLE = "「結婚がリアルになってきて、なんだか気分が重い」——そんなあなたへ。"
EXCERPT = "結婚が近づくにつれて、なんだか気分が重い、そわそわして落ち着かない——そんな感覚を抱く男性は少なくありません。その正体と、一人で抱え込まずに進んでいく方法をお伝えします。"
FOCUS_KEYWORD = "真剣交際 不安 男性 プレッシャー"

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

    nodes.append(p("結婚がリアルになってきて、なんだか気分が重い。そわそわして、集中できない。理由もよくわからないけど、なんとなくスッキリしない。"))
    nodes.append(sp())
    nodes.append(p("——そんな感覚、ありませんか。それ、実は\"ビビってる\"のかもしれません。今日はその正体についてお話ししたいと思います。"))
    nodes.append(sp())
    nodes.append(p("真剣交際に進むというのは、これからの二人が結婚に向けて具体的に話を進めていく、という宣言でもあります。お互いの家族へのご挨拶、結婚式のこと、婚約指輪や結婚指輪、親族へのご挨拶、お金のやりくり。いろんなことが一気に具体的になっていきます。相手が住み慣れた街を離れて来てくれるかもしれませんし、これから家庭を支えていく責任のようなものも、頭のどこかで感じ始めると思います。"))
    nodes.append(sp())
    nodes.append(p("これだけのことが一度に頭や心に浮かぶのに、迷いなく「よし、いくぞ」と思えるという人は、むしろ珍しいんじゃないかなと思います。小さな揺れも、大きな揺れも、あって当然です。"))
    nodes.append(sp())

    nodes.extend(section_heading("それ、実は日常でも起きています"))
    nodes.append(sp())
    nodes.append(p("こういう揺れって、実は日常でもよく起きていませんか。大事な会議の前や、大きな決断をする前、誰でも「本当にこれでいいのか」と一瞬立ち止まる感覚があると思います。楽しみにしていたはずのことでも、直前になると小さな抵抗感が出てくる。それが結婚のような大きな出来事になれば、なおさらですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("不安から、結論にすり替わる"))
    nodes.append(sp())
    nodes.append(p("ただ、こういう時に勘違いしやすいことがあるんです。プレッシャーを感じた、自分の未来に迷いが生まれた——そこから、「俺にはまだ早いのかも」「本当にこの人を幸せにできる自信がない」というふうに、不安が結論にすり替わってしまうことがあります。"))
    nodes.append(sp())
    nodes.append(p_bold("これ、実は「プレッシャーを避けるための思考のスライド」なんです。ここに気づいていただきたいんです。"))
    nodes.append(sp())
    nodes.append(p("不安から意識がそちらにスライドすると、せっかく「この人と家庭を持ちたい」と思えていた気持ちから後ずさりしたり、連絡を減らしてそのままフェードアウトしてしまったり。爆発するわけではなく、静かに距離を置いてしまう。これを繰り返している方も、実はいらっしゃいます。"))
    nodes.append(sp())

    nodes.extend(section_heading("一人で背負わなくていい"))
    nodes.append(sp())
    nodes.append(p("男性は「支える側」「決める側」でいなければ、という意識を、知らないうちに強く持っていることが多いです。弱音を吐いたら情けない。頼りない男だと思われたくない。だから、経済的な不安も、将来への責任も、一人で抱え込もうとしてしまう。"))
    nodes.append(sp())
    nodes.append(p("これ、性格の問題ではないと思っています。「男は弱さを見せてはいけない」という社会的な思い込みを、知らないうちに受け取ってきただけなんです。右利きの人が、意識しなくても自然に右手を使うのと同じように、これも一つの「慣れた反応」なんですよね。"))
    nodes.append(sp())
    nodes.append(p("でも実際に、幸せな結婚生活を送っている男性たちを見ていると、一人で全部背負おうとはしていません。不安なことも、わからないことも、パートナーに話しています。"))
    nodes.append(sp())

    nodes.extend(section_heading("不安は、不確かさから生まれる"))
    nodes.append(sp())
    nodes.append(p("未来は誰にもわかりません。だからこそ、怖いと思っていることを、まず認めて、洗い出してみることが大切です。「もしこうなったら、二人で話し合って決めよう」ということもあれば、「もしこうなったら、自分はこうしよう」と一人で決めておくことも、不安を減らして安心を増やす材料になります。"))
    nodes.append(sp())
    nodes.append(p("不安というのは、不確かさから生まれるものです。一人で抱えて誰にも話さないままだと、不確かさはいつまでも減らないので、不安もプレッシャーも、そのまま続いてしまいます。"))
    nodes.append(sp())
    nodes.append(p("心理学に「自己効力感」という言葉があります。これは、小さな成功体験を積み重ねることで育っていく、「自分にもできる」という感覚のことです。一人で抱え込んで空回りするより、相談しながら少しずつ進めていく方が、実はこの自己効力感を育てやすいんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("一人で抱えないで"))
    nodes.append(sp())
    nodes.append(p("誰にとっても、まったく新しい世界に進むのは怖いものです。それでも前に進んでいける人は、「自分がどうするか」を決めています。お相手も、きっと同じように不安を感じているはずです。それを分かち合うことこそが、夫婦としてのスタートなんじゃないでしょうか。"))
    nodes.append(sp())
    nodes.append(p_bold("弱音を吐くことは、弱さじゃありません。"))
    nodes.append(sp())
    nodes.append(p("まずは言いやすいところから、自分の気持ちを伝えてみてください。「ちょっと相談したいことがあるんだけど」——それだけで十分です。相手も、身構えるより先に「聞くよ」という気持ちで受け止めやすくなります。"))
    nodes.append(sp())
    nodes.append(p("一人で不安を抱え込まないでください。仲人にも相談してください。先に結婚した友人や、ご両親も、結婚の先輩です。話を聞いてみてください。そしてもちろん、公認心理師の私にも、いつでも相談してください。"))
    nodes.append(sp())

    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("もし今、心の中に小さな不安があるなら、それを一つだけ、彼女に話してみてください。「ちょっと相談したいことがあるんだけど」——そこから始めてみるだけで十分です。"))
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
