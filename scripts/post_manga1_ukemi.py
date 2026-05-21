"""
漫画#1「受け身をやめたら半年でご成婚できた話」ブログ投稿スクリプト
カテゴリ: 無料相談の前に読む（不安解消・向き不向き）
2026-05-21
"""
import os, time, uuid, base64, tempfile, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_ID = "641187e4-a409-4c2f-9639-ecc548f26f15"  # 無料相談の前に読む

MANGA_PATHS = [
    "/Users/nakashimamichi/Downloads/1_1.png",
    "/Users/nakashimamichi/Downloads/2_1.png",
    "/Users/nakashimamichi/Downloads/3_1.png",
    "/Users/nakashimamichi/Downloads/4_1.png",
]

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "8e779610-2acc-448e-b6b0-ad65dbb418d1",  # 無料相談
    "a8fd177f-b3ba-4a57-9f81-c26ba1ec0488",  # 婚活相談
]

RELATED_POST_IDS = [
    "78f3145c-452f-4f72-b1c0-e5964200b83e",  # 婚活沼②：1通だけ自分から申し込んでご成婚した話
    "56119732-3901-4782-bb84-528d3d09b1a8",  # 遠慮しない女性
    "3b824f3b-7b81-45e4-84ea-d5c0948d6b81",  # 仲人の反省・女性向け
]

client = OpenAI(api_key=OPENAI_KEY)


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


def h2(text):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": 2}}


def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}


def image_node(url, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": url}}, "caption": caption}}


def cta_link_node(text, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": text,
            "decorations": [{"type": "LINK", "linkData": {
                "link": {"url": url, "target": "BLANK"}
            }}]
        }}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}


def upload_local_image(local_path, display_name):
    print(f"アップロード中: {display_name}")
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"displayName": display_name, "mimeType": "image/png"},
        timeout=30,
    )
    if not r.ok:
        print(f"アップロードURL取得失敗: {r.status_code} {r.text[:300]}")
        return None

    data = r.json()
    upload_url = data.get("uploadUrl")
    file_id = data.get("fileId") or (data.get("file") or {}).get("id")
    if not upload_url:
        print(f"uploadUrlなし: {data}")
        return None

    with open(local_path, "rb") as f:
        file_bytes = f.read()

    sep = "&" if "?" in upload_url else "?"
    put_r = requests.put(
        f"{upload_url}{sep}filename={display_name}",
        data=file_bytes,
        headers={"Content-Type": "image/png"},
        timeout=60,
    )
    if not put_r.ok:
        print(f"ファイルアップロード失敗: {put_r.status_code} {put_r.text[:200]}")
        return None
    print("アップロード完了。処理待ち...")

    resp_data = {}
    try:
        resp_data = put_r.json()
    except Exception:
        pass
    if not file_id:
        file_id = resp_data.get("fileId") or (resp_data.get("file") or {}).get("id")

    if file_id:
        for i in range(20):
            time.sleep(3)
            chk = requests.get(
                f"{WIX_BASE}/site-media/v1/files/{file_id}",
                headers={"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID},
                timeout=15,
            )
            if chk.ok:
                fd = chk.json().get("file", {})
                if fd.get("state") in ("READY", "OK"):
                    url = fd.get("url", "")
                    print(f"完了: {url[:60]}...")
                    return {"url": url}
                print(f"待機中... ({fd.get('state')}, {i+1}/20)")
        print("タイムアウト")
        return None

    url = (resp_data.get("file") or {}).get("url") or resp_data.get("url")
    if url:
        return {"url": url}
    print(f"URLが取得できませんでした: {resp_data}")
    return None


def generate_ai_image(prompt, filename):
    print(f"AI画像生成中: {filename}")
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024",
        quality="medium",
        n=1,
    )
    b64 = resp.data[0].b64_json
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.write(base64.b64decode(b64))
    tmp.close()
    result = upload_local_image(tmp.name, filename)
    os.unlink(tmp.name)
    return result


