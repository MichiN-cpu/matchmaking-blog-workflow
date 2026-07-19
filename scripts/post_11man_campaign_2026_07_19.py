"""
会員11万名突破のいま、婚活を始めるあなたへ。入会金11,000円OFFキャンペーンのお知らせ
カテゴリ: お知らせ
2026-07-19
"""
import os, re, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = os.environ.get("WIX_SITE_ID", "d01daac5-b796-4bd3-b09b-6d9bbcc37573")
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

BANNER_PATH = "/Users/nakashimamichi/Downloads/11万人キャンペーン.jpg"

CATEGORY_IDS = [
    "fc247847-d52b-438c-ab23-95bae771dc0a",  # お知らせ
]

TAG_IDS = [
    "61acc4f3-6c16-4653-995b-dd6d9136c1d3",  # IBJ
    "32413ff0-17fc-455e-93e1-3add76e9eb46",  # キャンペーン
    "4e4f24d8-c0f5-4ff0-abb1-8f1422775843",  # 会員数
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "8e779610-2acc-448e-b6b0-ad65dbb418d1",  # 無料相談
    "4e730deb-5ff8-414c-a0ea-7fcde43eb113",  # 新規ご入会
]

RELATED_POST_IDS = [
    "c3d17505-356c-419e-9e6f-496bd4f04b1d",  # IBJ AWARD 2026年上期
    "b51edaff-47bb-4617-b55f-10906910deec",  # 乗り換え応援キャンペーン
    "1098fe45-b32f-4db4-bff4-1fb88d586097",  # 入会して1ヶ月で旅立っていく男性たち
]

TITLE = "会員11万名突破のいま、婚活を始めるあなたへ。入会金11,000円OFFキャンペーンのお知らせ"
EXCERPT = "IBJ全体の会員数が11万名を突破したことを記念し、入会金11,000円OFFの期間限定キャンペーンを実施中です。クーポン利用期間は7/18(土)〜8/16(日)、9/13(日)までのご入会が対象。数字の意味と、動くタイミングについてお伝えします。"
SEO_DESC = "IBJ会員数11万名突破を記念した入会金11,000円OFFキャンペーンのお知らせ。クーポン利用期間は7/18〜8/16、9/13までの入会が対象です。心理カウンセラー仲人が、数字の意味と動くタイミングについて解説します。"

IMAGE_PROMPT = {
    "prompt": (
        "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, no text. "
        "A beautiful Japanese woman in her late 20s to 30s, elegant refined features, model-like appearance, clear skin, "
        "standing outdoors on a bright city street, looking forward with a hopeful gentle smile, "
        "soft feminine outfit, hair down with gentle wave, "
        "real-world setting, professional lifestyle photography style, shallow depth of field, "
        "clean bright modern atmosphere, sense of new beginning and quiet optimism."
    ),
    "filename": "2026-07-19_11man_campaign_hope.png",
    "caption": "",
}

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


