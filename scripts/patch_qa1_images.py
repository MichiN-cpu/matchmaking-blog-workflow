"""
「あすなる愛媛のことを、もっと知ってほしい。よくある質問Q&A」
下書きID: 7c09a02f-c897-4fea-926c-993861c8110a
→ 画像3枚挿入 + タグ設定 + メタ説明
"""
import os, re, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
DRAFT_ID    = "7c09a02f-c897-4fea-926c-993861c8110a"

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "e9832229-ecaf-435f-98ec-6d3470a13cd4",  # 結婚相談所
    "61acc4f3-6c16-4653-995b-dd6d9136c1d3",  # IBJ
    "a8fd177f-b3ba-4a57-9f81-c26ba1ec0488",  # 婚活相談
    "8e779610-2acc-448e-b6b0-ad65dbb418d1",  # 無料相談
    "aa4700b5-badc-4875-91eb-d0026633922e",  # 婚活カウンセリング
]

SEO_DESCRIPTION = "IBJ加盟・少人数制・心理カウンセラー仲人・料金・無料相談……あすなる愛媛についてよく聞かれる質問に、仲人の中嶋美知がまとめてお答えします。"

BASE_STYLE = (
    "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
    "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
    "real-world setting, professional lifestyle photography style, "
    "shallow depth of field, clean bright modern atmosphere, no text"
)

IMAGE_PROMPTS = [
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A modern bright consultation room with soft plants, a round table with two chairs, "
            "warm natural light from a window, minimalist and welcoming decor. "
            "Empty room, inviting atmosphere, no people."
        ),
        "filename": "2026-05-30_qa1_img1.png",
    },
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A Japanese woman in her late 20s using a laptop in a bright clean home office, "
            "smiling slightly as she reads something, looking satisfied and calm. "
            "Clean desk, soft window light, relaxed professional setting."
        ),
        "filename": "2026-05-30_qa1_img2.png",
    },
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A happy Japanese couple in their 30s sitting together at a bright café table, "
            "both smiling naturally and relaxed, soft light, blurred background. "
            "Warm and optimistic atmosphere, sense of a fresh start together."
        ),
        "filename": "2026-05-30_qa1_img3.png",
    },
]

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

def image_node(file_info):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": file_info["url"]}}, "caption": ""}}

def generate_and_upload(prompt_text, filename):
    print(f"  gpt-image-1 生成中: {filename}")
    resp = client.images.generate(
        model="gpt-image-1", prompt=prompt_text, size="1536x1024", quality="medium", n=1
    )
    image_bytes = base64.b64decode(resp.data[0].b64_json)
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "displayName": filename}, timeout=30,
    )
    if not r.ok:
        print(f"  URL取得失敗: {r.status_code}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    sep = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print(f"  アップロード失敗: {ru.status_code}")
        return None
    url = ru.json().get("file", {}).get("url", "")
    if not url:
        print("  URL取得失敗")
        return None
    print(f"  完了: {url[:70]}...")
    return {"url": url}

def build_nodes(imgs):
    img1, img2, img3 = imgs[0], imgs[1], imgs[2]
    n = []

    n.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    n.append(sp())
    n.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    n.append(sp())
    n.append(p("「無料相談に行く前に、もう少しここのことを知りたい」"))
    n.append(sp())
    n.append(p("そういう方のために、よく聞かれることをまとめました。気になる項目だけでも読んでみてください！"))
    n.append(sp())

    if img1:
        n.append(image_node(img1)); n.append(sp())

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
    n.append(sp())

    if img2:
        n.append(image_node(img2)); n.append(sp())

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
    n.append(sp())

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
    n.append(sp())

    if img3:
        n.append(image_node(img3)); n.append(sp())

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
    n.append(sp())

    n.append(p("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan"))

    return n

def main():
    print("=" * 50)
    print("「あすなる愛媛Q&A」画像追加スクリプト")
    print("=" * 50)

    imgs = []
    for i, info in enumerate(IMAGE_PROMPTS, 1):
        print(f"\n[画像{i}/3]")
        result = generate_and_upload(info["prompt"], info["filename"])
        imgs.append(result)

    if any(img is None for img in imgs):
        print("\n⚠️ 一部の画像生成に失敗しました。")

    print("\nrichContent + タグ + メタ説明をPATCH中...")
    nodes = build_nodes(imgs)
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}",
        headers=wix_headers(),
        json={
            "draftPost": {
                "richContent": {"nodes": nodes, "metadata": {"version": 1}},
                "tagIds": TAG_IDS,
                "seoData": {"description": SEO_DESCRIPTION},
            },
            "fieldMask": "richContent,tagIds"
        },
        timeout=30,
    )
    if r.ok:
        print("PATCH完了 ✅")
    else:
        print(f"PATCH失敗: {r.status_code} {r.text[:300]}")
        return

    # カバー画像 displayed:true（元のQA1用アイキャッチ）
    cover_url = "https://static.wixstatic.com/media/e6bbff_d6a9cf480ad640699ff6c3ac1ecc2293~mv2.png"
    m = re.search(r"/media/([^?#\s]+)", cover_url)
    cover_id = m.group(1) if m else ""
    rc = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}",
        headers=wix_headers(),
        json={"draftPost": {"media": {
            "custom": True, "displayed": True,
            "wixMedia": {"image": {"id": cover_id, "url": cover_url, "height": 1024, "width": 1536, "filename": "2026-04-29_qa1_eyecatch.png"}}
        }}, "fieldMask": "media"},
        timeout=30,
    )
    print("カバー画像更新" + (" ✅" if rc.ok else f" 失敗({rc.status_code})"))
    print(f"\n✅ 完了！下書きID: {DRAFT_ID}")

if __name__ == "__main__":
    main()
