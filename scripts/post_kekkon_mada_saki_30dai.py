"""
「結婚はまだ先でいい」と思っていた男性たちが、後から気づいたこと — Wix下書き投稿スクリプト
カテゴリ: 30代婚活（男女・悩み別）
2026-06-11
"""
import os, time, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "ce3b3deb-a05e-4093-a1a3-aa657693da8d",  # 30代婚活（男女・悩み別）
]
TAG_IDS = [
    "b280c34f-9ade-4642-94c4-c9a0c4ddbdae",  # 30代
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "61acc4f3-6c16-4653-995b-dd6d9136c1d3",  # IBJ
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
]
RELATED_POST_IDS = [
    "3f84d312-9c4f-40b7-8476-963876091b38",  # ちょっと変わるだけでダントツになれる(30代後半から婚活→7ヶ月成婚)
    "fc81155c-09b4-4e31-9530-b0ff5f90e27f",  # 苦手でも諦めなかった 30代医療職男性の成婚ストーリー
    "63b597d5-7354-4738-a55c-f59aa21b6aec",  # 婚活を途中で諦めたくなる人の特徴2選
]

IMG_DIR = os.path.expanduser("~/matchmaking-blog-workflow/drafts/images")
EYECATCH = os.path.join(IMG_DIR, "2026-06-11_eyecatch.png")
BODY1    = os.path.join(IMG_DIR, "2026-06-11_body1_evening_meal.png")
BODY2    = os.path.join(IMG_DIR, "2026-06-11_body2_profile_cafe.png")


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


def h(text, level=2):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": level}}


def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}


def link_node(text, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": text,
            "decorations": [{"type": "LINK", "linkData": {
                "link": {"url": url, "target": "BLANK"}
            }}]
        }}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}


def image_node(url, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": url}}, "caption": caption}}


def upload_image_binary(filepath, filename):
    with open(filepath, "rb") as f:
        image_bytes = f.read()

    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "displayName": filename},
        timeout=30,
    )
    if not r.ok:
        print(f"アップロードURL取得失敗: {r.status_code} {r.text[:200]}")
        return None
    data = r.json()
    upload_url = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        print(f"uploadURL取得失敗: {data}")
        return None

    sep = "&" if "?" in upload_url else "?"
    upload_url_with_filename = f"{upload_url}{sep}filename={filename}"
    headers = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        headers["Authorization"] = upload_token
    ru = requests.put(upload_url_with_filename, data=image_bytes, headers=headers, timeout=120)
    if not ru.ok:
        print(f"バイナリアップロード失敗: {ru.status_code} {ru.text[:200]}")
        return None
    result = ru.json()
    file_obj = result.get("file", {})
    file_url = file_obj.get("url", "")
    file_id  = file_obj.get("id", "")
    if not file_url:
        print(f"アップロード結果にURLなし: {result}")
        return None
    print(f"アップロード完了: {filename} -> {file_url[:70]}...")
    return {"url": file_url, "id": file_id}


