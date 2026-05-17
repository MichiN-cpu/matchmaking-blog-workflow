"""
同居記事の画像を若くスタイリッシュに作り直し v3
下書きID: db6f3405-8ac9-4f76-a575-c8579ea63941
2026-05-17
"""
import os, time, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
DRAFT_ID    = "db6f3405-8ac9-4f76-a575-c8579ea63941"

CATEGORY_IDS     = ["a65acc05-b781-4ec9-95d7-66c9daefc19f"]
TAG_IDS          = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",
    "10dc8abd-4250-4356-a7ad-9f4465502257",
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",
    "18eef72c-620b-46dd-969b-30553b86c45a",
    "3a8d9ef3-9a26-4099-8ac8-546957aa1043",
    "3c983f3c-50b7-4193-9d37-64a066c45d1c",
]
RELATED_POST_IDS = [
    "e8c323f3-ec33-49f5-83ce-fb994d2a014b",
    "9ef3a363-e67a-44e8-a56e-b1492596dfe6",
    "7c374371-ece7-4888-8bb1-abddd6e62cd7",
]
MEMBER_ID = "69e25236-d316-4da8-92e4-f500aca1fe37"

client = OpenAI(api_key=OPENAI_KEY)

# スタイル定義：若くキレのあるイラスト
BASE_STYLE = (
    "Crisp modern Japanese illustration style, clean sharp lines, "
    "vibrant yet sophisticated color palette. "
    "Characters look stylish and youthful in their late 40s to early 50s — "
    "think chic Tokyo professionals, NOT retired grandparents. "
    "Contemporary fashion: slim-fit clothes, modern haircut, well-groomed. "
    "Bright cheerful mood, no text in image."
)

IMAGE_CONFIGS = [
    {
        "filename": "2026-05-17_arakan_cover_v3.png",
        "prompt": (
            f"{BASE_STYLE} "
            "A stylish Japanese man around 50, slim-fit dark casual jacket and light shirt, "
            "modern short haircut, warm confident smile, standing in a bright urban park setting. "
            "Cherry blossoms in background, fresh spring sunlight. "
            "Energetic and attractive, like a hero from a Japanese trendy drama. "
            "He looks ready for a new romantic chapter, not like a retiree."
        ),
        "role": "cover"
    },
    {
        "filename": "2026-05-17_arakan_couple_v3.png",
        "prompt": (
            f"{BASE_STYLE} "
            "A stylish Japanese couple both around 48-52 years old, sitting across from each other "
            "at a modern bright cafe with large windows. "
            "Man in slim chic casual wear, woman in a soft elegant blouse, both look fashionable. "
            "They lean in with genuine interest, warm smiles, eyes meeting. "
            "Like a scene from a sophisticated Japanese romantic drama. "
            "Bright warm light, fresh flowers on the table."
        ),
        "role": "img1"
    },
    {
        "filename": "2026-05-17_arakan_home_v3.png",
        "prompt": (
            f"{BASE_STYLE} "
            "A happy stylish Japanese couple around 50, relaxing together on a modern sofa "
            "in a bright minimalist living room. "
            "Man in a smart casual knit top, woman in a chic loungewear, "
            "both look young, fashionable and content. "
            "They are laughing over a glass of wine or tea. "
            "Cozy modern interior with indoor plants, warm evening light. "
            "Just the two of them — intimate, romantic, peaceful."
        ),
        "role": "img2"
    },
    {
        "filename": "2026-05-17_arakan_ready_v3.png",
        "prompt": (
            f"{BASE_STYLE} "
            "A stylish confident Japanese man around 50, slim modern business casual outfit, "
            "sitting at a clean bright desk with a planner and laptop open. "
            "He looks sharp, proactive and attractive — not old or tired. "
            "Warm natural light from a window, a small plant beside him. "
            "Expression: calm, capable, and quietly proud. "
            "He clearly has a plan and is ready to be a great partner."
        ),
        "role": "img3"
    },
]

def wix_headers():
    return {
        "Authorization": WIX_API_KEY,
        "wix-site-id":   WIX_SITE_ID,
        "Content-Type":  "application/json",
    }

def nid():
    return str(uuid.uuid4())[:8]

