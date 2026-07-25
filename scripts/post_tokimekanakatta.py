"""
ときめかなかった人が、いちばん大切な人になった話 — Wix下書き投稿スクリプト
カテゴリ: 仮交際・真剣交際（両方）
2026-07-25
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "3f5f378d-a4f4-47e0-90a7-ab4daa27504e",  # 仮交際
    "5414dab5-ded7-4b15-a88a-d679d6fd3c71",  # 真剣交際
]
TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "0ddde006-b527-4852-8056-8cdb87174e82",  # 真剣交際
    "d3951cb7-1ad4-406d-9d61-544c4e155c9d",  # 相手の見極め方
]
RELATED_POST_IDS = [
    "7f515e8f-b0bf-46bd-87e6-e45799651ddf",
    "2cf3dbc8-6b9d-471a-bc78-8fe3c75f4ff4",
    "ffcc121d-6384-4392-ac96-e7c75f424cf2",
]

TITLE = "【女性向け】ときめかなかった人が、いちばん大切な人になった話。"
EXCERPT = "ときめきより、気を使わなくていい安心感。それが決め手になった、仲人自身の婚活体験談です。愛媛・松山の結婚相談所が伝える、\"友達みたいな人\"を見送らないでほしい理由。"
FOCUS_KEYWORD = "婚活 ときめかない 結婚相手"

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
            "text": text, "decorations": [{"type": "BOLD", "fontWeightValue": 700}]
        }}
    ], "paragraphData": {}}

def heading(text):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": 2}}

def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}

def section_heading(text):
    return [sp(), divider_node(), sp(), heading(text)]

def link_node_centered(text, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": text,
            "decorations": [{"type": "LINK", "linkData": {
                "link": {"url": url, "target": "BLANK"}
            }}]
        }}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}

def build_nodes():
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    nodes.append(p("今日はちょっと、私自身の話をしようと思います。"))
    nodes.append(sp())
    nodes.append(p("私も婚活をしていたとき、最初はやっぱり「理想の人」を探していたんですよね。"))
    nodes.append(sp())
    nodes.append(p("素敵だな、憧れるなって思う人ほど、なぜか自分にブレーキがかかるんです。"))
    nodes.append(sp())
    nodes.append(p("「この人と違うな」って思われたくなくて、思ったことをそのまま言うのをちょっと控えたり、自分の考えを出すのを遠慮したり。"))
    nodes.append(sp())
    nodes.append(p("嫌われたくない、というほど大げさなものじゃないんです。ただ、無意識に少しだけセーブしちゃう。"))
    nodes.append(sp())
    nodes.append(p("あの感覚、わかる方いらっしゃいますよね。"))
    nodes.append(sp())
    nodes.append(p("でも結局、ご成婚退会されていく方々が口を揃えて言うことがあって。私自身もそれを実感したんです。"))
    nodes.append(sp())
    nodes.append(p_bold("決め手になったのは、憧れの人でも、条件が完璧な人でもなくて——気を使わずに、思ったことをそのまま言える人だった、ということでした。"))
    nodes.append(sp())

    nodes.extend(section_heading("「ときめき」と「安心」は、脳の中では別モノなんです"))
    nodes.append(sp())
    nodes.append(p("ここ、実はちゃんと理由があるんです。"))
    nodes.append(sp())
    nodes.append(p("恋愛感情の研究では、「ときめき」と「安心・信頼」はそもそも脳の中で違う仕組みで動いていると言われています。"))
    nodes.append(sp())
    nodes.append(p("ときめきは、相手のまだ知らない部分に反応して出てくる、ドーパミン的な高揚感。新しい人、よくわからない部分が残っている人ほど刺激的に感じやすいんですね。"))
    nodes.append(sp())
    nodes.append(p("一方の「安心する」「落ち着く」という感覚は、オキシトシンという、信頼関係の中でじわじわ育つホルモンが関わっていると言われています。"))
    nodes.append(sp())
    nodes.append(p("つまり、ときめきがないというのは、裏を返せば「もうこの人のことがだいぶわかっている」ということでもあるんです。"))
    nodes.append(sp())
    nodes.append(p("知らない部分が少ないから、刺激としてのときめきは起きにくい。でも、それって恋愛としては物足りなくても、結婚生活としてはものすごく心強いことなんですよね。"))
    nodes.append(sp())
    nodes.append(p("友達っぽい空気になるのも当然です。もう、その人のことをよく知ってるんですから。"))
    nodes.append(sp())
    nodes.append(p("愛媛で婚活中の30代・40代の女性からも、実はこの感覚、よく聞くんです。「ときめかないから、ちょっとこの人は違うのかなって」って。"))
    nodes.append(sp())
    nodes.append(p("その戸惑い、すごくよくわかります。理想の恋愛結婚のイメージと、目の前にある安心感が、なんだか矛盾しているように感じちゃうんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("気を使う癖は、性格じゃなくて反応パターンです"))
    nodes.append(sp())
    nodes.append(p("さっきの「憧れの人の前だとブレーキがかかる」って話、実はこれ、性格の問題じゃないんです。"))
    nodes.append(sp())
    nodes.append(p("右利きの人が急に箸を左手に持ち替えると、すごく不自由に感じますよね。それと同じで、「素敵な人の前では、自分を少し抑えたほうが安全」という反応の仕方が、いつのまにか体に染みついているだけなんです。"))
    nodes.append(sp())
    nodes.append(p_bold("不安は性格じゃなくて、慣れた反応パターン。癖なら、扱い方さえ知れば、少しずつ緩められます。"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("素敵だなと思う人の前だと、つい言いたいことを飲み込んでしまう。LINEの返信を送る前に、何度も文面を読み返して、言葉を選びすぎてしまう。一緒にいて全然疲れないのに、「ときめかないから」という理由だけで、そっと距離を置いたことがある。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("本音を出せる関係が、実は一番贅沢なものだったりします"))
    nodes.append(sp())
    nodes.append(p("心理学に「愛着理論」という考え方があって、そこでは、安心して本音を出せる相手のことを「安全基地」と呼びます。"))
    nodes.append(sp())
    nodes.append(p("人は、安全基地があるからこそ、そこから外の世界に安心して踏み出していけるんですね。逆に言うと、いつも相手の顔色をうかがっていないといけない関係は、安全基地にはなりにくいんです。"))
    nodes.append(sp())
    nodes.append(p("行動レベルでできることから始めるなら、まずは小さな実験からで大丈夫です。次に会う人との会話で、思っていることを一つだけ、そのまま言ってみる。"))
    nodes.append(sp())
    nodes.append(p("「実はさっきの話、ちょっとこう思ったんです」くらいの、小さな一言でいいんです。"))
    nodes.append(sp())
    nodes.append(p("でも本当に緩めたいのは、その奥にある「本音を言うと嫌われるかもしれない」という思い込みそのものです。"))
    nodes.append(sp())
    nodes.append(p("これがどこから来たのか、ゆっくり振り返ってみるのもおすすめです。過去に本音を出して傷ついた経験があったのかもしれないし、家族の中で「いい子」でいることを求められてきたのかもしれません。"))
    nodes.append(sp())
    nodes.append(p("理由がわかると、それだけで少し力が抜けます。"))
    nodes.append(sp())

    nodes.extend(section_heading("気を使い続けることは、想像以上に体力を使います"))
    nodes.append(sp())
    nodes.append(p("もう一つ、お伝えしておきたいことがあります。"))
    nodes.append(sp())
    nodes.append(p("顔色をうかがい続ける関係を選ぶと、長い結婚生活の中で、それがずっと続くということなんです。"))
    nodes.append(sp())
    nodes.append(p("「これを言ったらどう思われるかな」「今、機嫌はどうかな」——そんなふうに毎日、頭のどこかで相手のことを気にかけ続けるのは、実はかなりのエネルギーを使う作業なんですよね。"))
    nodes.append(sp())
    nodes.append(p("心身の健康の研究でも、慢性的に気を張り続けることが、ストレスホルモンの分泌や、睡眠の質、免疫の働きにまで影響することがわかっています。"))
    nodes.append(sp())
    nodes.append(p("仕事に集中できなかったり、休んでいるはずなのに心から休めなかったり——そういう形で、じわじわとダメージが積み重なっていくんです。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、気を使わなくていい相手を選ぶというのは、恋愛としての盛り上がりだけじゃなく、これから何十年も続く暮らしの体力を守る選択でもあるんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("ときめきがなかった人が、一番大切な人になる"))
    nodes.append(sp())
    nodes.append(p("不思議なもので、ときめきがなかった相手ほど、一緒に暮らし始めてから「この人でよかった」としみじみ思うことが多いんです。私自身がそうでした。"))
    nodes.append(sp())
    nodes.append(p("憧れていた恋愛結婚のイメージとは、ちょっと違う。でも、隣にいて疲れない、素のままの自分でいられる——それって、恋愛としては地味に見えても、暮らしの土台としては何より頼りになるものなんですよね。"))
    nodes.append(sp())
    nodes.append(p("疲れて帰ってきた夜に、「今日ちょっとしんどかった」って、取り繕わずに言える。特別な会話がなくても、ソファで並んでテレビを見ているだけで、なんだか安心する。"))
    nodes.append(sp())
    nodes.append(p("そういう小さな日常の場面こそが、長い結婚生活を支えていくんだと思います。"))
    nodes.append(sp())
    nodes.append(p_bold("だからこそ、「ときめかないから」という理由だけで、気を使わずにいられる人を取りこぼさないでほしいなって、心から願っています。"))
    nodes.append(sp())

    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("もし今、「ときめかないから」という理由だけで距離を置いている人がいたら、次に会うときに一つだけ、いつもより本音を言ってみてください。それだけで、その人との関係が何なのか、少し見えてきます。"))
    nodes.append(sp())

    # CTA
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
    r = requests.post(
        f"{WIX_BASE}/blog/v3/draft-posts",
        headers=wix_headers(),
        json=body,
        timeout=30,
    )
    if not r.ok:
        print(f"下書き作成失敗: {r.status_code} {r.text[:500]}")
        return
    draft = r.json().get("draftPost", {})
    draft_id = draft.get("id")
    print(f"下書き作成完了: {draft_id}")

    # SEOメタディスクリプション（正しい形式：seoData.tags）
    if draft_id:
        patch_body = {
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
        rp = requests.patch(
            f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
            headers=wix_headers(),
            json=patch_body,
            timeout=30,
        )
        if rp.ok:
            print("SEOメタ更新完了")
        else:
            print(f"SEOメタ更新失敗: {rp.status_code} {rp.text[:300]}")

    print(f"\n下書きID: {draft_id}")
    print(f"管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")

if __name__ == "__main__":
    main()
