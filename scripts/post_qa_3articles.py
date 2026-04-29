#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Q&A 3記事一括投稿スクリプト
- 記事①: あすなる愛媛ってどんなとこ？
- 記事②: こんな私でも大丈夫？
- 記事③: 言えなかった本音の疑問
"""

import os
import re
import time
import uuid
import requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_ID = "641187e4-a409-4c2f-9639-ecc548f26f15"  # 無料相談の前に読む

client = OpenAI(api_key=OPENAI_KEY)

def wix_headers():
    return {"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID, "Content-Type": "application/json"}

def nid():
    return str(uuid.uuid4())[:8]

def sp():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}
    ], "paragraphData": {}}

def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}

def make_text_nodes(text):
    result, pos = [], 0
    for m in re.compile(r'https?://\S+').finditer(text):
        if m.start() > pos:
            result.append({"type": "TEXT", "id": nid(), "nodes": [],
                           "textData": {"text": text[pos:m.start()], "decorations": []}})
        result.append({"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": m.group(0), "decorations": [
                           {"type": "LINK", "linkData": {"link": {"url": m.group(0), "target": "BLANK"}}}
                       ]}})
        pos = m.end()
    if pos < len(text):
        result.append({"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": text[pos:], "decorations": []}})
    return result or [{"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}]

def p(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": make_text_nodes(text), "paragraphData": {}}

def q(text):
    """質問（太字）"""
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [],
         "textData": {"text": text, "decorations": [{"type": "BOLD", "fontWeightValue": 700}]}}
    ], "paragraphData": {}}

def h(text, level=2):
    return {"type": "HEADING", "id": nid(),
            "nodes": [{"type": "TEXT", "id": nid(), "nodes": [],
                        "textData": {"text": text, "decorations": []}}],
            "headingData": {"level": level}}

def heading_block(text, level=2):
    return [sp(), divider_node(), sp(), h(text, level)]

def img_node(file_info, caption=""):
    url = file_info["url"]
    m = re.search(r"/media/([^?#\s]+)", url)
    wix_uri = f"wix:image://v1/{m.group(1)}/img.png" if m else url
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": wix_uri}}, "caption": caption}}

def greeting():
    nodes = []
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())
    return nodes

def cta():
    return [sp(), p("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan")]

# ── 記事① ────────────────────────────────────────────────────────────────────

def build_article1():
    n = greeting()
    n.append(p("「無料相談に行く前に、もう少しここのことを知りたい」"))
    n.append(sp())
    n.append(p("そういう方のために、よく聞かれることをまとめました。気になる項目だけでも読んでみてください！"))

    n.extend(heading_block("あすなる愛媛ってどんな相談所？"))
    n.append(q("Q. 大手の結婚相談所と何が違いますか？"))
    n.append(sp())
    n.append(p("一番の違いは、私・中嶋が最初から最後まで直接あなたの婚活に伴走すること。大手は担当者が多くの会員を抱えるため、どうしても一人ひとりの時間が限られます。あすなる愛媛は少人数制だから、「今この人に何が必要か」を一緒に考えながら進んでいけます。担当が変わることもありません。"))
    n.append(sp())
    n.append(q("Q. 心理カウンセラーが仲人というのは、どういうことですか？"))
    n.append(sp())
    n.append(p("婚活がうまくいかない理由って、テクニックより「心の動き」が影響していることが多いんですよ。自己肯定感のなさ、コミュニケーションのクセ、恋愛への思い込み——そういう内側の部分にアプローチしながら婚活を進められるのが、心理カウンセラー仲人ならではのサポートです。「なんかいつもうまくいかない」の根っこから変えていけます！"))
    n.append(sp())
    n.append(q("Q. 少人数制と聞きましたが、何人くらい担当しているんですか？"))
    n.append(sp())
    n.append(p("「一人ひとりをちゃんと見られる人数」にこだわっています。会員さん全員の今の悩みも、前回のお見合いの感想も、ぜんぶ把握した上でサポートしたい。だから「話したことを覚えていてもらえる」「毎回ゼロから説明しなくていい」という安心感が生まれます。"))
    n.append(sp())
    n.append(q("Q. IBJに加盟しているとは、どういう意味ですか？お相手はどこから紹介されますか？"))
    n.append(sp())
    n.append(p("IBJ（日本結婚相談所連盟）は国内最大規模のネットワークで、全国約9万人以上の会員さんの中からお相手を探せます！愛媛県内はもちろん、全国の素敵な方と出会える可能性があるんです。「地元では出会いがない」と思っていた方も、ぐっと視野が広がります。"))
    n.append(sp())
    n.append(q("Q. 愛媛県外の方でも入会できますか？オンラインで活動できますか？"))
    n.append(sp())
    n.append(p("できます！相談やカウンセリングはオンラインでOK。愛媛での出会いを希望している県外の方も、ぜひご相談ください。"))

    n.extend(heading_block("中嶋美知ってどんな人？"))
    n.append(q("Q. 心理カウンセラーとして、どんなサポートをしてもらえますか？"))
    n.append(sp())
    n.append(p("婚活中に出てくる「なぜかいつもここで行き詰まる」という繰り返しパターンに気づいて、一緒にほぐしていくことができます。お見合いで緊張しすぎてしまう、交際が深まると引いてしまう——こういう心の動きに、カウンセラーとしてアプローチしながら婚活を進めます。技術と心、両方からサポートできるのが強みです。"))
    n.append(sp())
    n.append(q("Q. カウンセリングと婚活サポートは、どう違いますか？"))
    n.append(sp())
    n.append(p("カウンセリングは「心を整える」こと、婚活サポートは「行動する」こと。あすなる愛媛ではその両方を同時に進んでいくイメージです。心が整うと行動が変わって、行動が変わると出会いが変わる——この流れを体感していただけます。"))
    n.append(sp())
    n.append(q("Q. 相性が合わなかった場合、担当を変えることはできますか？"))
    n.append(sp())
    n.append(p("あすなる愛媛は私・中嶋一人で運営しているので、担当変更という概念がありません。だからこそ、無料相談で「なんか違うな」と感じたら入会しなくて全然大丈夫。フィーリングって大事ですから、正直に教えてください。"))

    n.extend(heading_block("仲人って、どんな存在？"))
    n.append(q("Q. 仲人って何をする人ですか？なんで他人に結婚に口出しされなきゃいけないの？"))
    n.append(sp())
    n.append(p("「口出し」じゃなくて「伴走」です（笑）！お見合い相手探しから、交際中の「どうしよう」まで、一人じゃ悩みやすいところを一緒に考える存在です。友達に相談すると気を遣うし、親に話すと心配かけるし——そういうとき、「完全にあなたの味方で、かつプロ」な人間がいるって、思ったより心強いですよ。"))
    n.append(sp())
    n.append(q("Q. 仲人さんに自分のプライベートを全部話すのが嫌です。"))
    n.append(sp())
    n.append(p("話したくないことは、話さなくていいです！信頼が積み重なってから、自然に話せるようになることも多いです。あなたのペースに合わせます。"))
    n.append(sp())
    n.append(q("Q. 入会したら「早く決めなさい」って急かされそうで嫌です。"))
    n.append(sp())
    n.append(p("それ、私のスタイルとは真逆です（笑）。焦らせて合わない相手と結婚させることに、私にとってメリットはゼロです。少人数制で一人ひとりに向き合っているからこそ、あなたが「この人だ」と思えるまで一緒に進みます。"))

    n.extend(heading_block("費用と無料相談のこと"))
    n.append(q("Q. 無料相談では、どんなことを話せばいいですか？何か準備は必要ですか？"))
    n.append(sp())
    n.append(p("準備はゼロでOK！「婚活に興味はあるけど、よくわからなくて」くらいの気持ちで来てください。現在の状況をお聞きしながら、サービス内容・料金・活動の流れをご説明します。「話を聞くだけ」という方も大歓迎です。"))
    n.append(sp())
    n.append(q("Q. 入会せずに無料相談だけで終わっても大丈夫ですか？"))
    n.append(sp())
    n.append(p("もちろんです！無理に入会をすすめることは一切しません。帰るときに「来てよかった」と思ってもらえる時間にしたいんです。"))
    n.append(sp())
    n.append(q("Q. 料金プランを教えてください。月々の負担はどのくらいになりますか？"))
    n.append(sp())
    n.append(p("詳しい料金は無料相談の場でご説明しています。「思ったより現実的だった！」とおっしゃる方が多いですよ。入会金・月会費・成婚料などの内訳、活動期間の目安もあわせてお伝えします。"))
    n.append(sp())
    n.append(q("Q. IBJって聞いたことないんですが、大丈夫なんですか？"))
    n.append(sp())
    n.append(p("IBJは国内最大規模の結婚相談所ネットワークで、加盟相談所は全国3,000以上。信頼性で言えば業界トップクラスです。安心してください！"))
    n.append(sp())
    n.append(q("Q. 結婚相談所って、宗教とかネットワークビジネスとか関係ありますか？"))
    n.append(sp())
    n.append(p("ありません！！（笑）あすなる愛媛はIBJ加盟の正規の結婚相談所です。勧誘も変な商品販売も一切なし。"))
    n.append(sp())
    n.append(q("Q. 無料相談に行ったら、断りにくい雰囲気になりませんか？"))
    n.append(sp())
    n.append(p("「断りにくい雰囲気」にするつもりは全然ないです。「今日は話を聞くだけ」で帰っていただいて、ぜんぜん大丈夫。むしろ「また来たいな」と思ってもらえる時間にしたいんです。帰り際に背中を押されたと感じたら、それは私の失敗なので（笑）。"))
    n.extend(cta())
    return n

# ── 記事② ────────────────────────────────────────────────────────────────────

def build_article2():
    n = greeting()
    n.append(p("「婚活したいけど、自分みたいな人間が行って大丈夫かな」"))
    n.append(sp())
    n.append(p("そういう不安、ものすごくよくわかります。今日はそのリアルな疑問に、正直に答えます。"))

    n.extend(heading_block("入会前の「私って大丈夫？」"))
    n.append(q("Q. 恋愛経験がほとんどないのですが、大丈夫ですか？"))
    n.append(sp())
    n.append(p("むしろ大歓迎です！！恋愛経験が少ない方ほど素直に吸収してくれて、グングン成長する姿を何度も見てきました。大切なのは経験の数じゃなくて「相手のことを大切にしたい」という気持ち。一緒にゼロから作っていきましょう。"))
    n.append(sp())
    n.append(q("Q. 婚活が初めてで何もわかりません。何から始めればいいですか？"))
    n.append(sp())
    n.append(p("「何もわからない」状態で来てくれるのが、実は一番ありがたいんですよ（笑）。まっさらな状態が最高のスタートラインです。準備なんて何もいりません、手ぶらで来てください！"))
    n.append(sp())
    n.append(q("Q. 以前、別の結婚相談所でうまくいきませんでした。また失敗するのが怖いです。"))
    n.append(sp())
    n.append(p("前の相談所でうまくいかなかった経験、それがあすなる愛媛でうまくいくための大切な材料になるんです。どこで行き詰まったか・何が合わなかったか——一緒に丁寧に振り返ることが、次の婚活をまったく別ものに変えます。"))
    n.append(sp())
    n.append(q("Q. 自分に自信がないのですが、入会しても意味ありますか？"))
    n.append(sp())
    n.append(p("自信がない状態で来てくれてちょうどいいんです！「自信がついてから婚活しよう」と思っていると、一生始められないですよ（笑）。婚活を進める中でどんどん自信がついていく方を何人も見てきました。動きながら変わっていくのが、婚活の醍醐味のひとつです。"))
    n.append(sp())
    n.append(q("Q. 離婚歴があります。再婚活でも入会できますか？"))
    n.append(sp())
    n.append(p("もちろん！再婚希望の方も大歓迎です。一度の経験があるからこそ「次はこんな関係を築きたい」というビジョンがはっきりしていて、かえってスムーズにいくケースも多いです。お子さんのこと・お金のこと・親への挨拶など、再婚ならではのデリケートな部分も一緒に丁寧に考えていきます。"))

    n.extend(heading_block("「スペックが低い」「別に困ってない」という方へ"))
    n.append(q("Q. スペック（収入・外見）が低いと、活動しても意味ないですか？"))
    n.append(sp())
    n.append(p("スペックが全てだったら結婚相談所って成立しないんですよ（笑）。「一緒にいて心地よい人」「誠実に向き合ってくれる人」が選ばれる場面を何度も見てきました。「スペックが低い」と思っている方ほど、人の話をよく聞けて相手を大切にできる方が多い。それって一番大事な「結婚向きの素質」です。"))
    n.append(sp())
    n.append(q("Q. 「結婚相談所に入るほど困ってない」と思ってます。"))
    n.append(sp())
    n.append(p("この言葉、実はめちゃくちゃ多いんですよ（笑）。でも「困ってから動く」より「動いてから変わる」のほうが婚活はうまくいきます。「困ってないけど、このままでいいのかな」と思ったとき——それが一番いいタイミングかもしれないです。"))
    n.append(sp())
    n.append(q("Q. カウンセラーに「結婚できない理由」を分析されるのが怖いです。"))
    n.append(sp())
    n.append(p("怖いですよね（笑）。でも私は「ダメ出し」をするつもりはまったくないです。「なんでうまくいかないの？」を一緒に発見するのは、責めるためじゃなくて「じゃあここを変えたら変わるよ！」という希望を見つけるためです。分析より共感が先、それが私のスタイルです。"))

    n.extend(heading_block("活動中のこと"))
    n.append(q("Q. 仕事が忙しくて月に1〜2回しか動けません。それでも活動できますか？"))
    n.append(sp())
    n.append(p("できます！忙しい方ほど限られた機会を大切に使う意識が高くて、結果的にうまくいくケースが多いです。活動ペースは一緒に考えますので、まずご相談ください。"))
    n.append(sp())
    n.append(q("Q. お見合い相手は自分で選べますか？それとも紹介してもらうんですか？"))
    n.append(sp())
    n.append(p("両方できます！IBJのシステムで自分で検索してお申込みすることも、私からご提案することも。その時々の状況に合わせて組み合わせながら進めていきます。"))
    n.append(sp())
    n.append(q("Q. 交際中、どんなアドバイスをもらえますか？"))
    n.append(sp())
    n.append(p("LINEの返し方、デートプランの立て方、気持ちの伝え方——交際中に出てくる「どうしよう！」に具体的にお答えします。「相手が今どんな気持ちでいるか」を、心理カウンセラーの視点から一緒に読み解きながらサポートします。一人で悩まなくていい、それがあすなる愛媛の良さです。"))
    n.append(sp())
    n.append(q("Q. 成婚までに平均どのくらいかかりますか？"))
    n.append(sp())
    n.append(p("早い方で半年、平均的には1〜2年くらいのイメージです。大切なのはスピードより「この人でよかった！」と心から思える出会い。焦らず、でも止まらず、一緒に進んでいきましょう。"))
    n.extend(cta())
    return n

# ── 記事③ ────────────────────────────────────────────────────────────────────

def build_article3():
    n = greeting()
    n.append(p("「気になってるんだけど、なんか言いにくくて」"))
    n.append(sp())
    n.append(p("「こんなこと聞いたら失礼かな」"))
    n.append(sp())
    n.append(p("そういう本音の質問、全部受け取ります（笑）。思ってることを正直に聞いてくれるほうが、私は嬉しいです。"))

    n.extend(heading_block("「結婚相談所って…そういうとこでしょ？」"))
    n.append(q("Q. 結婚相談所って、自然な出会いで選ばれなかった人が行くとこじゃないですか？"))
    n.append(sp())
    n.append(p("正直に言ってくれてありがとうございます（笑）。そのイメージ、すごくよくわかります。でも実際に来ている方を見ていると、「モテないから来た」じゃなくて「出会う場所がない・時間がない・職場や友人に異性がいない」という現実的な理由が圧倒的に多いんですよ。医師、教師、エンジニア、看護師……仕事一筋で来てしまった方ばかりです。「選ばれない」んじゃなくて「そもそも出会いの機会がない」、まったく別の話です。"))
    n.append(sp())
    n.append(q("Q. 結婚相談所で出会ったって、友達に言えない気がします。"))
    n.append(sp())
    n.append(p("わかります！でも最近、かなり変わってきていますよ。「マッチングアプリで出会った」が普通になったように、「結婚相談所で出会った」も全然珍しくなくなってきています。それに、幸せになってしまえばどこで出会ったかなんて関係ない。「この人と結婚できてよかった」が、全部を上回ります。"))
    n.append(sp())
    n.append(q("Q. 結婚相談所に入る人って、「早く結婚したい」と焦ってる人ばかりじゃないの？"))
    n.append(sp())
    n.append(p("焦っている方もいれば「ちゃんと考えて決めたい」という方もいます。むしろ「流れで付き合ってなんとなく結婚するのが嫌だ」という、結婚をしっかり考えているからこそ来る方が多い印象です。焦りより「丁寧に選びたい」という意識の方が多いですよ。"))

    n.extend(heading_block("「愛とか好きとか、どうなるの？」"))
    n.append(q("Q. 条件で相手を選ぶって、なんか打算的で嫌です。"))
    n.append(sp())
    n.append(p("すごく真剣に考えている方がおっしゃるんですよね。でも「条件」って本来、「この人とどんな生活を送りたいか」の言語化なんです。収入・居住地・家族観——それって打算じゃなくて、将来の生活を想像しているということ。フィーリングだけで決めて「こんなはずじゃなかった」となるより、ずっと誠実な選び方だと思っています。"))
    n.append(sp())
    n.append(q("Q. 好きでもない人と結婚するの？愛のない結婚になりそう。"))
    n.append(sp())
    n.append(p("「好きから始まらなくていい」という考え方、知っていますか？結婚相談所での出会いは、最初から「ドキドキの恋愛感情」より「この人は誠実だな、一緒にいると安心するな」というところから始まることが多い。でも結婚生活って、むしろそっちのほうが長続きするんですよ。最初のドキドキより、積み重ねた信頼のほうがずっと深い愛になります。"))
    n.append(sp())
    n.append(q("Q. 条件で選んだ相手が、本当に自分のことを好きなのかわからない。"))
    n.append(sp())
    n.append(p("これ、実はアプリや自然な出会いでも同じ不安があると思うんですよね（笑）。結婚相談所の場合は、お互い「結婚を前提に会っている」という真剣さが保証されています。「好きになれるか試す」場所じゃなくて「一緒に生きていける人を探す」場所。それが結婚相談所です。"))
    n.append(sp())
    n.append(q("Q. 結婚相談所で結婚した人って、本当に幸せなんですか？"))
    n.append(sp())
    n.append(p("正直に言います——幸せな方、たくさん見てきました。「この人じゃなかったら出会えなかった」「婚活して本当によかった」とおっしゃる方ばかりです。しっかり考えて選んだ分、覚悟が決まっている。出会い方より、選び方と向き合い方のほうが幸せに影響します。"))

    n.extend(heading_block("「婚活=負け」じゃないよ、という話"))
    n.append(q('Q. 「婚活している」と認めると、なんか自分が"負け"みたいな気がします。'))
    n.append(sp())
    n.append(p("その感覚、めちゃくちゃわかります。でも婚活って「勝ち負け」じゃなくて「行動」なんですよ。欲しいものに向かって動くのは、かっこいいことだと思っています。負けじゃなくて、むしろ一番まともな判断です。"))
    n.append(sp())
    n.append(q("Q. 入会しても成婚できなかったら、お金だけ消えますよね？"))
    n.append(sp())
    n.append(p("そのリスクはゼロじゃないです、正直に言います。だからこそ「どう活動するか」が大事で、それをサポートするのが仲人の仕事です。費用対効果を最大にするために、私もガチで伴走します。"))
    n.append(sp())
    n.append(q("Q. 結婚相談所って、高い人だけが使えるもの？庶民には無理？"))
    n.append(sp())
    n.append(p("「思ったよりかかった」という声と「思ったより現実的だった」という声、半々です（笑）。少なくともあすなる愛媛は「払える範囲でちゃんとサポートを受けられること」を大切にしています。料金は無料相談でぜんぶお伝えしますので、まず聞きにいらしてください。"))
    n.extend(cta())
    return n

# ── 画像生成 ──────────────────────────────────────────────────────────────────

def generate_and_import(prompt_text, filename):
    print(f"  DALL-E 3 生成中: {filename}")
    resp = client.images.generate(model="dall-e-3", prompt=prompt_text,
                                   size="1792x1024", quality="standard", n=1)
    dall_e_url = resp.data[0].url
    print(f"  生成完了。Wixにインポート中...")
    r = requests.post(f"{WIX_BASE}/site-media/v1/files/import", headers=wix_headers(),
                      json={"url": dall_e_url, "displayName": filename, "mimeType": "image/png"}, timeout=30)
    if not r.ok:
        print(f"  インポート失敗: {r.status_code}")
        return None
    data = r.json()
    file_id = (data.get("file") or {}).get("id") or data.get("fileId")
    if not file_id:
        return None
    for i in range(20):
        time.sleep(3)
        chk = requests.get(f"{WIX_BASE}/site-media/v1/files/{file_id}", headers=wix_headers(), timeout=15)
        if chk.ok:
            fd = chk.json().get("file", {})
            if fd.get("state") in ("READY", "OK"):
                url = fd.get("url", "")
                m = re.search(r"/media/([^?#\s]+)", url)
                print(f"  インポート完了: {url[:60]}...")
                return {"url": url, "id": m.group(1) if m else file_id, "height": 1024, "width": 1792, "filename": filename}
            print(f"  待機中... ({fd.get('state')}, {i+1}/20)")
    return None

# ── Wix投稿 ───────────────────────────────────────────────────────────────────

def post_article(title, nodes, img, related_ids, excerpt):
    draft_post = {"title": title, "memberId": MEMBER_ID,
                  "richContent": {"nodes": nodes}, "categoryIds": [CATEGORY_ID]}
    if img:
        m = re.search(r"/media/([^?#\s]+)", img["url"])
        draft_post["media"] = {"custom": True, "wixMedia": {"image": {
            "id": m.group(1) if m else img["id"], "url": img["url"],
            "height": img["height"], "width": img["width"], "filename": img["filename"],
        }}}
    resp = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(),
                         json={"draftPost": draft_post}, timeout=30)
    if not resp.ok:
        print(f"  投稿失敗: {resp.status_code} {resp.text[:300]}")
        return None
    draft_id = resp.json().get("draftPost", {}).get("id")
    # excerpt + related posts
    requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(),
                   json={"draftPost": {"excerpt": excerpt, "relatedPostIds": related_ids},
                         "fieldMask": "excerpt,relatedPostIds"}, timeout=30)
    return draft_id

# ── メイン ────────────────────────────────────────────────────────────────────

RELATED = ["49bc08d5-9927-48c8-a37a-9124b0c43fce",
           "388e71e9-6147-4322-a8d9-b66778b31577",
           "3b824f3b-7b81-45e4-84ea-d5c0948d6b81"]

ARTICLES = [
    {
        "title": "あすなる愛媛のことを、もっと知ってほしい。よくある質問Q&A",
        "builder": build_article1,
        "excerpt": "IBJ加盟・少人数制・心理カウンセラー仲人・料金・無料相談……あすなる愛媛についてよく聞かれる質問に、仲人の中嶋美知がまとめてお答えします。",
        "img_prompt": ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
                       "A warm and welcoming marriage consultation office scene, a friendly female counselor "
                       "sitting across from a client at a cozy desk with soft plants and warm lighting, "
                       "East Asian appearance, black hair, professional yet approachable mood."),
        "img_name": "2026-04-29_qa1_eyecatch.png",
    },
    {
        "title": "こんな私でも大丈夫？婚活を始める前の不安に答えます。",
        "builder": build_article2,
        "excerpt": "恋愛経験なし・自信がない・以前失敗した・忙しい・離婚経験あり……婚活前の「私って大丈夫？」に、心理カウンセラー仲人が正直に答えます。",
        "img_prompt": ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
                       "A Japanese person standing at a crossroads looking thoughtful but hopeful, "
                       "a gentle supportive figure beside them, soft sunrise background, "
                       "East Asian appearance, black hair, warm encouraging mood."),
        "img_name": "2026-04-29_qa2_eyecatch.png",
    },
    {
        "title": "言えなかった本音の疑問、ぜんぶ受け取ります。",
        "builder": build_article3,
        "excerpt": "「モテない人が行くとこ？」「打算的では？」「負けみたいで嫌」——結婚相談所への言えなかった本音の疑問に、仲人が笑いながら正直に答えます。",
        "img_prompt": ("Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
                       "A Japanese person with a slightly skeptical but curious expression, "
                       "thought bubbles with question marks around them gradually turning into light bulbs, "
                       "East Asian appearance, black hair, warm background shifting from cool to warm tones, "
                       "honest and reassuring mood."),
        "img_name": "2026-04-29_qa3_eyecatch.png",
    },
]

def main():
    today = "2026-04-29"
    ids = []

    for i, art in enumerate(ARTICLES, 1):
        print(f"\n{'='*50}")
        print(f"記事{i}「{art['title'][:25]}…」")
        print(f"{'='*50}")

        print(f"  画像生成中...")
        img = generate_and_import(art["img_prompt"], art["img_name"])

        print(f"  Wixに投稿中...")
        nodes = art["builder"]()
        draft_id = post_article(art["title"], nodes, img, RELATED, art["excerpt"])

        if draft_id:
            print(f"  ✓ 下書きID: {draft_id}")
            ids.append((art["title"], draft_id))
        else:
            print(f"  ✗ 投稿失敗")

    print(f"\n{'='*50}")
    print("完了！")
    for title, did in ids:
        print(f"  [{title[:20]}...] {did}")
    print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")

if __name__ == "__main__":
    main()
