import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
DRAFT_ID    = "d9f205bf-f8ee-45af-894e-62b0cb82d5dc"

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

TITLE = "【女性向け】心から幸せに成婚退会していく女性は、男性の\"ここ\"を見ています。"
EXCERPT = "ときめきは、消さなくていいんです。ただ、心から幸せな結婚に進んでいく女性たちには、実はもう一つ見ているポイントがあります。愛媛・松山の結婚相談所が伝える、後悔しない相手選びの視点。"
FOCUS_KEYWORD = "婚活 男性 見るべきポイント 結婚相手"

def build_nodes():
    nodes = []
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    nodes.append(p("結婚相談所に興味を持ってくださる女性の多くが、「素敵な人と、運命的にときめいて出会いたい」という気持ちを持っていらっしゃいます。"))
    nodes.append(sp())
    nodes.append(p("その気持ち、すごくよくわかります。むしろ、その気持ちは消さないでいてほしいなって思っているんです。普段の生活では出会えないような素敵な人と出会えるかもしれない——その希望こそが、婚活を始める原動力になったりしますから。"))
    nodes.append(sp())
    nodes.append(p("ただ、実際に心から幸せな形で成婚退会されていく女性たちのお話を伺っていると、ある共通点があることに気づいたんです。それは、「ときめき」だけを基準にしていない、ということでした。"))
    nodes.append(sp())
    nodes.append(p("彼女たちは、ときめきを大事にしながらも、もう一つ、男性の\"ここ\"を見ています。"))
    nodes.append(sp())

    nodes.extend(section_heading("その\"ここ\"、実は最初は気づきにくいポイントです"))
    nodes.append(sp())
    nodes.append(p("実は私自身にも、心当たりがあります。"))
    nodes.append(sp())
    nodes.append(p("婚活をしていたとき、素敵だな、憧れるなって思う人ほど、なぜか自分にブレーキがかかったんです。「この人と違うな」って思われたくなくて、思ったことをそのまま言うのをちょっと控えたり、自分の考えを出すのを遠慮したり。嫌われたくない、というほど大げさなものじゃないんです。ただ、無意識に少しだけセーブしちゃう。あの感覚、わかる方いらっしゃいますよね。"))
    nodes.append(sp())
    nodes.append(p("成婚退会されていく方々のお話を伺っていると、口を揃えてこうおっしゃるんです。「最後の決め手は、憧れだけじゃなくて、気を使わずにいられたことでした」って。"))
    nodes.append(sp())
    nodes.append(p_bold("つまり\"ここ\"というのは——彼といるとき、気を使わずに、思ったことをそのまま言えるかどうか。そういう相手かどうか、なんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("「ときめき」と「安心」は、実は両方あっていいものなんです"))
    nodes.append(sp())
    nodes.append(p("誤解しないでいただきたいのですが、ときめきが悪いわけじゃないんです。"))
    nodes.append(sp())
    nodes.append(p("恋愛感情の研究では、「ときめき」と「安心・信頼」はそもそも脳の中で違う仕組みで動いていると言われています。ときめきは、相手のまだ知らない部分に反応して出てくる、ドーパミン的な高揚感。新しい人、よくわからない部分が残っている人ほど刺激的に感じやすいんですね。"))
    nodes.append(sp())
    nodes.append(p("一方の「安心する」「落ち着く」という感覚は、オキシトシンという、信頼関係の中でじわじわ育つホルモンが関わっていると言われています。"))
    nodes.append(sp())
    nodes.append(p("この二つは別のところから生まれる感覚だから、実は両方を持っている相手に出会えることも、ちゃんとあるんです。ただ、婚活中はどうしてもときめきの方に意識が向きやすい。だからこそ、安心の方は「見よう」としないと、うっかり見落としやすいんですよね。"))
    nodes.append(sp())
    nodes.append(p("愛媛で婚活中の30代・40代の女性からも、実はこういう声をよく聞きます。「ときめかないから、ちょっとこの人は違うのかなって」って。その戸惑い、すごくよくわかります。でも、その\"気を使わなくていい感じ\"こそが、実は見落とされがちな大事なサインだったりするんです。"))
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
    nodes.append(p("彼といるとき、なんとなく素の自分を出しきれていない感じがする。彼の顔色をうかがいながら、言葉を選んで話している。何も話さない沈黙の時間が、ちょっと気まずく感じる。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("本音を出せる関係が、実は一番贅沢なものだったりします"))
    nodes.append(sp())
    nodes.append(p("心理学に「愛着理論」という考え方があって、そこでは、安心して本音を出せる相手のことを「安全基地」と呼びます。"))
    nodes.append(sp())
    nodes.append(p("人は、安全基地があるからこそ、そこから外の世界に安心して踏み出していけるんですね。逆に言うと、いつも相手の顔色をうかがっていないといけない関係は、安全基地にはなりにくいんです。"))
    nodes.append(sp())
    nodes.append(p("行動レベルでできることから始めるなら、まずは小さな実験からで大丈夫です。次に会う人との会話で、思っていることを一つだけ、そのまま言ってみる。「実はさっきの話、ちょっとこう思ったんです」くらいの、小さな一言でいいんです。"))
    nodes.append(sp())
    nodes.append(p("でも本当に緩めたいのは、その奥にある「本音を言うと嫌われるかもしれない」という思い込みそのものです。これがどこから来たのか、ゆっくり振り返ってみるのもおすすめです。過去に本音を出して傷ついた経験があったのかもしれないし、家族の中で「いい子」でいることを求められてきたのかもしれません。理由がわかると、それだけで少し力が抜けます。"))
    nodes.append(sp())

    nodes.extend(section_heading("気を使い続けることは、想像以上に体力を使います"))
    nodes.append(sp())
    nodes.append(p("もう一つ、お伝えしておきたいことがあります。"))
    nodes.append(sp())
    nodes.append(p("顔色をうかがい続ける関係を選ぶと、長い結婚生活の中で、それがずっと続くということなんです。「これを言ったらどう思われるかな」「今、機嫌はどうかな」——そんなふうに毎日、頭のどこかで相手のことを気にかけ続けるのは、実はかなりのエネルギーを使う作業なんですよね。"))
    nodes.append(sp())
    nodes.append(p("心身の健康の研究でも、慢性的に気を張り続けることが、ストレスホルモンの分泌や、睡眠の質、免疫の働きにまで影響することがわかっています。仕事に集中できなかったり、休んでいるはずなのに心から休めなかったり——そういう形で、じわじわとダメージが積み重なっていくんです。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、気を使わなくていい相手かどうかというのは、恋愛としての盛り上がりだけじゃなく、これから何十年も続く暮らしの体力を守る、大事な視点でもあるんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("\"ここ\"を見られる女性が、心から幸せな結婚に進んでいく"))
    nodes.append(sp())
    nodes.append(p("ときめきは、そのまま大事にしてください。運命的な出会いを願う気持ちは、婚活を前に進める大切なエネルギーです。"))
    nodes.append(sp())
    nodes.append(p("そのうえで、彼といるときに、気を使わずに素の自分でいられるかどうか。本音を言っても、離れていかないと思えるかどうか。そんな\"ここ\"にも、少しだけ意識を向けてみてください。"))
    nodes.append(sp())
    nodes.append(p_bold("心から幸せな形で成婚退会されていく女性たちは、ときめきを消さないまま、この視点も一緒に持っていました。"))
    nodes.append(sp())
    nodes.append(p("ときめきと安心、両方を大切にした先に、疲れて帰ってきた日に「今日ちょっとしんどかった」と取り繕わずに言える関係、特別な会話がなくても隣にいるだけで安心できる関係が待っています。"))
    nodes.append(sp())

    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今、気になっている人がいたら、次に会うときに一つだけ、いつもより本音を言ってみてください。それでも彼が変わらず隣にいてくれたら、それが\"ここ\"のサインです。"))
    nodes.append(sp())

    nodes.append(link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan", "https://www.asunaru.jp/soudan"))
    return nodes

def main():
    nodes = build_nodes()
    rich_content = {"nodes": nodes, "metadata": {"version": 1}}

    patch_body = {
        "draftPost": {
            "title": TITLE,
            "richContent": rich_content,
            "excerpt": EXCERPT,
        },
        "fieldMask": "title,richContent,excerpt",
    }
    r = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}", headers=wix_headers(), json=patch_body, timeout=30)
    if not r.ok:
        print(f"本文更新失敗: {r.status_code} {r.text[:500]}")
        return
    print("本文・タイトル・抜粋 更新完了")

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
    rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}", headers=wix_headers(), json=seo_patch, timeout=30)
    print("SEOメタ更新完了" if rp.ok else f"SEOメタ更新失敗: {rp.status_code} {rp.text[:300]}")

if __name__ == "__main__":
    main()
