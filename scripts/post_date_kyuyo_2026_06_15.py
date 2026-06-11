"""
【男女共通】向かい合って話すだけが、デートじゃない。仮交際中の「なんか疲れる」をリフレッシュに変える話。
カテゴリ: 仮交際（3f5f378d-a4f4-47e0-90a7-ab4daa27504e）
公開予定: 2026-06-15（日）下書き保存のみ
"""
import os, re, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["3f5f378d-a4f4-47e0-90a7-ab4daa27504e"]

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "1c7a4d95-e95b-492a-93e2-da1c8a63ab9b",  # デート
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "27815c19-e4df-4f86-9949-70c119f752d2",  # 書籍
]

RELATED_POST_IDS = [
    "78d9e1c5-9567-4c4c-a7d8-9b318a131ee9",  # 「どこ行こうか」から、ふたりは始まる
    "36915afc-e0aa-4b34-898b-106f66f11f33",  # 仮交際中、彼からLINEが来ない
    "8dc13d85-b85f-4247-8a8b-8ed90bad6bdc",  # 媚びるな、危険
]

TITLE   = "【男女共通】向かい合って話すだけが、デートじゃない。仮交際中の「なんか疲れる」をリフレッシュに変える話。"
EXCERPT = "仮交際中のデートで「なんか疲れる」と感じていませんか？それはデートの設計の問題かもしれません。片野秀樹さんの休養学の視点から、二人でリフレッシュできるデートの組み立て方をご紹介します。"
SEO_DESC = EXCERPT

INFOGRAPHIC_PATH = os.path.expanduser("~/Downloads/休養学まとめ.png")

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, no text. "
            "A Japanese couple in their 30s walking side by side on a bright riverside path, "
            "relaxed and smiling, looking forward not at camera, black hair, "
            "clean bright modern atmosphere, professional lifestyle photography, shallow depth of field."
        ),
        "filename": "2026-06-15_date_kyuyo_eyecatch.png",
        "caption": "",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural daylight, East Asian appearance, no text. "
            "A Japanese couple in their 30s cooking together in a bright modern kitchen, "
            "smiling and engaged in the activity, side by side, black hair, "
            "clean contemporary interior, natural light, professional lifestyle photography."
        ),
        "filename": "2026-06-15_date_kyuyo_cooking.png",
        "caption": "一緒に作った記憶が、関係の土台になる",
    },
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


def p_bold(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": text,
            "decorations": [{"type": "BOLD", "boldData": {"bold": True}}]
        }}
    ], "paragraphData": {}}


def p_with_link(before, link_text, link_url, after=""):
    nodes = []
    if before:
        nodes.append({"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": before, "decorations": []}})
    nodes.append({"type": "TEXT", "id": nid(), "nodes": [], "textData": {
        "text": link_text,
        "decorations": [{"type": "LINK", "linkData": {"link": {"url": link_url, "target": "BLANK"}}}]
    }})
    if after:
        nodes.append({"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": after, "decorations": []}})
    return {"type": "PARAGRAPH", "id": nid(), "nodes": nodes, "paragraphData": {}}


def h(text, level=2):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": level}}


def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}


def section(heading_text):
    return [sp(), divider_node(), sp(), h(heading_text)]


def image_node(url, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": url}}, "caption": caption}}


def cta_node():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": "⬇️あなたに合った婚活を。無料相談はこちらから！⬇️",
            "decorations": [{"type": "LINK", "linkData": {
                "link": {"url": "https://www.asunaru.jp/soudan", "target": "BLANK"}
            }}]
        }}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}


