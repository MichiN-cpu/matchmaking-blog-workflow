"""
迷ったときほど、答えは頭の外にある。
カテゴリ: 無料相談の前に読む／仮交際
2026-08-02
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む
    "3f5f378d-a4f4-47e0-90a7-ab4daa27504e",  # 仮交際
]
TAG_IDS = [
    "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "0ddde006-b527-4852-8056-8cdb87174e82",  # 真剣交際
    "1571190e-c478-41bd-89b7-aa88c9747b98",  # 決断できない
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
]
RELATED_POST_IDS = [
    "e739167c-44b5-4cbb-b200-2225c919b409",  # かまってほしい/ひとりにして 距離感のNLPメタプログラム
    "7f515e8f-b0bf-46bd-87e6-e45799651ddf",  # 最後のひとりに出会うまで全部失敗
    "f71ec040-995d-4853-96b3-79d663703958",  # リードしなきゃを一人で抱えなくていい
]

TITLE = "【男女共通】迷ったときほど、答えは頭の外にある。"
EXCERPT = "仮交際から真剣交際に進むとき、「どちらを選べばいいかわからない」と立ち止まる方は少なくありません。条件やスペックでは出ない答えを、体感から見つけるNLPのワークをご紹介します。"
FOCUS_KEYWORD = "結婚相手 選べない 決め方"

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

    nodes.append(p("今日は、仮交際から真剣交際に進む時期によく起きる「選べない」というお悩みについて、私が実際に会員様に使っているワークをお話ししようと思います。"))
    nodes.append(sp())
    nodes.append(p("愛媛で婚活中の30代の方からも、よくいただくご相談なんです。「Aさんも良い人、Bさんも良い人。でも、どちらを選べばいいのか分からない」って。"))
    nodes.append(sp())
    nodes.append(p("条件で見れば甲乙つけがたい。年収も、価値観も、優しさも、比べれば比べるほど分からなくなっていく。真面目に婚活に取り組んでいる方ほど、この壁にぶつかりやすいんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("それは、決断力がないわけじゃありません"))
    nodes.append(sp())
    nodes.append(p("でもね、これ、性格の問題でも、決断力がないわけでもないんです。"))
    nodes.append(sp())
    nodes.append(p("右利きの人が、意識しなくても自然に右手を使うのと同じように、私たちには「慣れた反応」というものがあります。悩んだときに、頭の中で条件を並べて比較検討してしまうクセも、実はその一つ。学校でも仕事でも「論理的に、客観的に判断しなさい」と教わってきた方ほど、無意識にこの反応が出やすいんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("こんなこと、心当たりはありませんか"))
    nodes.append(sp())
    nodes.append(p("Aさんのいいところ、Bさんのいいところを、頭の中で表にして比べてしまう。"))
    nodes.append(sp())
    nodes.append(p("どちらかに決めた瞬間、「本当にこれでよかったのかな」と不安になる。"))
    nodes.append(sp())
    nodes.append(p("周りに「普通はどっちを選ぶものか」と意見を求めてしまう。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("条件を、一旦横に置いてみる"))
    nodes.append(sp())
    nodes.append(p("私が真剣交際への移行で迷っている会員様にお伝えしているのは、「一旦、条件も比較検討も横に置いてください」ということです。"))
    nodes.append(sp())
    nodes.append(p("代わりにやっていただくのは、NLPの「タイムライン・コンペア」というワークです。難しく聞こえるかもしれませんが、やること自体はシンプルです。"))
    nodes.append(sp())
    nodes.append(p("まず、Aさんを選んだ未来を思い浮かべて、その中に実際に足を踏み入れるようなつもりで、少しだけ体を動かしてみます。そして、頭で考えるのではなく、体のどこにどんな感じが起きるかに、そっと意識を向けてみるんです。"))
    nodes.append(sp())
    nodes.append(p("胸のあたりが温かくなる。肩の力がふっと抜ける。視界がクリアになる感じがする。心がふわっと軽くなる。逆に、なんとなく重心が浮く感じがしたり、集中が続かなかったり。"))
    nodes.append(sp())
    nodes.append(p("同じことを、Bさんを選んだ未来でもやってみます。"))
    nodes.append(sp())
    nodes.append(p_bold("そうすると、不思議なくらいはっきり、体感の違いが出てくるんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("欲しいのは、条件じゃなく感情だったりします"))
    nodes.append(sp())
    nodes.append(p("婚活中の方って、本当によく考えていらっしゃいます。条件、スペック、将来性。頭の中はいつもフル回転。"))
    nodes.append(sp())
    nodes.append(p("でも、実際に結婚生活の中で得たいものって、突き詰めると「感情」であり「体感」なんですよね。安心できる。嬉しい。穏やか。ウキウキする。一緒にいると勇気が湧いてくる——そういう感覚を、日々の暮らしの中で積み重ねていきたいはずなんです。"))
    nodes.append(sp())
    nodes.append(p("だとしたら、答えを出す場所も、そこに合わせたほうが自然だと思いませんか。"))
    nodes.append(sp())

    nodes.extend(section_heading("科学から見ても、体感には理由があります"))
    nodes.append(sp())
    nodes.append(p("これ、私の感覚だけの話ではなくて、脳科学の分野でも似たようなことが言われています。神経科学者のアントニオ・ダマシオは「ソマティック・マーカー仮説」という考え方を提唱していて、複雑な意思決定ほど、実は身体からの感情的なシグナルに頼っている、と説明しています。理屈は完璧なのに、感情の信号がうまく働かなくなると、簡単な選択すらできなくなってしまう人がいる、という研究報告もあるんです。"))
    nodes.append(sp())
    nodes.append(p("もう一つ。心理学者のダニエル・ギルバートは、人は自分の「将来の感情」を、頭の中の想像だけでは驚くほど正確に予測できない、ということを数々の実験で示しています。だからこそ、ただ考えるのではなく、実際にその未来に「入ってみて」感じてみることに意味があるんですね。"))
    nodes.append(sp())
    nodes.append(p("体感や感情は、潜在意識がそのまま表に出てきたもの。だから、そこに手を伸ばした人が選ぶ相手には、後から振り返っても、ちゃんと納得できる理由があるものなんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("決め方は、その後の結婚生活の土台になります"))
    nodes.append(sp())
    nodes.append(p("真剣交際に進んだ会員様たちを見ていると、決め方そのものが、その後の結婚生活の土台になっているように感じます。"))
    nodes.append(sp())
    nodes.append(p("頭で選んだ人は、後々また頭で悩み続けることが多い。でも、体感で「これだ」と選んだ人は、迷いが出たときも、あのときの感覚に立ち返ることができる。"))
    nodes.append(sp())
    nodes.append(p("一緒に暮らす毎日って、条件表を見返す時間じゃなくて、隣にいて「あ、なんかいいな」と感じる瞬間の積み重ねだったりしますよね。朝のなんでもない会話とか、疲れて帰った夜にほっとする瞬間とか。その感覚に、早いうちから慣れておくことは、決して遠回りじゃないと思うんです。"))
    nodes.append(sp())

    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("もし今、心の中で迷っていることが一つでもあるなら。それぞれを選んだ未来を軽く思い浮かべて、体のどこにどんな感じが起きるか、1分だけ観察してみてください。それだけで大丈夫です。"))
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
