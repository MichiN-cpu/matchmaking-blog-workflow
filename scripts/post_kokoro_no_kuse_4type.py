"""
あなたの婚活、止まってしまう理由は4つのうちどれ？——心のクセ診断と、そこからの一歩
カテゴリ: 無料相談の前に読む
2026-07-25
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["641187e4-a409-4c2f-9639-ecc548f26f15"]  # 無料相談の前に読む
TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "a8fd177f-b3ba-4a57-9f81-c26ba1ec0488",  # 婚活相談
    "a3a015e3-7f09-4a9f-b5c4-2c59a74bac7c",  # 自己肯定感
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
]
RELATED_POST_IDS = [
    "c80244fa-098c-4eb0-bbce-71c33d795003",
    "fc6ca9bd-3c37-4619-b33b-a4b0bcd0e05d",
    "1098fe45-b32f-4db4-bff4-1fb88d586097",
]

TITLE = "【男女共通】あなたの婚活、止まってしまう理由は4つのうちどれ？——心のクセ診断と、そこからの一歩"
EXCERPT = "婚活がなかなか進まないのは、性格のせいでも魅力が足りないせいでもありません。たくさんの会員さんのお話から見えてきた、婚活を止めてしまう4つの心のクセと、そこから抜け出す一歩をお伝えします。"
FOCUS_KEYWORD = "婚活 進まない 心理 パターン"

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

    nodes.append(p("これまでたくさんの会員さんとお話をしてきて、ずっと気づいていることがあります。"))
    nodes.append(sp())
    nodes.append(p("婚活が思うように進まないとき、その原因を「自分に魅力がないから」「タイミングが悪いから」と考える方が多いんです。でも実際にじっくりお話を伺っていくと、ほとんどの場合、原因はもっと別のところにあります。"))
    nodes.append(sp())
    nodes.append(p_bold("それは、その人がずっと昔から持っている\"心のクセ\"なんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("不安は性格じゃなくて、反応パターンです"))
    nodes.append(sp())
    nodes.append(p("右利きの人が急に箸を左手に持ち替えると、すごく不自由に感じますよね。それと同じで、私たちは知らないうちに「こういうときはこう反応する」という慣れたパターンを体に染みつかせています。"))
    nodes.append(sp())
    nodes.append(p("婚活が止まってしまうときも同じです。性格が悪いわけでも、魅力がないわけでもなく、ただ「昔からのクセ」がブレーキを踏んでいるだけ。癖なら、正体さえわかれば、少しずつ扱えるようになります。"))
    nodes.append(sp())
    nodes.append(p("これまで面談でお話を伺ってきた中で、特によく出会う4つのパターンをご紹介します。こんなこと、心当たりはありませんか。"))
    nodes.append(sp())

    nodes.extend(section_heading("パターンA：「本音を言うと嫌われる」という恐れ"))
    nodes.append(sp())
    nodes.append(p("思ったことをそのまま言うと「何言ってんの」と思われそうで、踏み込んだ話がしにくい。相手の好きなタイプを演じないといけない気がする。——そんな感覚、ありませんか。"))
    nodes.append(sp())
    nodes.append(p("これは、素の自分を出すこと自体が怖い、という反応パターンです。過去のどこかで、本音を言って傷ついた経験があったのかもしれません。"))
    nodes.append(sp())
    nodes.append(p("心理学の「愛着理論」では、安心して本音を出せる相手を「安全基地」と呼びます。逆に言うと、本音を出したら見捨てられるかもしれないという不安が強いと、どんな相手の前でも安全基地を作れず、いつまでも仮面を外せなくなってしまうんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("パターンG：親密になると、自分から離れてしまう"))
    nodes.append(sp())
    nodes.append(p("順調に進んでいるはずなのに、なぜか距離を置きたくなる。大事にしてくれている人ほど、自分から振ってしまう。——これも、実はよくあるパターンです。"))
    nodes.append(sp())
    nodes.append(p("不思議に思われるかもしれませんが、これは「成功が近づくほど不安が強まる」という反応パターンなんです。"))
    nodes.append(sp())
    nodes.append(p("神経科学の視点では、人は大きな変化——たとえそれが良い変化であっても——に対して、体が警戒信号を出すことがあると言われています。慣れた「うまくいかない自分」から、未知の「幸せな自分」に変わることそのものが、脳にとっては一種のストレスになるんですね。うまくいきそうになるほど、無意識にブレーキを踏んでしまうのは、あなたの意志が弱いからではありません。"))
    nodes.append(sp())

    nodes.extend(section_heading("パターンJ：「役に立つこと」でしか、自分の価値を感じられない"))
    nodes.append(sp())
    nodes.append(p("相手が喜ぶ顔を見るのが好き。「ありがとう」と言われると、自分がここにいる意味を感じる。——優しさとして素敵なことですが、これが行き過ぎると苦しくなることがあります。"))
    nodes.append(sp())
    nodes.append(p("心理学では、これに近い状態を「随伴的自己価値」と呼ぶことがあります。何かで役に立った\"から\"価値がある、という条件つきの自己肯定感です。何もしていない、ただそこにいるだけの自分には価値がないと感じてしまうと、常に何かを差し出し続けないと安心できなくなってしまうんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("パターンQ：「自分なんて」が、行動そのものを止めてしまう"))
    nodes.append(sp())
    nodes.append(p("他の会員さんはレベルが高くて申し込めない。自分と結婚したいと思う人なんていない。——そう感じて、動く前に諦めてしまうパターンです。"))
    nodes.append(sp())
    nodes.append(p("これは、事前に諦めることで、傷つく前に自分を守っている状態です。行動する前に断られた気持ちになっておけば、実際に断られたときのショックが少なくて済む——そんな無意識の計算が働いているんですね。守ろうとする気持ち自体は、決して悪いものじゃありません。"))
    nodes.append(sp())

    nodes.extend(section_heading("この4つに共通していること"))
    nodes.append(sp())
    nodes.append(p("A・G・J・Qに共通しているのは、どれも「昔の自分を守るために身につけた、賢い工夫だった」ということです。"))
    nodes.append(sp())
    nodes.append(p("本音を隠すことで傷つかずに済んだ時期があった。距離を置くことで裏切られずに済んだ時期があった。役に立つことで居場所を確保できた時期があった。諦めることでショックを避けられた時期があった。"))
    nodes.append(sp())
    nodes.append(p("どれも、その人なりの生き延び方だったんです。だからこそ、否定する必要はありません。ただ、今のあなたにとって、その工夫がまだ必要かどうかを、一度確かめてみてほしいんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("心のクセを、少しずつ緩めるために"))
    nodes.append(sp())
    nodes.append(p("行動レベルでできることから始めるなら、まずは小さな一歩からで大丈夫です。今日会う人との会話で、いつもより一つだけ多く本音を言ってみる。距離が縮まって不安になったら、「あ、今この感覚が出てるな」と気づくだけでいい。役に立とうとする前に、何もせずただそこにいてみる。申し込む前に、諦める理由を一つだけ保留にしてみる。"))
    nodes.append(sp())
    nodes.append(p("でも正直にお伝えすると、この心のクセを一人だけで緩めるのは、かなり難しいことなんです。"))
    nodes.append(sp())
    nodes.append(p("やり方を知らないのは、当然のことです。誰も教えてくれませんでしたから。自分の中に染みついたクセを、自分一人で客観的に見つめて、緩めていく——これができる人は、実はそう多くありません。"))
    nodes.append(sp())
    nodes.append(p_bold("だからこそ、プロを頼ってください。"))
    nodes.append(sp())
    nodes.append(p("あすなる愛媛では、仲人自身が公認心理師でもあるので、婚活の相談とあわせて、この\"心のクセ\"の部分まで一緒に整理することができます。一人で抱え込まなくていいんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("変化の恐れを緩めた人から、ご成婚退会していきます"))
    nodes.append(sp())
    nodes.append(p("心のクセに気づいたからといって、その瞬間から怖さがなくなるわけではありません。本音を言うのも、距離を詰めるのも、申し込むのも、最初は今までと同じくらい怖いはずです。"))
    nodes.append(sp())
    nodes.append(p("それでも、変化への恐れを抱えたまま、少しずつそれを緩めて、新しい選択肢を手に入れていった方たちがいます。そして、そういう方たちから、ご成婚退会されていくんです。"))
    nodes.append(sp())
    nodes.append(p("怖さがなくなってから動くのではなく、怖さを抱えたまま、プロと一緒に少しずつ動いていく。癖を緩めるごとに、怖さも少しずつ緩んでいきます。だから大丈夫ですよ。"))
    nodes.append(sp())
    nodes.append(p_bold("その積み重ねが、婚活を——そして、その先の結婚生活を——軽やかなものに変えていきます。"))
    nodes.append(sp())

    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("この4つのパターンを読んで、一番心当たりがあったものを一つだけ選んでみてください。それに気づけたことが、もう最初の一歩です。"))
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