def upload_image_binary(image_bytes, filename):
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "displayName": filename},
        timeout=30,
    )
    if not r.ok:
        print(f"  アップロードURL取得失敗: {r.status_code} {r.text[:200]}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        print(f"  uploadUrl取得失敗: {data}")
        return None
    sep  = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print(f"  アップロード失敗: {ru.status_code} {ru.text[:200]}")
        return None
    file_obj = ru.json().get("file", {})
    url = file_obj.get("url", "")
    if not url:
        print(f"  URL取得失敗: {ru.json()}")
        return None
    print(f"  → {url[:80]}...")
    return url


def generate_and_upload_image(prompt, filename):
    print(f"\n[gpt-image-1] 生成中: {filename}")
    resp = client.images.generate(
        model="gpt-image-1", prompt=prompt, size="1536x1024", quality="high", n=1,
    )
    img_data = resp.data[0]
    if not img_data.b64_json:
        print("  b64_json取得失敗")
        return None
    img_bytes = base64.b64decode(img_data.b64_json)
    save_path = os.path.join(os.path.dirname(__file__), f"../drafts/images/{filename}")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(img_bytes)
    print("  生成完了。Wixにアップロード中...")
    return upload_image_binary(img_bytes, filename)


def build_nodes(url_eyecatch, url_infographic, url_cooking):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # イントロ・共感
    nodes.append(p("仮交際が始まって、デートを重ねていくうちに、こんな感覚がやってくることがあります。"))
    nodes.append(sp())
    nodes.append(p("デートは楽しいはずなのに、なんとなく疲れる。"))
    nodes.append(p("話すことが少なくなってきた気がする。"))
    nodes.append(p("ランチの後、ディナーの後、なんとなくどっと来る感じがある。"))
    nodes.append(sp())
    nodes.append(p("こんな心当たり、ありませんか。"))
    nodes.append(sp())
    nodes.append(p("——そういうとき、多くの方が「もしかしてこの人と相性が悪いのかな」と思い始めます。でもね、少し待ってほしいんです。"))
    nodes.append(sp())
    nodes.append(p_bold("疲れるのは「デートの設計」のせいかもしれません。"))
    nodes.append(sp())
    nodes.append(p("「デートで疲れやすいんです」——それは体質でも性格でもなく、デートの組み立て方のパターンの話かもしれないんです。右利きの人が左手だけで一日を過ごしたら疲れるように、同じ種類のことだけを繰り返していると、どんなに好きな相手でも消耗してきます。それだけのことです。"))
    nodes.append(sp())

    if url_eyecatch:
        nodes.append(image_node(url_eyecatch, "並んで歩くだけで、二人の距離が縮まる"))
        nodes.append(sp())

    # セクション1
    nodes.extend(section("「話すデート」は、休養の一種類しか使っていない"))
    nodes.append(sp())
    nodes.append(p("少し面白い話をしますね。"))
    nodes.append(sp())
    nodes.append(p_with_link(
        "休養学という分野があります。スポーツ科学者の片野秀樹さんが著書『",
        "休養学",
        "https://amzn.to/4uYCUvT",
        "』でまとめていらっしゃるのですが、休養には「親交」「休息」「運動」「娯楽」「創作・想像」「栄養」「転換」の7つのタイプがあります。"
    ))
    nodes.append(sp())
    nodes.append(p("カフェやレストランで向かい合って話すデート。これは「親交」という種類の休養です。大切な人と話してつながること——それ自体は、とても大事なことをしているんです。"))
    nodes.append(sp())
    nodes.append(p("ただ、デートのたびに「親交」だけをずっと続けていると、少し疲れてくる。これは相手が嫌いになったわけでも、話題が尽きたわけでもありません。一種類の休養だけを使い続けているからです。"))
    nodes.append(sp())

    if url_infographic:
        nodes.append(image_node(url_infographic, "片野秀樹『休養学』をもとに作成"))
        nodes.append(sp())

    # セクション2
    nodes.extend(section("休養タイプを組み合わせると、デートが変わります"))
    nodes.append(sp())
    nodes.append(p("「7種類を全部取ろう！」と気負わなくていいんです。いつものデートに、一つだけ違う要素を足す。それだけで、デートの後の感触がずいぶん変わります。"))
    nodes.append(sp())

    nodes.append(h("休息 × デート", 3))
    nodes.append(sp())
    nodes.append(p("公園のベンチで、何も決めずにぼんやりする。岩盤浴でゆっくりする。同じ映画を並んで見る。向かい合って「話さなきゃ」という空気がない時間が、実は「一緒にいる安心感」を育てます。沈黙が苦にならなくなってきたら、それはかなりいい関係になっているサインです。"))
    nodes.append(sp())

    nodes.append(h("運動 × デート", 3))
    nodes.append(sp())
    nodes.append(p("二人でウォーキングする。サイクリング、ボウリング、ミニゴルフ。横に並んで同じ方向を向く時間は、自然と会話が生まれやすくなるんですよね。心理学では、面と向かって話すより肩を並べているほうが話しやすい、ということが知られています。「なんか今日、いつもよりよく話せたな」という感覚、体を動かしながら並んでいるときにやってきます。"))
    nodes.append(sp())

    nodes.append(h("娯楽 × デート", 3))
    nodes.append(sp())
    nodes.append(p("音楽のライブ、美術館、水族館、マーケット。「好きなもの」や「気になるもの」を共有すると、その人の内面が自然に見えてきます。どんな顔で笑うか、何に目を輝かせるか——そういう発見が、じわじわと愛着に変わります。"))
    nodes.append(sp())

    nodes.append(h("創作 × デート", 3))
    nodes.append(sp())
    nodes.append(p("料理教室、陶芸体験、フラワーアレンジメント。共同作業のときに、人の脳はオキシトシン（愛着に関わるホルモン）を出しやすくなることが研究で示されています。「二人で作ったね」という体験の記憶は、積み重なっていくたびに、関係の土台になります。"))
    nodes.append(sp())

    if url_cooking:
        nodes.append(image_node(url_cooking, "一緒に作った記憶が、関係の土台になる"))
        nodes.append(sp())

    nodes.append(h("栄養 × デート", 3))
    nodes.append(sp())
    nodes.append(p("ただ「食べる」から「一緒に選んで食べる」へ。週末の朝にパン屋さんへ行く、マルシェで気になる食材を買う、一緒に料理してみる。食のデートでも、一手間加わるだけで別の種類のリフレッシュになります。"))
    nodes.append(sp())

    nodes.append(h("転換 × デート", 3))
    nodes.append(sp())
    nodes.append(p("いつもと違う場所へ行く。行ったことのない街を歩く、ドライブで気まぐれに寄り道する。「いつもの自分」から少し離れる体験が、気分のリセットになります。非日常の空間で、二人の新しい一面が見えてくることもあります。"))
    nodes.append(sp())

    # 希望への着地
    nodes.extend(section("「一緒にいると、なんか元気になるな」"))
    nodes.append(sp())
    nodes.append(p("仮交際中は、デートのたびに「この人との相性、どうなんだろう」と確認しながら過ごしてしまいがちです。そういう目で相手を見ていると、どんなに良い人でも疲れてきます。"))
    nodes.append(sp())
    nodes.append(p("でも、「今日は二人でどこへ行こうか」「何をしようか」という感覚でデートを設計できるようになると、少しずつ空気が変わります。"))
    nodes.append(sp())
    nodes.append(p("向かい合って話すことが目的ではなく、一緒にいることが自然になる。相手を評価する時間が減って、ただ楽しむ時間が増える。そのうちに「この人と一緒にいると、なんか元気になるな」という感覚がやってきます。"))
    nodes.append(sp())
    nodes.append(p("その感覚が、愛着です。愛着が育った先に、結婚があります。"))
    nodes.append(sp())
    nodes.append(p("じんわり、でも確かに変わります。ぜひ、次のデートから試してみてください。"))
    nodes.append(sp())

    # 今週の一歩
    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("次のデートに、「食事＋会話」以外の要素を一つだけ加えてみてください。散歩でも、映画でも、一緒に料理でも。小さな一つで、十分です。"))
    nodes.append(sp())

    # CTA
    nodes.append(cta_node())

    return {"nodes": nodes}