def build_nodes(manga_imgs, body_img1, body_img2):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # イントロ
    nodes.append(p("今日は、あすなる愛媛のホームページに掲載した漫画「受け身をやめたら半年でご成婚できた話」を、もう少し掘り下げてお伝えしたいと思います。"))
    nodes.append(sp())
    nodes.append(p("漫画の主人公は30代の女性。婚活を始めてしばらく、なんとなくうまくいかないまま時間が過ぎていました。でも、あることに気づいて行動を変えたら、半年でご成婚退会になったんです。"))
    nodes.append(sp())
    nodes.append(p("「あること」って何だと思いますか？"))
    nodes.append(sp())
    nodes.append(p("実はそれ、「待つのをやめた」ということでした。"))
    nodes.append(sp())

    # 漫画4枚
    captions = [
        "受け身をやめたら半年でご成婚できた話（1/4）",
        "受け身をやめたら半年でご成婚できた話（2/4）",
        "受け身をやめたら半年でご成婚できた話（3/4）",
        "受け身をやめたら半年でご成婚できた話（4/4）",
    ]
    for i, img in enumerate(manga_imgs):
        if img:
            nodes.append(image_node(img["url"], captions[i]))
            nodes.append(sp())

    # セクション1：ミニ診断
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h2("「待っている」に、心当たりはありませんか"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("気になるプロフィールを見つけても、「向こうから申し込んでくれるかも」と待っています。"))
    nodes.append(p("仮交際中、彼からのLINEを「返信がくるまで待っています」。"))
    nodes.append(p("デートの場所も、食事のメニューも、「彼が決めてくれたら…」と思っています。"))
    nodes.append(p("真剣交際に進む話も、「向こうから言ってきたら」と待っています。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方、このあとの話がきっと役に立ちます。"))
    nodes.append(sp())
    nodes.append(p("「待つ」って、女性らしいことのように思えますよね。"))
    nodes.append(sp())
    nodes.append(p("押しつけがましくない、控えめな、いい女性の姿……という感覚、私にもありました（笑）。"))
    nodes.append(sp())
    nodes.append(p("でもね、婚活の場では「待つ」が逆効果になることが、けっこう多いんです。"))
    nodes.append(sp())

    # body image 1
    if body_img1:
        nodes.append(image_node(body_img1["url"], "気になる人に、自分から申し込む。その一歩が、ご縁を動かします。"))
        nodes.append(sp())

    # セクション2：右利き比喩＋反応パターン
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h2("受け身は「性格」ではなく「反応パターン」です"))
    nodes.append(sp())
    nodes.append(p("右利きの人が「左手でお箸を持とう」と思ったら、ものすごいエネルギーが要りますよね。"))
    nodes.append(sp())
    nodes.append(p("それと同じで、婚活の反応にも「慣れたパターン」があります。"))
    nodes.append(sp())
    nodes.append(p("受け身でいることは、性格の問題ではないんです。"))
    nodes.append(sp())
    nodes.append(p("ずっとそのほうが「安全だった」から、そのパターンが定着しているだけ。"))
    nodes.append(sp())
    nodes.append(p("かつての私もそうでした。"))
    nodes.append(sp())
    nodes.append(p("好きな人の前では黙って待つ。嫌われたくないから、自分の意見は後まわし。相手のペースに合わせて、合わせて、合わせているうちに——なぜか関係が薄れていく。"))
    nodes.append(sp())
    nodes.append(p("不安は性格ではなく、反応パターンなんですよね。"))
    nodes.append(sp())
    nodes.append(p("そしてパターンは、気づけば変えられます。"))
    nodes.append(sp())

    # セクション3：行動レベルの解決策
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h2("まず「気になる人に、自分から申し込む」ことから"))
    nodes.append(sp())
    nodes.append(p("じゃあ、まず何をすればいいの？というお話をしますね。"))
    nodes.append(sp())
    nodes.append(p("一番最初の一歩は、「気になる人に自分から申し込む」ことです。"))
    nodes.append(sp())
    nodes.append(p("これ、けっこう勇気が要りますよね。"))
    nodes.append(sp())
    nodes.append(p("断られたらどうしよう、という気持ちもよくわかります。"))
    nodes.append(sp())
    nodes.append(p("でも、申し込みは「私はあなたに興味があります」という、最初の小さな自己表現なんです。"))
    nodes.append(sp())
    nodes.append(p("待っているだけでは、気になっている人とのご縁は動き出しません。"))
    nodes.append(sp())
    nodes.append(p("交際が始まってからも同じです。「このお店が好きです」「次回はここに行ってみたいな」——大きな話でなくていいんです。"))
    nodes.append(sp())
    nodes.append(p("自分の気持ちを小出しに届けていくことで、相手もあなたのことをもっと知りたくなります。"))
    nodes.append(sp())
    nodes.append(p("関係はお互いに作るものです。受け取るだけでなく、届けることも大事なんですよね。"))
    nodes.append(sp())

    # body image 2
    if body_img2:
        nodes.append(image_node(body_img2["url"], "「待つ」の奥に何があるのか。一緒に見ていきましょう。"))
        nodes.append(sp())

    # セクション4：心理的深掘り
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h2("「学習されたもの」は、再学習できます"))
    nodes.append(sp())
    nodes.append(p("そして、もう一段深いところで起きていることがあります。"))
    nodes.append(sp())
    nodes.append(p("「待つ」ことが染みついている方は、どこかで「自分の意見を出すと嫌われる」と感じていることが多いんです。"))
    nodes.append(sp())
    nodes.append(p("これは思い込みではなく、過去の経験から学んだ反応パターンです。"))
    nodes.append(sp())
    nodes.append(p("たとえば子供の頃、自分の意見を言ったら否定されたとか、目立つと怒られたとか。そういう経験が積み重なると、無意識に「黙っていれば安全」という反応が定着していきます。"))
    nodes.append(sp())
    nodes.append(p("心理学では「学習された無力感」とも呼ばれます。"))
    nodes.append(sp())
    nodes.append(p("でも「学習されたもの」であれば、「再学習」もできます。"))
    nodes.append(sp())
    nodes.append(p("カウンセリングでこのパターンに気づいて少しずつ緩めていくと、婚活だけでなく、日常のあちこちで「自分の気持ちを言える感覚」が育ってきます。"))
    nodes.append(sp())

    # セクション5：漫画の事例
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h2("漫画の主人公が変えた、たった一つのこと"))
    nodes.append(sp())
    nodes.append(p("漫画の主人公も、最初はそういう女性でした。"))
    nodes.append(sp())
    nodes.append(p("お見合い申し込みは全部「待ち」。仮交際でも、自分の気持ちを出せずにいた。それが半年以上続いていたんです。"))
    nodes.append(sp())
    nodes.append(p("でも、仲人とのセッションを重ねる中で「待つことが自分を守る手段だった」と気づきました。"))
    nodes.append(sp())
    nodes.append(p("そして勇気を出して、ずっと気になっていた人に自分から申し込んだ。"))
    nodes.append(sp())
    nodes.append(p("そのお見合いが、ご成婚に繋がりました。"))
    nodes.append(sp())

    # 締め・希望着地
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p("婚活がうまくいかないとき、「私には縁がないのかも」と思いがちです。"))
    nodes.append(sp())
    nodes.append(p("でも多くの場合、縁の問題ではありません。"))
    nodes.append(sp())
    nodes.append(p("受け身というパターンが、せっかくの縁を薄くしているだけなんです。"))
    nodes.append(sp())
    nodes.append(p("それは変えられます。ちゃんと、変えられるんです。"))
    nodes.append(sp())
    nodes.append(p("一緒にごはんを食べながら「これ好きなんだよね」って自然に言える日。"))
    nodes.append(p("彼が「もっと聞かせて」って前のめりになってくれる日。"))
    nodes.append(sp())
    nodes.append(p("その感覚、遠くないですよ。"))
    nodes.append(sp())

    # 今週の一歩
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h2("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("気になるプロフィールを見つけたら、今日中に申し込んでみてください。"))
    nodes.append(sp())
    nodes.append(p("完璧なタイミングなんてありません。"))
    nodes.append(sp())
    nodes.append(p("「気になる」と感じたその瞬間が、動くサインです。"))
    nodes.append(sp())

    # CTA（中央寄せ）
    nodes.append(cta_link_node("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"))

    return nodes


def main():
    title    = "【女性向け】受け身をやめたら、半年でご成婚できた話。——「待つ」から「届ける」へ。"
    excerpt  = "「好きになったら、待つ」——ほとんどの女性が持っている感覚ですが、婚活では逆効果になることも。お見合い申し込みも仮交際も、「待つ」から「届ける」へ変えるだけで、縁の流れが変わります。愛媛・松山の結婚相談所あすなる愛媛より。"

    # 漫画4枚アップロード
    print("=== 漫画パネル4枚アップロード ===")
    manga_imgs = []
    for i, path in enumerate(MANGA_PATHS, 1):
        img = upload_local_image(path, f"2026-05-21_manga1_panel{i}.png")
        manga_imgs.append(img)

    # カバー画像生成
    print("\n=== カバー画像生成 ===")
    cover = generate_ai_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A young East Asian woman (black hair, soft floral dress) confidently looking at a smartphone "
        "screen with a warm smile, about to send a message. Bright hopeful atmosphere, cherry blossom "
        "petals floating gently. Horizontal composition.",
        "2026-05-21_manga1_cover.png"
    )

    # ボディ画像1生成（申し込みシーン）
    print("\n=== ボディ画像1生成 ===")
    body_img1 = generate_ai_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A young East Asian woman in her 30s (black hair, casual elegant outfit) sitting at a desk, "
        "looking at a tablet showing profile photos with a thoughtful yet determined expression, "
        "finger hovering over the screen as if about to tap. Warm indoor lighting.",
        "2026-05-21_manga1_body1.png"
    )

    # ボディ画像2生成（カウンセリングシーン）
    print("\n=== ボディ画像2生成 ===")
    body_img2 = generate_ai_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "An East Asian woman in her 30s talking with a kind warm middle-aged female counselor in a "
        "bright cozy counseling room. Both seated facing each other, the counselor listening with a "
        "gentle reassuring smile, the young woman looking relieved and engaged. Indoor plants nearby.",
        "2026-05-21_manga1_body2.png"
    )

    # richContent構築
    nodes = build_nodes(manga_imgs, body_img1, body_img2)
    rich_content = {"nodes": nodes, "metadata": {"version": 1}}

    # 下書き作成
    print("\n=== Wix下書き作成 ===")
    body = {
        "draftPost": {
            "title": title,
            "richContent": rich_content,
            "categoryIds": [CATEGORY_ID],
            "tagIds": TAG_IDS,
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
        print(f"下書き作成失敗: {r.status_code} {r.text[:300]}")
        return
    draft = r.json().get("draftPost", {})
    draft_id = draft.get("id")
    print(f"下書き作成完了: {draft_id}")

    # カバー画像・メタ・関連記事・抜粋を更新
    print("=== メタデータ更新 ===")
    patch_body = {
        "draftPost": {
            "excerpt": excerpt,
            "relatedPostIds": RELATED_POST_IDS,
            "seoData": {"description": excerpt},
        },
        "fieldMask": "excerpt,relatedPostIds,seoData.description"
    }
    if cover:
        patch_body["draftPost"]["coverMedia"] = {"image": {"src": {"url": cover["url"]}}}
        patch_body["fieldMask"] += ",coverMedia"

    rp = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
        headers=wix_headers(),
        json=patch_body,
        timeout=30,
    )
    if rp.ok:
        print("メタ更新完了")
    else:
        print(f"メタ更新失敗: {rp.status_code} {rp.text[:200]}")

    print(f"\n{'='*50}")
    print(f"完了！下書きID: {draft_id}")
    print(f"タイトル: {title}")
    print(f"カテゴリ: 無料相談の前に読む")
    print(f"漫画パネル: {sum(1 for x in manga_imgs if x)}/4枚アップロード済み")
    print(f"カバー画像: {'生成済み' if cover else '失敗（手動で追加してください）'}")
    print(f"ボディ画像: {sum(1 for x in [body_img1, body_img2] if x)}/2枚生成済み")
    print("⚠️ Wixブログエディターで画像が正しく表示されているか必ず確認してください")


if __name__ == "__main__":
    main()
