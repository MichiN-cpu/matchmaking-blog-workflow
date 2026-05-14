"""
漫画#3「結婚相談所の偏見、全部ひっくり返った話」ブログ投稿スクリプト
カテゴリ: 結婚相談所の始め方（IBJ・流れ・費用）
2026-05-14
"""
import os, re, time, uuid, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_ID = "0122d61b-14c6-42d9-a950-d4b527ea39d1"  # 結婚相談所の始め方
MANGA_PATH  = "/Users/nakashimamichi/Downloads/ChatGPT Image 2026年5月14日 07_34_29.png"

RELATED_POST_IDS = [
    "3f84d312-9c4f-40b7-8476-963876091b38",
    "99399e46-95ec-4da7-b44f-b9346f795bd3",
    "1c5083f2-484d-463d-a71a-fa70193ead42",
]

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "61acc4f3-6c16-4653-995b-dd6d9136c1d3",  # IBJ
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "8e779610-2acc-448e-b6b0-ad65dbb418d1",  # 無料相談
    "a8fd177f-b3ba-4a57-9f81-c26ba1ec0488",  # 婚活相談
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
    # 静的URLをそのまま使う（wix:image://v1/形式は表示されない既知の問題あり）
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
    """ローカルファイルをWixにアップロードしてURLを返す"""
    import base64, tempfile
    print(f"ローカル画像アップロード中: {display_name}")

    # Step1: アップロードURL取得（POST）
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
    print(f"アップロードURL取得: {upload_url[:80] if upload_url else 'None'}")

    if not upload_url:
        print(f"uploadUrl なし: {data}")
        return None

    # Step2: ファイルをPUT
    with open(local_path, "rb") as f:
        file_bytes = f.read()

    sep = "&" if "?" in upload_url else "?"
    put_url = f"{upload_url}{sep}filename={display_name}"
    put_r = requests.put(
        put_url,
        data=file_bytes,
        headers={"Content-Type": "image/png"},
        timeout=60,
    )
    if not put_r.ok:
        print(f"ファイルアップロード失敗: {put_r.status_code} {put_r.text[:200]}")
        return None
    print("ファイルアップロード完了。処理待ち...")

    # Step3: file_idで待機してURLを取得
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
                    print(f"アップロード完了: {url[:60]}...")
                    return {"url": url}
                print(f"待機中... ({fd.get('state')}, {i+1}/20)")
        print("タイムアウト")
        return None

    url = (resp_data.get("file") or {}).get("url") or resp_data.get("url")
    if url:
        return {"url": url}

    print(f"URLが取得できませんでした: {resp_data}")
    return None


def generate_cover_image():
    """gpt-image-1でカバー画像を生成してWixにアップロード"""
    import base64, tempfile, os as _os
    prompt = (
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A young Japanese woman (East Asian appearance, brown hair, soft pink dress) sitting "
        "across from a warm friendly mature Japanese woman in her 50s (professional beige suit) "
        "in a bright modern white office. The young woman looks relieved and pleasantly surprised. "
        "Clean bright atmosphere with indoor plants. Horizontal composition."
    )
    print("gpt-image-1 カバー画像生成中...")
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024",
        quality="medium",
        n=1,
    )

    img_data = resp.data[0]
    b64 = img_data.b64_json
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.write(base64.b64decode(b64))
    tmp.close()
    print(f"生成完了。Wixにアップロード中...")

    result = upload_local_image(tmp.name, "2026-05-14_manga3_cover.png")
    _os.unlink(tmp.name)
    return result


