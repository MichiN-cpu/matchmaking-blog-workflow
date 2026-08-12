"""
自分を責めない人から、うまくいく。ゴルフのメンタルコントロールに学ぶ婚活の話
カテゴリ: 無料相談の前に読む
2026-08-12
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む
]
TAG_IDS = [
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
    "d372d6c7-06f8-47fe-a647-6229a0b94c80",  # お見合い
    "a3a015e3-7f09-4a9f-b5c4-2c59a74bac7c",  # 自己肯定感
]
RELATED_POST_IDS = [
    "c80244fa-098c-4eb0-bbce-71c33d795003",  # 「楽勝」が口癖になった人から、婚活はうまくいく。
    "cd924cca-49c1-42ef-97d3-db44b30dc50b",  # 心のクセ診断
    "29af95af-c7da-4507-bdbe-f53aa9f54309",  # 迷ったときほど答えは頭の外にある。
]

TITLE = "自分を責めない人から、うまくいく。ゴルフのメンタルコントロールに学ぶ婚活の話"
EXCERPT = "婚活がうまくいかないとき、つい「自分のせいだ」と抱え込んでいませんか。ゴルフの試合でコーチが徹底する「うまくいかないことは自分以外のせいにする」というメンタルコントロール法から、婚活を苦しくしない考え方をご紹介します。反応パターンに気づけば、力を抜いて続けていけます。"
FOCUS_KEYWORD = "婚活 うまくいかない 自分のせい"

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

    nodes.append(p("先日、ゴルフをされている方から、面白い話を聞きました。"))
    nodes.append(sp())
    nodes.append(p("ゴルフの練習中はさておき、試合本番になると、メンタルがものすごく結果に影響するんだそうです。だからこそ、コーチから徹底して指導されることがあるらしいんですね。"))
    nodes.append(sp())
    nodes.append(p("それは、「試合中はどんなにうまくいかないことがあっても、自分以外のもののせいにする」ということでした。"))
    nodes.append(sp())
    nodes.append(p("天候のせい。周りの音のせい。時間のせい。太陽のせい。コースの設計のせい。"))
    nodes.append(sp())
    nodes.append(p("一見、ちょっと無責任にも聞こえる教えですよね。でも、これ、すごく理にかなっているんです。"))
    nodes.append(sp())
    nodes.append(p("ゴルフって、基本的には一人のゲームなんですよね。誰かとチームを組むわけでもない。目の前に向かって戦う相手がいるわけでもない。ただ、自分がどれだけスコアを伸ばせるか、それだけなんです。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、うまくいかなかったときに全部「自分のせい」にしてしまうと、もう本当に苦しくなる。逃げ場がなくなってしまうんですよね。"))
    nodes.append(sp())
    nodes.append(p("これ、婚活にもすごく似ていると思うんです。"))
    nodes.append(sp())
    nodes.append(p("婚活も、お相手がいるとはいえ、実はコントロールできない要因だらけなんですよね。"))
    nodes.append(sp())
    nodes.append(p("お相手の希望条件。お相手が今、お見合いを受けられる状態にあるかどうか。スケジュールがいっぱいで余裕がない時期かもしれない。ちょうど気になる人ができたタイミングだったかもしれない。お相手の思い描く結婚生活のハードルがとても高かったり、すでに固まっていたり。ご家族の希望条件が、想像以上に重かったりもします。"))
    nodes.append(sp())
    nodes.append(p("「これをしたら絶対にこの人とうまくいく」という正解、実はないんですよね。いろんなタイミングが重なって、初めて成り立つものだから。"))
    nodes.append(sp())
    nodes.append(p("お相手の好みも、ご家族の希望も、出会うタイミングも、こちらが完全に合わせにいくことって、そもそも難しいものなんです。"))
    nodes.append(sp())
    nodes.append(p("十人十色、蓼食う虫も好き好き、とはよく言ったもので。「え、そんな理由で終わってしまうの?」と、私自身びっくりすることも、正直あります。"))
    nodes.append(sp())
    nodes.append(p("悪いところなんて全然ないし、気になるところも気に触るところもない。なのに「なんだか友達みたいな、くつろぎすぎる感じがして」という理由で終わってしまったり。何かドラマチックな出来事がきっかけで、急に終わってしまったり。"))
    nodes.append(sp())
    nodes.append(p("理屈や理論だけでは説明できない部分が、ちゃんとあるんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("気づいたら、自分を責めていませんか"))
    nodes.append(sp())
    nodes.append(p("うまくいかなかったとき、「私のせいだ」「自分に魅力がなかったんだ」と抱え込んでしまう。そんな心当たり、ありませんか。"))
    nodes.append(sp())
    nodes.append(p("お見合いが成立しなかったとき、真っ先に自分の欠点を探してしまう。"))
    nodes.append(sp())
    nodes.append(p("デートの感触は良かったはずなのに、その後連絡が途切れると「私の話し方が悪かったのかな」と何度も振り返ってしまう。"))
    nodes.append(sp())
    nodes.append(p("条件的には合っているはずなのにご縁が続かないと、「自分はやっぱりダメなのかもしれない」と落ち込んでしまう。"))
    nodes.append(sp())
    nodes.append(p_bold("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("それ、性格じゃなくて反応パターンです"))
    nodes.append(sp())
    nodes.append(p("実はこの「うまくいかないことがあると、つい自分のせいにしてしまう」というのも、性格の問題ではなくて、反応パターンなんです。"))
    nodes.append(sp())
    nodes.append(p("利き手ってありますよね。右利きの人が、無意識に右手を使うのと同じ。特別意識しなくても、そちらの手が自然に出てしまう。それくらい、深く染みついた「クセ」なんです。"))
    nodes.append(sp())
    nodes.append(p_bold("不安も、自分を責める思考も、性格ではなく反応パターン。だから、変えていくこともできます。"))
    nodes.append(sp())
    nodes.append(p("心理学には「帰属理論」という考え方があります。うまくいかなかった理由を、自分の内側（能力や人格）に求めるか、外側（状況やタイミング）に求めるかで、その後のモチベーションや自己肯定感が大きく変わる、というものです。スポーツ心理学の世界では、外側の要因に目を向けられる選手ほど、次のプレーへの立て直しが早いことが知られています。ゴルフのコーチが「天候のせいにしていい」と教えるのは、根性論ではなく、ちゃんと理にかなった技術なんですね。"))
    nodes.append(sp())
    nodes.append(p("それに、自分を責め続けている状態って、体にも負担がかかります。「私が悪い」と感じ続けると、コルチゾールというストレスホルモンが出て、体も心も緊張したままになってしまう。そうなると、次のお見合いの場でも表情がこわばったり、素の自分が出しにくくなったりする。悪循環になってしまうんですよね。"))
    nodes.append(sp())
    nodes.append(p("さらに言うと、今の社会は「結果は自己責任」という空気がとても強いんです。社会学の世界では、これを「個人化」と呼んだりします。昔は家やご近所が結婚を取り持ってくれていたけれど、今は恋愛も結婚も、うまくいかなかったときに「自分の努力不足」として引き受けなければならない場面が増えている、という指摘です。だからこそ、意識して「これは私だけの責任じゃない」と思い出す必要があるんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("今日からできる、小さな実践"))
    nodes.append(sp())
    nodes.append(p("お見合いが成立しなかったとき、デートの後に連絡が続かなかったとき。頭の中で自分を責める前に、声に出してでも、紙に書いてでもいいので、外側の要因を一つ挙げてみてください。"))
    nodes.append(sp())
    nodes.append(p("「お相手の今のタイミングじゃなかったのかも」「ご家族の希望条件と合わなかったのかも」「単純に、好みのタイプが違っただけかも」。"))
    nodes.append(sp())
    nodes.append(p("ゴルフ選手が「今日は風が強かったな」とつぶやくのと同じです。これは言い訳ではなく、次のプレーに向けて自分を立て直すための、れっきとした技術なんですよね。"))
    nodes.append(sp())
    nodes.append(p("そしてもう一段、根っこの部分。「うまくいかない＝自分のせい」という反応パターンそのものに気づくこと。これがいちばん大事です。"))
    nodes.append(sp())
    nodes.append(p("自分では、なかなか気づけないものなんですよね。かつての私自身も、そうでした。だからこそ、外から見てもらう機会が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("力まず、続けていく先に"))
    nodes.append(sp())
    nodes.append(p("婚活は、正解が決まっているテストとは違います。「この振る舞いをすれば合格」という、ほにゃらら検定ではないんです。"))
    nodes.append(sp())
    nodes.append(p("だから、いちばんの近道は、リラックスして、淡々とお見合いの申し込みと、お受けするというところを続けていくこと。自分ではどうしようもない、ご縁のタイミングやお導きがあるまで、緊張しすぎないこと。"))
    nodes.append(sp())
    nodes.append(p("そのために大切なのは、自分らしくいること。自分らしい楽しみを見つけて、婚活そのものを楽しむこと。"))
    nodes.append(sp())
    nodes.append(p("たとえば、お見合いの帰り道にお気に入りのカフェに寄る。仮交際中のお相手と、他愛のない話で笑い合う。うまくいかなかった日は、好きな音楽を聴きながら「今日は天候のせい」と、ちょっと自分に笑ってあげる。そんな小さな積み重ねが、婚活を続けていく力になります。"))
    nodes.append(sp())
    nodes.append(p("力まず、続けていく先に、たった一人の、これから何年も一緒に暮らしていく方との出会いがあります。"))
    nodes.append(sp())
    nodes.append(p("そこまでの道のりを、どうか一人で抱え込まないでくださいね。"))
    nodes.append(sp())

    nodes.append(link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"))
    return nodes

def create_draft():
    body = {
        "draftPost": {
            "title": TITLE,
            "richContent": {"nodes": build_nodes(), "metadata": {"version": 1}},
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "excerpt": EXCERPT,
            "memberId": MEMBER_ID,
        },
        "publish": False,
    }
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(), json=body, timeout=30)
    if not r.ok:
        print("下書き作成失敗:", r.status_code, r.text[:500])
        return None
    draft = r.json()["draftPost"]
    print("下書き作成完了 ID:", draft["id"])
    return draft["id"]

def set_related_posts(draft_id):
    body = {
        "draftPost": {"relatedPostIds": RELATED_POST_IDS},
        "fieldMask": "relatedPostIds",
    }
    r = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=body, timeout=30)
    print("関連記事設定:", "完了" if r.ok else f"失敗 {r.status_code} {r.text[:300]}")

if __name__ == "__main__":
    draft_id = create_draft()
    if draft_id:
        set_related_posts(draft_id)
        print("\nDRAFT_ID =", draft_id)
