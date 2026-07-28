"""
「俺、本当は結婚したいのかな」って思ったあなたに読んでほしい話
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
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
    "a3a015e3-7f09-4a9f-b5c4-2c59a74bac7c",  # 自己肯定感
]
RELATED_POST_IDS = [
    "388e71e9-6147-4322-a8d9-b66778b31577",  # また会いたいと思われる男性が自然にやっていること
    "f3e9966d-dda6-44cd-8f08-58187f3349c9",  # 見た目を変えたら、婚活も自分への見方も変わった話
    "1098fe45-b32f-4db4-bff4-1fb88d586097",  # 入会して1ヶ月で旅立っていく男性たちの理由
]

TITLE = "「俺、本当は結婚したいのかな」って思ったあなたに読んでほしい話"
EXCERPT = "「俺、本当は結婚したいのかな」とふと感じるとき、それは冷めたわけでも性格の問題でもありません。多くの場合、その正体は\"彼女を喜ばせられるか自信がない\"というサインです。プレゼントや会話でうまくいかなかった経験があるあなたに、その理由と、今日からできることをお伝えします。"
FOCUS_KEYWORD = "婚活 男性 自信がない 結婚したいか迷う"

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

    nodes.append(p("男性会員さんたちとお話ししていると、「俺、本当は結婚したいのかな」とふと迷う声を聞くことがあります。今日はその裏にあるものについて、お話ししたいと思います。"))
    nodes.append(sp())

    nodes.extend(section_heading("自信のなさの正体"))
    nodes.append(sp())
    nodes.append(p("多くの場合、この迷いの正体は「彼女を喜ばせられるか、満たしてあげられるか、自信がない」という気持ちです。"))
    nodes.append(sp())
    nodes.append(p("なぜ自信が持てないかというと、正解がわからないからです。そしておそらく、その裏には成功体験の少なさがあります。良かれと思って選んだプレゼント、一生懸命考えたデート先、会話が途切れないようにと頑張った話題。それなのに、うまくいかなかった経験があるのではないでしょうか。"))
    nodes.append(sp())

    nodes.extend(section_heading("不安は性格ではなく、反応パターンです"))
    nodes.append(sp())
    nodes.append(p("右利きの人が急に左手で箸を持つと、すごく不自由に感じますよね。それと同じで、私たちは「こうすればうまくいくはず」という慣れたやり方を、知らないうちに繰り返しています。"))
    nodes.append(sp())
    nodes.append(p("自信のなさも、性格の問題ではありません。ただ、うまくいかなかった経験からできた反応パターンが、顔を出しているだけなんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("心当たり、ありませんか"))
    nodes.append(sp())
    nodes.append(p("一生懸命選んだプレゼントに「ありがとう」と言われたのに、二度と身につけてもらえなかった。連れて行ったデート先で、なぜか彼女の表情が曇っていた。話が弾んでいる、うんうんと楽しそうに聞いてくれていると思っていたのに、次のお誘いを断られた。——そんな経験です。"))
    nodes.append(sp())
    nodes.append(p("これ、私は婚活でも結婚生活でも、本当によく聞く話なんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("男女で、”良い”の基準が違うだけです"))
    nodes.append(sp())
    nodes.append(p("なぜこんなことが起こるかというと、男性と女性では、いいと感じる基準・選ぶ基準がそもそも違うからです。特にプレゼントは、その差が大きく出ます。"))
    nodes.append(sp())
    nodes.append(p("既婚の男性の友人が、ぼやいていたことがあります。少ないお小遣いから、喜んでもらえたらと思って買ったアクセサリーを、一度もつけてもらえなかったと。別の友人は、彼女が好きだと言っていたブランドのものを選んだのに、「なんか違う」と言われて、わけがわからなかったと言っていました。"))
    nodes.append(sp())
    nodes.append(p("その気持ち、よくわかります。でもこれは、あなたのセンスや気遣いが足りないわけではないんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("だからこそ、”聞く”が最強の武器になります"))
    nodes.append(sp())
    nodes.append(p("プレゼントもデート先も、お金を使う前に、まず聞いてください。サプライズは、実は失敗しやすいのでやめましょう。聞いてしまえば、彼女にとって最高のプレゼントを、確実にオーダーできます。"))
    nodes.append(sp())
    nodes.append(p("会話も同じです。コミュニケーション学の視点では、男性同士の会話は情報を伝え合う”報告型”になりやすく、女性同士の会話は気持ちを分かち合う”共感型”になりやすいと言われています。あなたが一生懸命話す情報提供型の話は、実は彼女にとって少し退屈なことがあるんです。それでも彼女が笑顔でうなずいてくれるのは、優しさとマナーで聞いてくれているからなんですね。"))
    nodes.append(sp())
    nodes.append(p_bold("だから、あなたが長々と話さなくていいんです。"))
    nodes.append(sp())
    nodes.append(p("彼女が話すのを、うんうんと穏やかに聞いてあげてください。「良かったね」「大変だったね」「頑張ったね」「それ面白いね」——それだけで、彼女は十分ハッピーになります。"))
    nodes.append(sp())

    nodes.extend(section_heading("聞くことは、自信につながります"))
    nodes.append(sp())
    nodes.append(p("心理学に「自己効力感」という言葉があります。これは、小さな成功体験を積み重ねることで育っていく、「自分にもできる」という感覚のことです。"))
    nodes.append(sp())
    nodes.append(p("聞きながら、彼女の反応を確かめながら進めていくと、少しずつ彼女の”正解”がわかるようになります。彼女を喜ばせられた、幸せな気持ちにできた——その積み重ねが自信になり、その延長線上に、二人の笑顔の結婚生活を想像できるようになっていきます。"))
    nodes.append(sp())

    nodes.extend(section_heading("頼りにされる人から、選ばれていきます"))
    nodes.append(sp())
    nodes.append(p("彼女の望みや願いをしっかり聞いて、寄り添えるあなたを、心から頼りにしてくれる女性は現れます。ずっと一緒にいたいと、思ってもらえるようになります。"))
    nodes.append(sp())
    nodes.append(p("そうそう、ファッションの好みも、彼女に聞いてみてください。多くの男性の服の好みは、実は彼女の好みとは違います。かわいい女性、綺麗な女性と歩きたいと男性が思うのと同じで、女性もまた、かっこいい男性と歩きたいと思っているんです。服も、鞄も、靴も、彼女の好みに合わせてみる。それだけで、印象は大きく変わります。"))
    nodes.append(sp())

    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("次にプレゼントやデート先を決めるとき、決める前に彼女に一言、聞いてみてください。それだけで、結果は大きく変わります。これから彼女を見つけるというあなたは、仲人に聞いてください。"))
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
