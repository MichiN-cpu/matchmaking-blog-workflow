"""
"リードしなきゃ"を、一人で抱えなくていい。——婚活も結婚も、二人で作るものです
カテゴリ: 仮交際
2026-07-25
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["3f5f378d-a4f4-47e0-90a7-ab4daa27504e"]  # 仮交際
TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
]
RELATED_POST_IDS = [
    "97989a04-0b1e-471f-929d-7d34528d6b32",
    "08a6d791-66a4-4594-a55c-6e30180cd86a",
    "96068104-095f-4934-b2bc-db6f60b98e11",
]

TITLE = "【男性向け】\"リードしなきゃ\"を、一人で抱えなくていい。——婚活も結婚も、二人で作るものです"
EXCERPT = "デートの計画も、連絡のペースも、関係を進めることも、全部自分がやらなきゃ——そう思って疲れていませんか。愛媛・松山の結婚相談所が伝える、\"一人で背負う婚活\"から抜け出すための視点。"
FOCUS_KEYWORD = "婚活 男性 一人で頑張る 疲れる"

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

    nodes.append(p("面談で男性会員さんとお話ししていると、よくこんな言葉を聞きます。"))
    nodes.append(sp())
    nodes.append(p("「自分がリードしなきゃいけないと思うと、しんどくて」"))
    nodes.append(sp())
    nodes.append(p("「一人で壁があるように感じます」"))
    nodes.append(sp())
    nodes.append(p("デートのお店を決めるのも、連絡のペースを保つのも、次に進めるかどうかを判断するのも、全部自分の役目だと思っている。そんな男性が、実はとても多いんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("不安は性格じゃなくて、反応パターンです"))
    nodes.append(sp())
    nodes.append(p("右利きの人が急に箸を左手に持ち替えると、すごく不自由に感じますよね。それと同じで、「男は自分からリードするものだ」という反応の仕方も、性格ではなく、いつのまにか体に染みついた慣れたパターンなんです。"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("デートのお店選びで悩みすぎて、誘うこと自体が億劫になる。LINEの返信が少し遅れただけで、自分の連絡の仕方が悪かったのかと考え込む。相手の気持ちがわからないまま、次に誘っていいのかどうかを一人で判断しようとする。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("「男はリードするもの」という思い込みの出どころ"))
    nodes.append(sp())
    nodes.append(p("これ、実は個人の弱さの話じゃないんです。"))
    nodes.append(sp())
    nodes.append(p("社会学の視点で見ると、「デートや結婚は男性主導で進めるもの」という価値観は、長い間、社会全体で共有されてきた\"台本\"のようなものでした。誘うのは男性、決めるのは男性、支えるのは男性。育ってくる過程で、はっきり教えられたわけではないのに、なんとなく刷り込まれている感覚がある方も多いんですよね。"))
    nodes.append(sp())
    nodes.append(p("でも、実際の恋愛や結婚は、台本通りにはいきません。相手にも意志があって、相手にもリードしたい部分があって、相手にも支えたい気持ちがあります。"))
    nodes.append(sp())
    nodes.append(p("一人で全部背負おうとすることは、真面目さの表れでもあります。ただ、それを続けていると、心理学でいう「学習性無力感」に近い状態に近づいていくことがあります。頑張っても頑張っても、うまくいくかどうかは自分だけでコントロールできない。それなのに責任だけは全部自分にある、と感じ続けると、だんだん動くこと自体が怖くなってしまうんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("一人で背負い続けることの、体への負担"))
    nodes.append(sp())
    nodes.append(p("もう一つ、お伝えしておきたいことがあります。"))
    nodes.append(sp())
    nodes.append(p("「自分がやらなきゃ」という緊張感をずっと持ち続けることは、想像以上に体力を使います。心身の健康の研究でも、慢性的に責任感を抱え続けることが、ストレスホルモンの分泌や、睡眠の質、集中力にまで影響することがわかっています。"))
    nodes.append(sp())
    nodes.append(p("デートの前になると変に肩に力が入る。相手の反応を気にしすぎて、会っている間もどこか気が休まらない。——そんな感覚がある方は、すでにこの負担のサインが出ているのかもしれません。"))
    nodes.append(sp())

    nodes.extend(section_heading("二人で作る、という感覚に切り替える"))
    nodes.append(sp())
    nodes.append(p("行動レベルでできることから始めるなら、まずは小さな一歩からで大丈夫です。次のデートのお店選びを、一つだけ相手に委ねてみる。「どこか行きたいところある？」と聞いてみる。連絡のペースについても、「僕はこれくらいの頻度が心地いいけど、どう思う？」と、正解を一人で決めずに聞いてみる。"))
    nodes.append(sp())
    nodes.append(p("そして、根本のところで見つめ直したいのは、「リードする＝一人で全部決める」という思い込みそのものです。本当のリードというのは、全部を背負うことではなく、相手と一緒に方向を決めていく力のことなんですよね。"))
    nodes.append(sp())
    nodes.append(p("コミュニケーション学では、これに近い考え方を「協働的な意思決定」と呼びます。二人の関係は、一人が引っ張って、もう一人がついていくものではなく、二人で一緒に作り上げていくものだという捉え方です。"))
    nodes.append(sp())
    nodes.append(p("そして、二人で作っていくために、実はとても効果的な一手間があります。それは、女性が話しているとき、途中で遮らずに、最後まで耳を傾けることです。"))
    nodes.append(sp())
    nodes.append(p("「でも」「それより」と口を挟みたくなる瞬間があっても、まずは最後まで聞く。それだけで、女性は「ちゃんと聞いてもらえた」という満足感を得られます。そしてその安心感があるからこそ、自分の気持ちも素直に話せるようになりますし、今度は逆に、あなたの考えにも耳を傾けてくれるようになるんです。"))
    nodes.append(sp())
    nodes.append(p_bold("コミュニケーション学でいう「傾聴」も、まさにこの構造です。聞くという行為は、リードすることの反対ではありません。むしろ、二人で作っていくための、一番シンプルで確実な一歩なんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("支え合える関係を、婚活の段階からつくる"))
    nodes.append(sp())
    nodes.append(p("一人で頑張り続けてきた男性ほど、実は「支えてもらう」ということに慣れていません。でも、結婚生活は何十年も続きます。仕事で疲れて帰ってきた日、体調を崩した日、悩みを抱えた日——そんなとき、一人で抱え込まずに、隣にいる人と分け合えるかどうかが、長い暮らしの心地よさを大きく左右します。"))
    nodes.append(sp())
    nodes.append(p("婚活の段階で「一人で背負わなくていい」という感覚を少しずつ練習しておくことは、その先の結婚生活の土台をつくることでもあるんです。"))
    nodes.append(sp())
    nodes.append(p_bold("デートのお店を一緒に決めた。連絡のペースについて素直に聞けた。それだけの小さな一歩が、「この人とは、一緒に作っていけそうだ」という安心感を、相手にも自分にも育てていきます。"))
    nodes.append(sp())

    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("次に会うとき、彼女が話し終わる前に口を挟みそうになったら、一度だけ我慢して、最後まで聞いてみてください。それだけで、二人の関係の重さが少し変わります。"))
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