def build_nodes(manga_img=None):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # イントロ
    nodes.append(p("結婚相談所にこんなイメージありませんか？"))
    nodes.append(sp())
    nodes.append(p("「登録してる男性って…モテない人ばかりなんじゃ」"))
    nodes.append(p("「断れなくて変な人と会わされるんじゃないの」"))
    nodes.append(p("「なんか堅苦しそうで、自分には合わないかも」"))
    nodes.append(sp())
    nodes.append(p("今日はそのことを漫画にしました。"))
    nodes.append(sp())

    # 漫画画像
    if manga_img:
        nodes.append(image_node(manga_img["url"], "結婚相談所の偏見、全部ひっくり返った話"))
        nodes.append(sp())

    # セクション1
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h2("「モテない男性しかいない」は本当か"))
    nodes.append(sp())
    nodes.append(p("これ、かなり多い誤解です。"))
    nodes.append(sp())
    nodes.append(p("あすなる愛媛が加盟するIBJのネットワーク会員は100,000人以上。年齢・職業・年収・学歴の審査と独身証明の提出が入会の条件で、会社員・経営者・士業・公務員の方が中心です。"))
    nodes.append(sp())
    nodes.append(p("来てみた女性の方によく言われるんですよね。「なんでこんな人が相談所に来てるの？って思うくらいちゃんとしてる」って。"))
    nodes.append(sp())
    nodes.append(p("考えてみると、納得で。マッチングアプリで何十件もやりとりして疲れた、写真だけで判断される場が嫌になった、そういう経験の後に「もっと真剣な場で出会いたい」と来る方が多い。"))
    nodes.append(sp())
    nodes.append(p("アプリで疲れた人＝結婚に真剣な人、ということなんです。"))
    nodes.append(sp())

    # セクション2
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h2("「断れない」は思い込み"))
    nodes.append(sp())
    nodes.append(p("お断りは、普通のことです。"))
    nodes.append(sp())
    nodes.append(p("「断る＝相手を傷つける」という感覚、日本人は特に強い傾向があります。"))
    nodes.append(sp())
    nodes.append(p("でもね、考えてみてください。結婚できるのはたった1人だけ。お見合いした方みんな連れていくわけにはいきませんよね😊"))
    nodes.append(sp())
    nodes.append(p("だからお断りは責めることでも責められることでもなく、ごく自然なプロセスなんです。"))
    nodes.append(sp())
    nodes.append(p("ただ、「なんか違う気がする」の直感だけで次々とNGにし続けると、だんだん出会いの幅が狭くなっていくこともあって。その加減を一緒に考えるのも、仲人の役割のひとつだったりします。"))
    nodes.append(sp())
    nodes.append(p("罪悪感を持たなくて大丈夫ですよ、というのは、いつも最初にお伝えしていることのひとつです。"))
    nodes.append(sp())

    # セクション3
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h2("仲人がいることの、本当の価値"))
    nodes.append(sp())
    nodes.append(p("漫画の中に、こんな場面があります。"))
    nodes.append(sp())
    nodes.append(p("「結婚後の生活について、彼になんだか聞きにくくて…」"))
    nodes.append(sp())
    nodes.append(p("これ、すごくリアルな悩みだなあと思って入れたシーンです。"))
    nodes.append(sp())
    nodes.append(p("お付き合いが順調でも、お金のこと、住む場所のこと、仕事をどうするか…なんか急に聞きにくい、という感覚ってありませんか。"))
    nodes.append(sp())
    nodes.append(p("そういうとき「仲人からの宿題ということにしましょうか」という渡し方ができる。二人の間に入って、大事な話を自然に進めるのも、仲人の役割なんです。"))
    nodes.append(sp())
    nodes.append(p("愛着理論では、人は「安全基地」があるときに動けるようになると言われています。仲人が安全基地になって、安心してお互いを知っていける。それが結婚相談所の本質的な価値だと、私は思っています。"))
    nodes.append(sp())

    # 締め
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p("「来る前に想像していたこと、全部違いました。」"))
    nodes.append(sp())
    nodes.append(p("漫画の最後、こんなセリフで終わります。"))
    nodes.append(sp())
    nodes.append(p("偏見って、行動する前に足を止めてしまうもの。でも来てみたら「あ、こんな感じか」と思っていただけることがほとんどです。"))
    nodes.append(sp())
    nodes.append(p("「こっそり無料相談、予約した」でいいんです。誰かに言わなくていい。まず話だけ聞いてみてください。"))
    nodes.append(sp())

    # CTA（中央寄せ）
    nodes.append(cta_link_node("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"))

    return nodes


def main():
    title = "結婚相談所に偏見がある方へ。来てみたら、全部ちがいました。"
    excerpt = "「モテない男性しかいない」「断れない」「堅苦しそう」——結婚相談所にそんなイメージを持っていませんか？実際に来てみると、全部ちがいました。漫画で正直にお伝えします。"

    # 漫画画像アップロード
    manga_img = upload_local_image(MANGA_PATH, "2026-05-14_manga3_henken.png")

    # カバー画像生成
    cover = generate_cover_image()

    # richContent構築
    nodes = build_nodes(manga_img)
    rich_content = {"nodes": nodes, "metadata": {"version": 1}}

    # 下書き作成
    print("Wixに下書き作成中...")
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
    print("カバー画像・メタ更新中...")
    patch_body = {
        "draftPost": {
            "excerpt": excerpt,
            "relatedPostIds": RELATED_POST_IDS,
            "seoData": {
                "description": excerpt,
            },
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

    print(f"\n完了！下書きID: {draft_id}")
    print(f"タイトル: {title}")
    print(f"カテゴリ: 結婚相談所の始め方")
    print(f"漫画画像: {'アップロード済み' if manga_img else '失敗（手動で追加してください）'}")
    print(f"カバー画像: {'生成済み' if cover else '失敗（手動で追加してください）'}")
    print("⚠️ Wixブログエディターで画像が正しく表示されているか必ず確認してください")


if __name__ == "__main__":
    main()