def create_draft(rich_content):
    body = {
        "draftPost": {
            "title": TITLE,
            "memberId": MEMBER_ID,
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "richContent": rich_content,
        }
    }
    r = requests.post(
        f"{WIX_BASE}/blog/v3/draft-posts",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"下書き作成失敗: {r.status_code} {r.text[:300]}")
        return None
    return r.json().get("draftPost", {}).get("id")


def update_draft(post_id, cover_url):
    body = {
        "draftPost": {
            "coverMedia": {"image": {"src": {"url": cover_url}}},
            "excerpt": EXCERPT,
            "seoData": {"description": SEO_DESC},
            "relatedPostIds": RELATED_POST_IDS,
        },
        "fieldMask": "coverMedia,excerpt,seoData.description,relatedPostIds"
    }
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{post_id}",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"PATCH失敗: {r.status_code} {r.text[:300]}")
    return r.ok


def main():
    print("=== 休養学×デート記事 投稿スクリプト ===\n")

    # 1. インフォグラフィックをWixにアップロード
    print("[1] 休養学まとめ図をアップロード中...")
    if not os.path.exists(INFOGRAPHIC_PATH):
        print(f"  ファイルが見つかりません: {INFOGRAPHIC_PATH}")
        url_infographic = None
    else:
        with open(INFOGRAPHIC_PATH, "rb") as f:
            infographic_bytes = f.read()
        url_infographic = upload_image_binary(infographic_bytes, "2026-06-15_date_kyuyo_infographic.png")

    # 2. アイキャッチ生成
    print("\n[2] アイキャッチ画像を生成中...")
    url_eyecatch = generate_and_upload_image(IMAGE_PROMPTS[0]["prompt"], IMAGE_PROMPTS[0]["filename"])

    # 3. 料理シーン生成
    print("\n[3] 本文画像（料理シーン）を生成中...")
    url_cooking = generate_and_upload_image(IMAGE_PROMPTS[1]["prompt"], IMAGE_PROMPTS[1]["filename"])

    # 4. richContent構築
    print("\n[4] richContent構築中...")
    rich_content = build_nodes(url_eyecatch, url_infographic, url_cooking)

    # 5. 下書き作成
    print("\n[5] Wix下書き作成中...")
    post_id = create_draft(rich_content)
    if not post_id:
        print("失敗。終了します。")
        return

    print(f"  → 下書きID: {post_id}")

    # 6. カバー画像・抜粋・関連記事を更新
    if url_eyecatch:
        print("\n[6] カバー画像・抜粋・関連記事を更新中...")
        ok = update_draft(post_id, url_eyecatch)
        print(f"  → {'成功' if ok else '失敗'}")

    print(f"\n✅ 完了！\n下書きID: {post_id}")
    print("Wixブログ管理画面で確認してください。")


if __name__ == "__main__":
    main()