def upload_image_binary(image_bytes, filename, mime="image/png"):
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": mime, "displayName": filename},
        timeout=30,
    )
    if not r.ok:
        print(f"  アップロードURL取得失敗: {r.status_code}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        print(f"  uploadUrl取得失敗: {data}")
        return None
    sep  = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": mime, "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print(f"  アップロード失敗: {ru.status_code} {ru.text[:200]}")
        return None
    file_obj = ru.json().get("file", {})
    url = file_obj.get("url", "")
    fid = file_obj.get("id", "")
    if not url:
        print(f"  URL取得失敗: {ru.json()}")
        return None
    m = re.search(r"/media/([^?#\s]+)", url)
    print(f"  → {url[:70]}...")
    return {"url": url, "id": m.group(1) if m else fid}


def generate_and_import_image(prompt, filename):
    print(f"\n[gpt-image-1] 生成中: {filename}")
    resp = client.images.generate(
        model="gpt-image-1", prompt=prompt, size="1536x1024", quality="high", n=1,
    )
    img_data = resp.data[0]
    if not img_data.b64_json:
        print("  b64_json取得失敗")
        return None
    print("  生成完了。Wixにアップロード中...")
    return upload_image_binary(base64.b64decode(img_data.b64_json), filename)


def upload_banner():
    print(f"\n[banner] アップロード中: {BANNER_PATH}")
    with open(BANNER_PATH, "rb") as f:
        image_bytes = f.read()
    return upload_image_binary(image_bytes, "2026-07-19_11man_campaign_banner.jpg", mime="image/jpeg")


def build_nodes(img_banner=None, img_hope=None):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # イントロ
    nodes.append(p("今日は、ちょっと嬉しいご報告と、それに合わせたキャンペーンのお知らせです。"))
    nodes.append(sp())
    nodes.append(p("私たちが加盟しているIBJ（日本結婚相談所連盟）の会員数が、このたび11万名を突破しました。"))
    nodes.append(sp())
    nodes.append(p("「へえ、そうなんだ」で終わらせてもいい話なんですが、実はこれ、婚活を考えている方にとって、地味にすごく大事な数字だったりするんです。"))
    nodes.append(sp())

    if img_banner:
        nodes.append(image_node(img_banner["url"], ""))
        nodes.append(sp())

    # セクション1
    nodes.extend(section("「11万名」という数字が、実はあなたの背中を押してくれる理由"))
    nodes.append(sp())
    nodes.append(p("今日は、その理由を少しだけ、心理学と社会学の視点も交えてお話しさせてください。"))
    nodes.append(sp())
    nodes.append(p("まず単純に、母数が大きいというのは、出会える確率そのものが上がるということです。"))
    nodes.append(sp())
    nodes.append(p("これは当たり前のようで、婚活においてはかなり本質的な話で。"))
    nodes.append(sp())
    nodes.append(p("通信の世界に「ネットワーク効果」という考え方があります。"))
    nodes.append(sp())
    nodes.append(p("参加者が増えれば増えるほど、そのネットワーク全体の価値は掛け算的に大きくなる、という理論です。"))
    nodes.append(sp())
    nodes.append(p("電話が1台しかなければ誰にも繋がりませんが、100万台あれば無限の組み合わせが生まれますよね。"))
    nodes.append(sp())
    nodes.append(p("婚活のマッチングも、実はこれと同じ構造をしているんです。"))
    nodes.append(sp())
    nodes.append(p("会員数が増えるほど、年齢・価値観・ライフスタイルの組み合わせの幅が広がって、「自分にちょうどいい人」に出会える可能性が単純に上がっていく。"))
    nodes.append(sp())
    nodes.append(p("もうひとつ、心理学的な話もさせてください。"))
    nodes.append(sp())
    nodes.append(p("社会心理学に「社会的証明」という考え方があります。"))
    nodes.append(sp())
    nodes.append(p("多くの人がすでに選んでいるものは、それだけで「安心して選べるもの」に感じられる、という人の心の働きです。"))
    nodes.append(sp())
    nodes.append(p("11万人という数字は、それだけの人が「結婚相談所という選択」に一歩を踏み出した証でもあります。"))
    nodes.append(sp())
    nodes.append(p("あなただけが特別に勇気を試されているわけじゃない、というのが、私はすごく大事だと思っていて。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、この数字を見て「私も」と思っていただけたら嬉しいです。"))
    nodes.append(sp())

    # セクション2（キャンペーン詳細）
    nodes.extend(section("11万名突破を記念した、入会金11,000円OFFキャンペーン"))
    nodes.append(sp())
    nodes.append(p("そしてこのたび、この11万名突破を記念して、入会金が11,000円（税込）OFFになるキャンペーンが始まりました。"))
    nodes.append(sp())
    nodes.append(p("内容をまとめますね。"))
    nodes.append(sp())
    nodes.append(p("【キャンペーン内容】入会金 11,000円（税込）OFF"))
    nodes.append(sp())
    nodes.append(p("【クーポン利用期間】2026年7月18日（土）〜2026年8月16日（日）"))
    nodes.append(sp())
    nodes.append(p("【ご注意】クーポンご利用の上でのご入会は、2026年9月13日（日）までが対象となります。"))
    nodes.append(sp())
    nodes.append(p("無料相談にお越しいただいた際、「キャンペーンを見た」とひとことお伝えいただくだけで大丈夫です。"))
    nodes.append(sp())
    nodes.append(p("タイミングって、不思議なもので。"))
    nodes.append(sp())
    nodes.append(p("「そろそろかな」と思っていたときに、こういうお知らせが目に入るのも、何かのご縁なんじゃないかと、私は思っています。"))
    nodes.append(sp())

    # セクション3
    nodes.extend(section("「今じゃなくてもいいかな」と思ったあなたへ"))
    nodes.append(sp())
    nodes.append(p("キャンペーンのお話をすると、決まって出てくる反応があります。"))
    nodes.append(sp())
    nodes.append(p("「今はまだ、そのタイミングじゃないかも」という気持ちです。"))
    nodes.append(sp())
    nodes.append(p("これ、すごくよくわかるんです。"))
    nodes.append(sp())
    nodes.append(p("かつての私も、何かを決めるとき、「もう少し考えてから」が口癖でした（笑）。"))
    nodes.append(sp())
    nodes.append(p("でも心理学の世界には「決断疲れ」という言葉があります。"))
    nodes.append(sp())
    nodes.append(p("考える時間を延ばせば延ばすほど決断の質が良くなるわけではなく、むしろ選択そのものへのエネルギーが目減りしていく、という考え方です。"))
    nodes.append(sp())
    nodes.append(p("行動経済学者バリー・シュワルツも、選択肢が多すぎることがかえって人を動けなくさせる「選択のパラドックス」を指摘していて。"))
    nodes.append(sp())
    nodes.append(p("情報を集めれば集めるほど安心できるかというと、実はそうでもないんですよね。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、「話を聞くだけ」の無料相談から始めることを、私はいつもおすすめしています。"))
    nodes.append(sp())
    nodes.append(p("決めるための情報じゃなくて、決めなくていい安心感を、まず持ち帰ってもらえたらと思っていて。"))
    nodes.append(sp())

    if img_hope:
        nodes.append(image_node(img_hope["url"], ""))
        nodes.append(sp())

    # セクション4
    nodes.extend(section("数字の先にあるのは、ひとりひとりの物語"))
    nodes.append(sp())
    nodes.append(p("11万名という数字は、確かに大きな数字です。"))
    nodes.append(sp())
    nodes.append(p("でも私が日々お会いしているのは、その中のたった一人、目の前のあなたです。"))
    nodes.append(sp())
    nodes.append(p("数字が大きくなっても、私たちがお手伝いすることは変わりません。"))
    nodes.append(sp())
    nodes.append(p("あなたのペースで、あなたに合ったお相手と、ちゃんと向き合っていく。"))
    nodes.append(sp())
    nodes.append(p("その伴走をするために、私たちはここにいます。"))
    nodes.append(sp())
    nodes.append(p("11万名という数字を、他人事のニュースとしてではなく、「私もその中に入ってみようかな」のきっかけにしていただけたら、これほど嬉しいことはありません。"))
    nodes.append(sp())

    # CTA（中央寄せ）
    nodes.append(cta_node())

    return nodes


def main():
    # Step 1: バナー画像アップロード（カバー用）
    img_banner = upload_banner()

    # Step 2: 希望を感じさせる写真を1枚生成
    img_hope = generate_and_import_image(IMAGE_PROMPT["prompt"], IMAGE_PROMPT["filename"])

    # Step 3: richContent構築
    nodes = build_nodes(img_banner=img_banner, img_hope=img_hope)

    # Step 4: 下書き作成
    print("\n[Wix] 下書き作成中...")
    body = {
        "draftPost": {
            "title": TITLE,
            "memberId": MEMBER_ID,
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "relatedPostIds": RELATED_POST_IDS,
            "language": "ja",
            "richContent": {"nodes": nodes, "metadata": {"version": 1}},
            "excerpt": EXCERPT,
        }
    }
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(), json=body, timeout=30)
    if not r.ok:
        print(f"下書き作成失敗: {r.status_code} {r.text[:400]}")
        return
    draft_id = r.json().get("draftPost", {}).get("id")
    print(f"下書き作成完了: {draft_id}")

    # Step 5: カバー画像をPATCH（バナー画像を使用）
    if img_banner and draft_id:
        print("[Wix] カバー画像をPATCH中...")
        patch_media = {
            "draftPost": {
                "media": {
                    "wixMedia": {
                        "image": {
                            "id": img_banner["id"],
                            "url": img_banner["url"],
                        }
                    },
                    "displayed": True,
                    "custom": False,
                }
            },
            "fieldMask": "media"
        }
        rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
                            headers=wix_headers(), json=patch_media, timeout=30)
        print("カバー画像PATCH完了" if rp.ok else f"カバー画像PATCH失敗: {rp.status_code} {rp.text[:200]}")

    # Step 6: SEOディスクリプションをPATCH
    if draft_id:
        print("[Wix] SEOディスクリプションをPATCH中...")
        patch_seo = {
            "draftPost": {
                "seoData": {"description": SEO_DESC}
            },
            "fieldMask": "seoData.description"
        }
        rs = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
                            headers=wix_headers(), json=patch_seo, timeout=30)
        print("SEO PATCH完了" if rs.ok else f"SEO PATCH失敗: {rs.status_code} {rs.text[:200]}")

    print(f"\n完了")
    print(f"下書きID: {draft_id}")
    print(f"タイトル: {TITLE}")


if __name__ == "__main__":
    main()