def build_nodes(img1=None, img2=None):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # イントロ
    nodes.append(p("最近、男性の会員さんとお話ししていて、よく聞くお話があるんですよね。"))
    nodes.append(sp())
    nodes.append(p("「結婚はまだ先でいいかな、と思っていたんです」"))
    nodes.append(sp())
    nodes.append(p("仕事を頑張りたい時期だし、女性と違って妊娠する体でもないし。"))
    nodes.append(p("だから「自分にはまだ時間がある」って、自然に思える。"))
    nodes.append(p("それ、すごくよくわかるんです。"))
    nodes.append(p("私自身も、何かを始めるタイミングって「今じゃなくてもいいかな」って先延ばしにしてしまうこと、正直ありますし（笑）。"))
    nodes.append(sp())
    nodes.append(p("でね。"))
    nodes.append(sp())
    nodes.append(p("実際に30代後半になってから婚活を始めた男性たちに話を聞くと、口を揃えてこう言うんです。"))
    nodes.append(sp())
    nodes.append(p("「思っていたより、ずっとしんどかった」"))
    nodes.append(p("「もっと早く動いておけばよかった」"))
    nodes.append(p("「相談所に、もっと早く入っておけばよかった」"))
    nodes.append(sp())

    # Section 1: ミニ診断・反応パターン
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("こんなこと、思い当たることはありませんか"))
    nodes.append(sp())
    nodes.append(p("「結婚なんて、30代後半か、40代になってからでいいかな」"))
    nodes.append(p("「仕事が落ち着いたら、ちゃんと考えよう」"))
    nodes.append(p("「焦って結婚相手を探すのは、なんだかかっこ悪い気がする」"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あ、それ自分かも」と思った方は、このあとの話、きっと役に立つと思います。"))
    nodes.append(sp())
    nodes.append(p("こういう「まだ先でいい」という感覚も、実は、性格ではなく、ただの“反応パターン”なんですよね。"))
    nodes.append(sp())
    nodes.append(p("たとえば、右利きの人がお箸を右手で持つのって、生まれつき決まっていたわけじゃなくて、繰り返し使っているうちに、自然とそうなっただけなんです。"))
    nodes.append(sp())
    nodes.append(p("それと同じで、「結婚はまだ先」という感覚も、これまで触れてきた情報や、まわりの空気の中で、いつのまにか身についた“クセ”のようなもの。"))
    nodes.append(p("決して、あなた自身の本質や、価値観そのものではないんですよね。"))
    nodes.append(sp())
    nodes.append(p("だから、ちょっとだけ視点を変えてみると、見える景色が変わってくることがあります。"))
    nodes.append(sp())

    # Section 2: 仕事と結婚は両立できる
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("結婚しても、仕事のやりがいは消えない"))
    nodes.append(sp())
    nodes.append(p("まず、これだけは伝えておきたいんですけど。"))
    nodes.append(sp())
    nodes.append(p("結婚したからといって、仕事に手を抜くことになったり、暇になったりすることは、まずありません。"))
    nodes.append(p("むしろ、家族のためにという目的ができることで、仕事への向き合い方が変わったという声を、私はたくさん聞いてきました。"))
    nodes.append(sp())
    nodes.append(p("「自分のためだけ」より「大切な人のため」の方が、人は踏ん張れる。"))
    nodes.append(p("これは心理学でも、モチベーションの研究の中でよく語られる話なんですよね。"))
    nodes.append(p("世界で一番自分を応援してくれる人がそばにいる。"))
    nodes.append(p("それって、仕事にとっても、ものすごく心強いことだと思うんです。"))
    nodes.append(sp())

    # Section 3: IBJガイドライン・相談所の強み
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("結婚相談所に登録している人は、もう「覚悟が決まっている人」"))
    nodes.append(sp())
    nodes.append(p("それから、もう一つ。"))
    nodes.append(sp())
    nodes.append(p("結婚相談所、特にIBJ加盟店には、共通のガイドラインがあって。"))
    nodes.append(p("お見合いから3ヶ月をめどにご成婚を目指し、長くても6ヶ月以内には進退を決めましょう、という基準があるんです。"))
    nodes.append(sp())
    nodes.append(p("つまり、相談所に登録している女性は「結婚を決めている人たち」なんですよね。"))
    nodes.append(p("恋人探しではなく、結婚を見据えて、ある程度のスピード感を持って動いている。"))
    nodes.append(sp())
    nodes.append(p("ここがアプリや自然な出会いと、大きく違うところだと思います。"))
    nodes.append(p("お見合いをセッティングしてもらえて、交際の進め方も相談できて、アドバイスをもらいながらトントンと進められる。"))
    nodes.append(p("だから、忙しい男性ほど、実は結婚相談所が向いているんですよね。"))
    nodes.append(sp())

    # Section 4: 社会構造の話
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("年齢とともに変わる、婚活の“構造”の話"))
    nodes.append(sp())
    nodes.append(p("ちょっと、社会の構造のお話もさせてください。"))
    nodes.append(sp())
    nodes.append(p("20代のうちは、就職したばかりで、ライバルとの差ってそんなに大きくないんです。"))
    nodes.append(p("でも、年齢が上がるにつれて、年収やキャリアの差はどんどん開いていきます。"))
    nodes.append(p("特定の業種や役職についている人と、そうでない人の差が、プロフィールの上でもはっきり見えてくるようになる。"))
    nodes.append(sp())
    nodes.append(p("それから、お相手になる女性の側にも変化が起きます。"))
    nodes.append(sp())
    nodes.append(p("20代の女性には、申し込みが集中しやすいけれど、相手の人数自体は限られている。"))
    nodes.append(p("でも、年齢が上がってくると、その女性に対して年下の男性からも、年上の男性からも、申し込みが入るようになるんです。"))
    nodes.append(p("しかも結婚相談所に入会している男女のボリュームゾーンは30代。"))
    nodes.append(p("つまり、ライバルの数そのものが、年齢とともに増えていく構造になっているんですよね。"))
    nodes.append(sp())
    nodes.append(p("これは、誰のせいでもなく、ただの構造の話です。"))
    nodes.append(p("だからこそ、知っておくと、動き方が変わってくると思うんです。"))
    nodes.append(sp())

    # Section 5: 対処法（行動レベル＋根本）
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("今日からできる、小さな一歩"))
    nodes.append(sp())
    nodes.append(p("じゃあ、どうしたらいいのか。"))
    nodes.append(sp())
    nodes.append(p("まず行動レベルでは、ものすごくシンプルです。"))
    nodes.append(p("「気になるプロフィールがあったら、申し込んでみる」。"))
    nodes.append(p("それだけでいいんです。"))
    nodes.append(p("お見合いが決まれば、あとは相談所がサポートしながら、一歩ずつ進めていけます。"))
    nodes.append(p("一人で抱え込む必要は、まったくありません。"))
    nodes.append(sp())

    if img2:
        nodes.append(image_node(img2["url"], "気になるプロフィールに、まず一歩踏み出してみる"))
        nodes.append(sp())

    nodes.append(p("そしてもう一つ、根本的なところで大事なのが、「まだ大丈夫」という思い込みに、ちょっとだけ気づいてあげること。"))
    nodes.append(sp())
    nodes.append(p("それは事実というより、さっきお話しした“反応パターン”かもしれない。"))
    nodes.append(p("そう捉え直すだけで、「じゃあ、ちょっと動いてみようかな」という気持ちが、自然と芽生えてくることがあるんですよね。"))
    nodes.append(sp())

    # Section 6: 希望の着地
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("想像してみてください"))
    nodes.append(sp())
    nodes.append(p("仕事から帰ってきた夜。"))
    nodes.append(p("玄関を開けると、「お疲れさま」って迎えてくれる人がいる。"))
    nodes.append(p("今日あったことを、ちょっとだけ話せる相手がいる。"))
    nodes.append(p("一緒にごはんを食べながら、たわいもないことで笑い合える時間がある。"))
    nodes.append(sp())

    if img1:
        nodes.append(image_node(img1["url"], "仕事から帰った夜に、待っていてくれる人がいる暮らし"))
        nodes.append(sp())

    nodes.append(p("それは、遠い未来の話ではなくて、今、動き始めることで、案外早く手に入る景色なんですよね。"))
    nodes.append(sp())
    nodes.append(p("仕事を頑張りたい気持ちも、家庭を持ちたい気持ちも、本当は両方とも、あなた自身の本音から出てきているものだと思うんです。"))
    nodes.append(p("どちらかを諦める必要なんて、まったくありません。"))
    nodes.append(sp())
    nodes.append(p("じんわりとですが、確かに、両方を手にしている人たちを、私はこれまでにたくさん見てきました。"))
    nodes.append(p("だから、安心して、一歩を踏み出してみてくださいね。"))
    nodes.append(sp())

    # CTA（中央寄せ）
    nodes.append(link_node("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"))

    return nodes


