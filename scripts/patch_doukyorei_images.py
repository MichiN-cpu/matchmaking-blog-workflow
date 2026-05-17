"""
同居記事の画像を明るく作り直し + richContent更新スクリプト
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

CATEGORY_IDS    = ["a65acc05-b781-4ec9-95d7-66c9daefc19f"]
TAG_IDS         = [
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

BASE_STYLE = (
    "Flat illustration style, no text, bright cheerful warm colors, "
    "optimistic and hopeful mood, minimalist, Japanese blog aesthetic, "
    "soft pastel tones with warm orange and coral accents. "
    "NOT dark, NOT gloomy, NOT stressful."
)

IMAGE_CONFIGS = [
    {
        "filename": "2026-05-17_arakan_cover_v2.png",
        "prompt": (
            f"{BASE_STYLE} "
            "A cheerful Japanese man in his late 50s, neat casual outfit, "
            "standing outdoors with a warm confident smile and arms open wide, "
            "cherry blossom petals floating around him. "
            "Bright blue sky, sunshine, fresh spring atmosphere. "
            "Energetic, ready for a new chapter of life."
        ),
        "role": "cover"
    },
    {
        "filename": "2026-05-17_arakan_couple_talk_v2.png",
        "prompt": (
            f"{BASE_STYLE} "
            "A Japanese couple in their 50s sitting together at a bright sunny café, "
            "both smiling warmly, leaning in with interest as they talk. "
            "Flowers on the table, warm light coming through the window. "
            "Open, honest, and warm conversation. "
            "Cheerful and hopeful atmosphere."
        ),
        "role": "img1"
    },
    {
        "filename": "2026-05-17_arakan_happy_home_v2.png",
        "prompt": (
            f"{BASE_STYLE} "
            "A happy Japanese couple in their 50s sitting together on a sofa at home, "
            "laughing over a cup of tea, a cat curled up beside them. "
            "Cozy bright living room, houseplants, soft afternoon light. "
            "Peaceful, warm, and joyful domestic scene. "
            "Just the two of them, comfortable and content."
        ),
        "role": "img2"
    },
    {
        "filename": "2026-05-17_arakan_planning_v2.png",
        "prompt": (
            f"{BASE_STYLE} "
            "A confident Japanese man in his late 50s sitting at a bright desk, "
            "smiling as he reviews a neatly organized planner and checklist. "
            "A small plant on the desk, sunshine coming through the window. "
            "Prepared, proactive, and optimistic atmosphere. "
            "Symbolizing a man who is thoughtfully getting ready for the future."
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
        print(f"アップロードURL取得失敗: {r.status_code} {r.text[:200]}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        return None
    sep = "&" if "?" in upload_url else "?"
    upload_url_fn = f"{upload_url}{sep}filename={filename}"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(upload_url_fn, data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print(f"バイナリアップロード失敗: {ru.status_code} {ru.text[:200]}")
        return None
    result  = ru.json()
    file_obj = result.get("file", {})
    file_url = file_obj.get("url", "")
    file_id  = file_obj.get("id", "")
    if not file_url:
        return None
    print(f"  → アップロード完了: {file_url[:70]}...")
    return {"url": file_url, "id": file_id}

def generate_image(cfg):
    print(f"\n[{cfg['role']}] 画像生成中: {cfg['filename']}...")
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=cfg["prompt"],
        size="1536x1024",
        quality="high",
        n=1,
    )
    img_data = resp.data[0]
    print("  生成完了。アップロード中...")
    if img_data.b64_json:
        return upload_image_binary(base64.b64decode(img_data.b64_json), cfg["filename"])
    return None

# ---- richContent helpers ----
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

def image_node(url, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": url}}, "caption": caption}}

def build_nodes(img1_url, img2_url, img3_url):
    nodes = []
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())
    nodes.append(p("今日は、少し正直な話をさせてください。"))
    nodes.append(sp())
    nodes.append(p("アラカン——還暦近くのご年齢で婚活されている男性の中に、ご両親のどちらかと同居されている方がいらっしゃいます。"))
    nodes.append(p("プロフィールには「相談の上で」と書いてあるけれど、本音は「いずれ一緒に住んでほしい」と思っていることが多いんですよね。"))
    nodes.append(sp())
    nodes.append(p("その気持ち、もちろんわかります。大切な親御さんですから。"))
    nodes.append(sp())
    nodes.append(p("でも今日は、そこに正直に向き合っていただきたくて、書いています。"))
    nodes.append(sp())

    nodes.append(divider_node()); nodes.append(sp())
    nodes.append(h("逆の立場で、一度考えてみてください"))
    nodes.append(sp())
    nodes.append(p("もしあなたが、女性側の親御さんと一緒に暮らさないといけないと言われたら——どうでしょう？"))
    nodes.append(sp())
    nodes.append(p("面識もほとんどない、生活スタイルも価値観も異なる、でも毎日顔を合わせてバランスをとりながら過ごす。"))
    nodes.append(p("そしてその方の介護も、いずれやってくる。"))
    nodes.append(sp())
    nodes.append(p("……想像するだけで、少し重くなりませんか。"))
    nodes.append(sp())
    nodes.append(p("女性たちも、まったく同じ気持ちです。"))
    nodes.append(sp())
    nodes.append(image_node(img1_url, ""))
    nodes.append(sp())

    nodes.append(divider_node()); nodes.append(sp())
    nodes.append(h("「相談の上で」は、女性には「同居あり」に見えています"))
    nodes.append(sp())
    nodes.append(p("これが現実なんですよね。"))
    nodes.append(sp())
    nodes.append(p("「相談の上で」と書いてあっても、女性は読み解いています。"))
    nodes.append(p("「いずれ同居を望んでいる方なんだな」と。"))
    nodes.append(sp())
    nodes.append(p("そしてそこで、静かに心が動きます。"))
    nodes.append(p("「一緒に暮らすことになったら、どんな毎日になるだろう」と。"))
    nodes.append(sp())
    nodes.append(p("女性はおしゃべりです（笑）。"))
    nodes.append(p("友人や先輩からの話がリアルに蓄積されています。"))
    nodes.append(p("姑と同居で苦労した話、夫が間に挟まれて頼りなく見えた話、1人になれる時間がなくて限界になった話——そういう話が、女性たちの間では当たり前のように共有されています。"))
    nodes.append(sp())
    nodes.append(p("だから、想像力のハードルが低い。"))
    nodes.append(p("「そうなったとき、自分はどうなるか」がリアルに見えてしまうんです。"))
    nodes.append(sp())
    nodes.append(p("そしてこう思います。"))
    nodes.append(p("「いい人だなと思っても、同居があるなら……。傷つけ合うリスクを取るより、これまで通り1人のほうがマシかもしれない。」と。"))
    nodes.append(sp())

    nodes.append(divider_node()); nodes.append(sp())
    nodes.append(h("若い頃の同居とは、まったく違います"))
    nodes.append(sp())
    nodes.append(p("若くして結婚して、子どもが生まれて、一緒に孫を育てて——そういう積み重ねの中での同居は、愛着も理解もあります。"))
    nodes.append(p("我慢もできるし、遠慮がなくなってくることもある。"))
    nodes.append(sp())
    nodes.append(p("でも、アラカンでの婚活は違います。"))
    nodes.append(sp())
    nodes.append(p("お互いにすでに長年の生活スタイルがある。"))
    nodes.append(p("夫婦でそれをすり合わせるだけでも、かなりのエネルギーが必要です。"))
    nodes.append(p("そこにさらにもう一人——まったくの初対面に近い方が加わって、その方の意図や気持ちを汲みながら、バランスをとりながら暮らしていく。"))
    nodes.append(sp())
    nodes.append(p("心理学でいう「自律性の欲求」という概念があります。"))
    nodes.append(p("人間は自分のペースで、自分の空間で過ごせる時間がないと、じわじわとストレスが積み上がっていきます（デシとライアン、1985年）。"))
    nodes.append(p("同居という環境は、その自律性を大きく制限する可能性があるんです。"))
    nodes.append(sp())
    nodes.append(p("介護が加わると、もっとです。"))
    nodes.append(sp())
    nodes.append(image_node(img2_url, ""))
    nodes.append(sp())

    nodes.append(divider_node()); nodes.append(sp())
    nodes.append(h("だからこそ、早めの行動が必要です"))
    nodes.append(sp())
    nodes.append(p("「同居をお願いしたら、成婚は難しくなる」と覚悟した上でお願いするなら、それはお気持ちの問題ですから、私には何も言えません。"))
    nodes.append(sp())
    nodes.append(p("でも、少しでも成婚の可能性を広げたいと思っていらっしゃるなら、今すぐできることがあります。"))
    nodes.append(sp())
    nodes.append(p("まず、親御さんがまだお元気なうちに、動いてください。"))
    nodes.append(sp())
    nodes.append(p("「まだ大丈夫」と思っている間が、一番準備しやすいときです。"))
    nodes.append(sp())
    nodes.append(p("具体的には——ケアマネージャーさんに一度相談する、在宅介護サービスの情報を調べる、将来的に施設を利用する選択肢を確認しておく。"))
    nodes.append(p("そういったことを、今からやっておくということです。"))
    nodes.append(sp())

    nodes.append(divider_node()); nodes.append(sp())
    nodes.append(h("「準備しています」という一言が、女性の心を動かします"))
    nodes.append(sp())
    nodes.append(p("お見合いの場やデートで、万が一「ご両親のことはどのようにお考えですか」と聞かれたとき。"))
    nodes.append(sp())
    nodes.append(p("「まだ考えていないです」という男性と、「ケアマネさんとも相談していて、こういう方向で考えています」という男性——どちらが頼もしく見えるでしょうか。"))
    nodes.append(sp())
    nodes.append(p("家族社会学の観点から言えば、結婚は「2人のシステム」に外部環境をどう取り込むかの設計でもあります。"))
    nodes.append(p("その設計を、すでに始めているかどうかが、女性の安心感に直結します。"))
    nodes.append(sp())
    nodes.append(p("「奥さんに苦労させたくない」「幸せにしたい」「笑顔いっぱいにしてあげたい」という思いがあるなら、その思いを行動で見せてほしいんです。"))
    nodes.append(sp())
    nodes.append(p("婚活の場に出てくる「前に」、もしくは「今すぐに」。"))
    nodes.append(sp())
    nodes.append(image_node(img3_url, ""))
    nodes.append(sp())

    nodes.append(divider_node()); nodes.append(sp())
    nodes.append(h("厳しいことを言ったのは、応援しているからです"))
    nodes.append(sp())
    nodes.append(p("奇跡を待っていても、ナイチンゲールのような天使が現れることはなかなかありません（笑）。"))
    nodes.append(sp())
    nodes.append(p("現実に向き合って、準備して、行動する——その姿勢が、あなたをもっとも魅力的な男性に見せてくれます。"))
    nodes.append(sp())
    nodes.append(p("何か聞かれたときに「こういう対策を考えています」「もう準備しています」と自信を持って答えられる男性は、それだけで女性の信頼をつかみます。"))
    nodes.append(sp())
    nodes.append(p("心から応援しているから、正直にお伝えしました。"))
    nodes.append(sp())

    nodes.append(link_node("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"))
    return nodes

def main():
    # 4枚生成・アップロード
    imgs = {}
    for cfg in IMAGE_CONFIGS:
        result = generate_image(cfg)
        imgs[cfg["role"]] = result

    cover = imgs.get("cover")
    img1  = imgs.get("img1")
    img2  = imgs.get("img2")
    img3  = imgs.get("img3")

    # richContent再構築
    img1_url = img1["url"] if img1 else ""
    img2_url = img2["url"] if img2 else ""
    img3_url = img3["url"] if img3 else ""
    nodes = build_nodes(img1_url, img2_url, img3_url)
    rich_content = {"nodes": nodes, "metadata": {"version": 1}}

    # 下書き全体をPATCH（richContent + カバー + メタ）
    cover_id  = cover["id"] if cover and cover.get("id") else ""
    cover_url = cover["url"] if cover else ""
    meta_desc = "親と同居のアラカン婚活男性へ。「相談の上で同居を」は女性にはほぼ同居確定に見えます。成婚確率が大きく下がる理由と、今すぐできる準備を心理カウンセラー仲人が正直にお伝えします。"

    print("\nWixに下書きPATCH中...")
    patch_body = {
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
    }
    rp = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}",
        headers=wix_headers(),
        json=patch_body,
        timeout=60,
    )
    if rp.ok:
        print("✅ PATCH完了！")
    else:
        print(f"PATCH失敗: {rp.status_code} {rp.text[:300]}")

    print(f"\n✅ 完了！下書きID: {DRAFT_ID}")
    print("⚠️  Wixブログ管理画面で画像が正しく表示されているか必ず確認してください！")

if __name__ == "__main__":
    main()