def upload_image_binary(image_bytes, filename):
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "displayName": filename},
        timeout=30,
    )
    if not r.ok:
        print(f"  アップロードURL取得失敗: {r.status_code}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        return None
    sep = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print(f"  アップロード失敗: {ru.status_code}")
        return None
    file_obj = ru.json().get("file", {})
    url = file_obj.get("url", "")
    fid = file_obj.get("id", "")
    if not url:
        return None
    print(f"  → {url[:70]}...")
    return {"url": url, "id": fid}

def generate_image(cfg):
    print(f"\n[{cfg['role']}] {cfg['filename']}...")
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=cfg["prompt"],
        size="1536x1024",
        quality="high",
        n=1,
    )
    img_data = resp.data[0]
    print("  生成完了、アップロード中...")
    if img_data.b64_json:
        return upload_image_binary(base64.b64decode(img_data.b64_json), cfg["filename"])
    return None

# ---- richContent ----
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
            "decorations": [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]
        }}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}

def image_node(url):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": url}}, "caption": ""}}

def build_nodes(img1_url, img2_url, img3_url):
    n = []
    n.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    n.append(sp())
    n.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    n.append(sp())
    n.append(p("今日は、少し正直な話をさせてください。"))
    n.append(sp())
    n.append(p("アラカン——還暦近くのご年齢で婚活されている男性の中に、ご両親のどちらかと同居されている方がいらっしゃいます。"))
    n.append(p("プロフィールには「相談の上で」と書いてあるけれど、本音は「いずれ一緒に住んでほしい」と思っていることが多いんですよね。"))
    n.append(sp())
    n.append(p("その気持ち、もちろんわかります。大切な親御さんですから。"))
    n.append(sp())
    n.append(p("でも今日は、そこに正直に向き合っていただきたくて、書いています。"))
    n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("逆の立場で、一度考えてみてください"))
    n.append(sp())
    n.append(p("もしあなたが、女性側の親御さんと一緒に暮らさないといけないと言われたら——どうでしょう？"))
    n.append(sp())
    n.append(p("面識もほとんどない、生活スタイルも価値観も異なる、でも毎日顔を合わせてバランスをとりながら過ごす。"))
    n.append(p("そしてその方の介護も、いずれやってくる。"))
    n.append(sp())
    n.append(p("……想像するだけで、少し重くなりませんか。"))
    n.append(sp())
    n.append(p("女性たちも、まったく同じ気持ちです。"))
    n.append(sp())
    n.append(image_node(img1_url)); n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("「相談の上で」は、女性には「同居あり」に見えています"))
    n.append(sp())
    n.append(p("これが現実なんですよね。"))
    n.append(sp())
    n.append(p("「相談の上で」と書いてあっても、女性は読み解いています。「いずれ同居を望んでいる方なんだな」と。"))
    n.append(sp())
    n.append(p("そしてそこで、静かに心が動きます。「一緒に暮らすことになったら、どんな毎日になるだろう」と。"))
    n.append(sp())
    n.append(p("女性はおしゃべりです（笑）。"))
    n.append(p("友人や先輩からの話がリアルに蓄積されています。"))
    n.append(p("姑と同居で苦労した話、夫が間に挟まれて頼りなく見えた話、1人になれる時間がなくて限界になった話——そういう話が、女性たちの間では当たり前のように共有されています。"))
    n.append(sp())
    n.append(p("だから、想像力のハードルが低い。「そうなったとき、自分はどうなるか」がリアルに見えてしまうんです。"))
    n.append(sp())
    n.append(p("「いい人だなと思っても、同居があるなら……。傷つけ合うリスクを取るより、これまで通り1人のほうがマシかもしれない。」と。"))
    n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("若い頃の同居とは、まったく違います"))
    n.append(sp())
    n.append(p("若くして結婚して、子どもが生まれて、一緒に孫を育てて——そういう積み重ねの中での同居は、愛着も理解もあります。我慢もできるし、遠慮がなくなってくることもある。"))
    n.append(sp())
    n.append(p("でも、アラカンでの婚活は違います。"))
    n.append(sp())
    n.append(p("お互いにすでに長年の生活スタイルがある。夫婦でそれをすり合わせるだけでも、かなりのエネルギーが必要です。"))
    n.append(p("そこにさらにもう一人——まったくの初対面に近い方が加わって、その方の意図や気持ちを汲みながら、バランスをとりながら暮らしていく。"))
    n.append(sp())
    n.append(p("心理学でいう「自律性の欲求」という概念があります。"))
    n.append(p("人間は自分のペースで、自分の空間で過ごせる時間がないと、じわじわとストレスが積み上がっていきます（デシとライアン、1985年）。"))
    n.append(p("同居という環境は、その自律性を大きく制限する可能性があるんです。"))
    n.append(sp())
    n.append(p("介護が加わると、もっとです。"))
    n.append(sp())
    n.append(image_node(img2_url)); n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("だからこそ、早めの行動が必要です"))
    n.append(sp())
    n.append(p("「同居をお願いしたら、成婚は難しくなる」と覚悟した上でお願いするなら、それはお気持ちの問題ですから、私には何も言えません。"))
    n.append(sp())
    n.append(p("でも、少しでも成婚の可能性を広げたいと思っていらっしゃるなら、今すぐできることがあります。"))
    n.append(sp())
    n.append(p("まず、親御さんがまだお元気なうちに、動いてください。「まだ大丈夫」と思っている間が、一番準備しやすいときです。"))
    n.append(sp())
    n.append(p("具体的には——ケアマネージャーさんに一度相談する、在宅介護サービスの情報を調べる、将来的に施設を利用する選択肢を確認しておく。そういったことを、今からやっておくということです。"))
    n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("「準備しています」という一言が、女性の心を動かします"))
    n.append(sp())
    n.append(p("お見合いの場やデートで、万が一「ご両親のことはどのようにお考えですか」と聞かれたとき。"))
    n.append(sp())
    n.append(p("「まだ考えていないです」という男性と、「ケアマネさんとも相談していて、こういう方向で考えています」という男性——どちらが頼もしく見えるでしょうか。"))
    n.append(sp())
    n.append(p("家族社会学の観点から言えば、結婚は「2人のシステム」に外部環境をどう取り込むかの設計でもあります。その設計を、すでに始めているかどうかが、女性の安心感に直結します。"))
    n.append(sp())
    n.append(p("「奥さんに苦労させたくない」「幸せにしたい」「笑顔いっぱいにしてあげたい」という思いがあるなら、その思いを行動で見せてほしいんです。"))
    n.append(sp())
    n.append(p("婚活の場に出てくる「前に」、もしくは「今すぐに」。"))
    n.append(sp())
    n.append(image_node(img3_url)); n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("厳しいことを言ったのは、応援しているからです"))
    n.append(sp())
    n.append(p("奇跡を待っていても、ナイチンゲールのような天使が現れることはなかなかありません（笑）。"))
    n.append(sp())
    n.append(p("現実に向き合って、準備して、行動する——その姿勢が、あなたをもっとも魅力的な男性に見せてくれます。"))
    n.append(sp())
    n.append(p("何か聞かれたときに「こういう対策を考えています」「もう準備しています」と自信を持って答えられる男性は、それだけで女性の信頼をつかみます。"))
    n.append(sp())
    n.append(p("心から応援しているから、正直にお伝えしました。"))
    n.append(sp())
    n.append(link_node("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"))
    return n