def main():
    title = "「結婚はまだ先でいい」と思っていた男性たちが、後から気づいたこと"
    excerpt = ("「結婚はまだ先で大丈夫」——そう思っていた30代の男性たちに、聞いてみました。"
               "仕事も大事にしながら、実は早めに動くことが力になる理由を、心理学や社会の構造もまじえてお伝えします。"
               "仕事も家庭も、両方を手に入れる人がやっていたこととは。")
    meta_desc = ("「結婚はまだ先でいい」と思っている30代男性へ。仕事と結婚は両立できる理由、IBJガイドライン、"
                 "婚活の構造的な変化を心理カウンセラー仲人がやさしく解説。早めに動くことが力になります。")

    print("画像をWixにアップロード中...")
    cover = upload_image_binary(EYECATCH, "2026-06-11_eyecatch.png")
    img1  = upload_image_binary(BODY1, "2026-06-11_body1_evening_meal.png")
    img2  = upload_image_binary(BODY2, "2026-06-11_body2_profile_cafe.png")

    nodes = build_nodes(img1, img2)
    rich_content = {"nodes": nodes, "metadata": {"version": 1}}

    print("Wixに下書き作成中...")
    body = {
        "draftPost": {
            "title": title,
            "richContent": rich_content,
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "memberId": MEMBER_ID,
            "excerpt": excerpt,
            "relatedPostIds": RELATED_POST_IDS,
        }
    }
    r = requests.post(
        f"{WIX_BASE}/blog/v3/draft-posts",
        headers=wix_headers(),
        json=body,
        timeout=30,
    )
    if not r.ok:
        print(f"下書き作成失敗: {r.status_code} {r.text[:300]}")
        return
    draft = r.json().get("draftPost", {})
    draft_id = draft.get("id")
    print(f"下書き作成完了: {draft_id}")

    if cover and draft_id:
        print("カバー画像・メタ更新中...")
        patch_body = {
            "draftPost": {
                "coverMedia": {
                    "image": {"src": {"url": cover["url"]}}
                },
                "seoData": {
                    "description": meta_desc
                }
            },
            "fieldMask": "coverMedia,seoData.description"
        }
        rp = requests.patch(
            f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
            headers=wix_headers(),
            json=patch_body,
            timeout=30,
        )
        if rp.ok:
            print("カバー画像・メタ更新完了！")
        else:
            print(f"更新失敗: {rp.status_code} {rp.text[:200]}")

    print(f"\n完了！下書きID: {draft_id}")
    print("⚠️ Wixブログ管理画面で画像が正しく表示されているか必ず確認してください！")


if __name__ == "__main__":
    main()
