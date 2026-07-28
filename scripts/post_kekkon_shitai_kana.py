"""
「私、本当に結婚したいのかな」って思ったあなたに読んでほしい話
カテゴリ: 無料相談の前に読む
2026-07-28
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["641187e4-a409-4c2f-9639-ecc548f26f15"]  # 無料相談の前に読む
TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "25417c41-e15f-4447-8e02-1e9b7ff48aec",  # 受け身
    "9b60ae78-5278-4749-8def-5547b1410215",  # 迷い
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
    "d5599216-6bdd-47df-9af3-07d1c15c1539",  # 願いを叶える
]
RELATED_POST_IDS = [
    "14ec5353-eba7-4b05-88fa-16d99fd521d1",  # 受け身をやめたら、半年でご成婚できた話
    "ef922c0a-d808-4a03-aef8-c9be3c9c66b5",  # 20年後の幸せな自分から、今日の婚活へのメッセージ
    "c80244fa-098c-4eb0-bbce-71c33d795003",  # 「楽勝」が口癖になった人から、婚活はうまくいく
]

TITLE = "「私、本当に結婚したいのかな」って思ったあなたに読んでほしい話"
EXCERPT = "婚活の途中で「そもそも私、本当に結婚したいのかな」とふと疑ってしまうこと、ありませんか。実はその迷いの正体は、自分の結婚生活を自分で決められていないサインです。望む暮らしを描き、言葉にできる人から、婚活は軽やかに終わっていきます。たくさんの会員さんを見てきて気づいた、心の仕組みをお伝えします。"
FOCUS_KEYWORD = "婚活 結婚したいか迷う 心理"

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

    nodes.append(p("先日、婚活中の女性会員さんとお話ししていて、こんな声を聞きました。「そもそも私、本当に結婚したいのかな。」"))
    nodes.append(sp())
    nodes.append(p("婚活をしていると、活動すればするほど、逆にこの疑問がふと顔を出すことがあります。実はこれ、私が今まで聞いてきた中で、かなりよくある声なんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("不安は性格ではなく、反応パターンです"))
    nodes.append(sp())
    nodes.append(p("右利きの人が急に左手で箸を持つと、すごく不自由に感じますよね。それと同じで、私たちは知らないうちに「こういうときはこう考える」という慣れたパターンを体に染みつかせています。"))
    nodes.append(sp())
    nodes.append(p("「本当に結婚したいのかな」という迷いも、性格の問題ではありません。ただ、ある反応パターンが顔を出しているだけなんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("迷う人に、共通していること"))
    nodes.append(sp())
    nodes.append(p("これまでたくさんの会員さんとお話ししてきて、気づいたことがあります。「結婚したいのかどうかわからない」と感じるとき、それはたいてい、自分の結婚生活を自分で決められていないサインなんです。"))
    nodes.append(sp())
    nodes.append(p("心当たり、ありませんか。場の空気を読んで、相手に合わせるのはとても得意。でも「どんな家に住みたい？」「休日はどう過ごしたい？」と聞かれると、ふと言葉に詰まる。そしてどこかで、運命の出会いさえあれば幸せになれると思っている。——そんな感覚です。"))
    nodes.append(sp())
    nodes.append(p("自分がどんな結婚生活を送りたいか、思い描けていなければ、相手次第・運次第で結果が決まる気がしてしまいます。そうなると不安になるのは当然で、その不安をごまかすために「そもそも結婚したくないのかも」という言葉が出てくるんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("その”合わせる力”は、必殺技でもあり、弱点でもある"))
    nodes.append(sp())
    nodes.append(p("相手に合わせる力は、素敵な力です。場の雰囲気を良くできるし、そつなく物事を進められる。でも、誰もあなたの人生の責任は取ってくれません。"))
    nodes.append(sp())
    nodes.append(p("人に合わせて生きてきた人ほど、自分が何を好きなのか、どんな会話を夫婦でしたいのか、何が自分の充電になるのか、実はよくわかっていないことが多いんです。心理学ではこれを、幼いころに「自分を出すより、合わせるほうが安全だった」と学習してきた反応パターンとして説明することがあります。加えて、女性が望みをはっきり口にすると「わがまま」と見られやすいという、社会がつくってきた空気も、この学習を後押ししてきました。"))
    nodes.append(sp())

    nodes.extend(section_heading("男性は、実は察するのが苦手です"))
    nodes.append(sp())
    nodes.append(p("大事なことなので、男性の特性について少しお話しします。"))
    nodes.append(sp())
    nodes.append(p("男性は基本的に、パートナーの望みを叶えたいと思っている生き物です。ただ、察することがとても苦手で、良かれと思って選んだものが的外れになることが本当によくあります。そして一度その失敗で傷つくと、次はもう自分から動こうとしなくなってしまうんです。"))
    nodes.append(sp())
    nodes.append(p_bold("だからこそ、望みをはっきり言葉にして伝えることは、わがままではなく、パートナーへの贈り物になります。"))
    nodes.append(sp())
    nodes.append(p("「これで喜んでもらえた」という実感があるからこそ、男性はまた次も動けるようになるんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("今日からできること"))
    nodes.append(sp())
    nodes.append(p("行動レベルでできることは、実はとても小さなことです。今日の食事は何が食べたいか、聞かれたときに正直に答えてみる。休日にどう過ごしたいか、一つだけ口に出してみる。"))
    nodes.append(sp())
    nodes.append(p("ただ、正直にお伝えすると、長年染みついた”合わせ癖”を一人だけで緩めるのは、かなり難しいことなんです。やり方を知らないのは当然で、誰も教えてくれませんでしたから。"))
    nodes.append(sp())
    nodes.append(p_bold("だからこそ、プロを頼ってください。"))
    nodes.append(sp())
    nodes.append(p("あすなる愛媛では、仲人自身が公認心理師でもあるので、婚活のご相談とあわせて、この”心のクセ”の部分まで一緒に整理することができます。"))
    nodes.append(sp())

    nodes.extend(section_heading("自分の望む結婚生活を、描けている人から"))
    nodes.append(sp())
    nodes.append(p("自分が望む結婚生活を思い描けている人は、お見合いの最初の一歩から違います。「この人とはちょっと違うかな」と思えば、早めに交際終了という判断もできる。そうやって、一番くつろげて、自分の望みに応えようとしてくれるパートナーにたどり着いていきます。"))
    nodes.append(sp())
    nodes.append(p("一緒に夕食のメニューを決める。疲れて帰った夜に「今日はこれが食べたい」と素直に言える。家事のやり方を、二人ですり合わせていく。そんな小さな場面の積み重ねが、望む結婚生活そのものになっていきます。"))
    nodes.append(sp())
    nodes.append(p_bold("そこまで見えてくると、「そもそも結婚したいのかな」という迷いは、自然と消えていきます。"))
    nodes.append(sp())
    nodes.append(p("運命を待つのではなく、自分でその生活を創っていけると、わかるからです。"))
    nodes.append(sp())

    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、誰かとの会話で、いつもなら流してしまう小さな希望を一つだけ、言葉にしてみてください。「今日はこれが食べたい」その一言からで大丈夫です。"))
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