def main():
    imgs = {}
    for cfg in IMAGE_CONFIGS:
        imgs[cfg["role"]] = generate_image(cfg)

    cover = imgs.get("cover")
    img1  = imgs.get("img1")
    img2  = imgs.get("img2")
    img3  = imgs.get("img3")

    nodes = build_nodes(
        img1["url"] if img1 else "",
        img2["url"] if img2 else "",
        img3["url"] if img3 else "",
    )
    rich_content = {"nodes": nodes, "metadata": {"version": 1}}

    cover_id  = cover["id"]  if cover else ""
    cover_url = cover["url"] if cover else ""
    meta_desc = "親と同居のアラカン婚活男性へ。「相談の上で同居を」は女性にはほぼ同居確定に見えます。成婚確率が大きく下がる理由と、今すぐできる準備を心理カウンセラー仲人が正直にお伝えします。"

    print("\nWixに下書きPATCH中...")
    rp = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}",
        headers=wix_headers(),
        json={
            "draftPost": {
                "id": DRAFT_ID,
                "richContent": rich_content,
                "categoryIds": CATEGORY_IDS,
                "tagIds": TAG_IDS,
                "memberId": MEMBER_ID,
                "relatedPostIds": RELATED_POST_IDS,
                "media": {
                    "wixMedia": {"image": {"id": cover_id, "url": cover_url}},
                    "displayed": True,
                    "custom": True
                },
                "seoData": {
                    "tags": [{"type": "meta", "props": {"name": "description", "content": meta_desc}, "custom": False, "disabled": False}]
                }
            }
        },
        timeout=60,
    )
    if rp.ok:
        print("✅ PATCH完了！")
    else:
        print(f"PATCH失敗: {rp.status_code} {rp.text[:300]}")

    print(f"\n✅ 完了！下書きID: {DRAFT_ID}")
    print("⚠️  Wixで画像が正しく表示されているか確認してください！")

if __name__ == "__main__":
    main()
