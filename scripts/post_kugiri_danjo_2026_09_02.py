"""
【男女共通】いつまでも「まだ決めなくていい」と思っていませんか？
カテゴリ: 仮交際
2026-09-02
"""
import os, sys, uuid, base64, requests
from openai import OpenAI

sys.path.insert(0, os.path.dirname(__file__))
from eyecatch_composer import compose_eyecatch

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")

client = OpenAI(api_key=OPENAI_KEY)

CATEGORY_IDS = [
    "3f5f378d-a4f4-47e0-90a7-ab4daa27504e",  # 仮交際
]
TAG_IDS = [
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "ce76d0c1-1fa1-4898-954b-2903a34dbcd4",  # マッチングアプリ
    "1571190e-c478-41bd-89b7-aa88c9747b98",  # 決断できない
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
]
RELATED_POST_IDS = [
    "b0a017e2-8b97-448f-8522-b3b0c8bd0d5a",
    "35d610c7-50ee-45ad-8d0a-310b7893b9b6",
    "29af95af-c7da-4507-bdbe-f53aa9f54309",
]

TITLE = "【男女共通】いつまでも「まだ決めなくていい」と思っていませんか？――仮交際と真剣交際、区切りがある婚活の話"
EXCERPT = "関係が曖昧なまま何人とも続けられてしまうのが今の恋愛の形。でも婚活には「そろそろ決める」という区切りがあります。心理学の視点から、区切りがあることの意味をお伝えします。"
FOCUS_KEYWORD = "仮交際 真剣交際 違い"

REAL_PHOTO_URL = "https://static.wixstatic.com/media/a4e52d_cf3f0f8fec8d40e4ac0e0bb6dfc4771d~mv2.png"

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "drafts", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

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

def image_node(file_obj, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": file_obj["url"]}}, "caption": caption}}

def real_photo_node():
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {
                "image": {"src": {"url": REAL_PHOTO_URL}},
                "containerData": {"width": {"size": "SMALL"}, "alignment": "CENTER"},
            }}

def build_nodes():
    nodes = []
    nodes.append(p("こんにちは！松山市駅から徒歩3分。"))
    nodes.append(sp())
    nodes.append(p("あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    nodes.append(p("マッチングアプリで出会った相手と、なんとなく関係が続いている。楽しくないわけではないけれど、この先どうなるかは決めていない。そんな状態に心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("今日は、その「決めなくていい」という状態について、少し立ち止まって考えてみたいと思います。"))
    nodes.append(sp())

    nodes.extend(section_heading("「まだ決めなくていい」は、実は苦しい"))
    nodes.append(sp())
    nodes.append(p("社会学者ジグムント・バウマンは、現代の恋愛が「いつでも他に乗り換えられる」流動的な関係になっていると指摘しました。関係を決めきらないままでいることは、自由に見えて、実は常に選び続けなければならない緊張状態でもあります。"))
    nodes.append(sp())
    nodes.append(p("マッチングアプリでのやり取りが、良い感じで続いているのに、なぜか将来の話にはならない。何人かと同時に連絡を取り合っているうちに、誰との関係も深まらないまま時間だけが過ぎていく。そんな声を、私はカウンセリングの中で何度も聞いてきました。"))
    nodes.append(sp())
    # [IMG:floating]
    nodes.append(p("これは、決断力がないからではありません。「区切り」がない環境に置かれれば、誰でも決めることが難しくなる。それだけのことなんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("こんなこと、心当たりはありませんか"))
    nodes.append(sp())
    nodes.append(p("いい人だと思うけれど、この人に決めていいのか分からないまま連絡を続けている。"))
    nodes.append(sp())
    nodes.append(p("複数の人とやり取りをしているうちに、誰との会話も似たような内容になってしまう。"))
    nodes.append(sp())
    nodes.append(p("「そろそろ将来の話をしたい」と思っても、切り出すタイミングがつかめない。"))
    nodes.append(sp())
    nodes.append(p("――どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("結婚相談所には、「区切り」がある"))
    nodes.append(sp())
    nodes.append(p("結婚相談所での婚活には、「仮交際」と「真剣交際」という2つの段階があります。仮交際の間は、複数の方と同時にお会いして構いません。これはマッチングアプリと同じで、比べながら進めていい期間です。"))
    nodes.append(sp())
    nodes.append(p("違うのは、その先に「真剣交際に進む」という明確な区切りが用意されていることです。真剣交際に入ったら、そこからはお一人に絞って向き合います。「なんとなく続く」状態のまま何ヶ月も過ごすことが、制度としてそもそも起こりにくい設計になっているんです。"))
    nodes.append(sp())
    nodes.append(p("行動経済学の研究でも、人は自分で締め切りを設定するより、外側から区切りを与えられたほうが行動に移しやすいことが分かっています。ダイエットも貯金も、宣言したり誰かに管理してもらったりするほうが続きやすいのと同じ仕組みです。"))
    nodes.append(sp())
    # [IMG:decision]
    nodes.append(p("婚活における「そろそろ決める」というタイミングも、一人で判断し続けるより、仲人という第三者と一緒に見極めていくほうが、驚くほど楽になります。"))
    nodes.append(sp())

    nodes.extend(section_heading("素直に「決めたい」と言っていい"))
    nodes.append(sp())
    nodes.append(p("「まだ決めなくていい」という状態に居心地の良さを感じる方もいれば、本当は早く区切りをつけて、次に進みたいと感じている方もいます。どちらが正解ということはありません。"))
    nodes.append(sp())
    nodes.append(p('ただ、もし後者に近いなら、我慢して"待つ"を続ける必要はないんです。「そろそろ決めたい」という自分の気持ちに、素直に従っていい。私はそんな婚活のあり方を"素直婚"と呼んでいます。'))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今、進行中の関係について「自分はいつまでにどうしたいか」を、頭の中だけでなく紙に一行だけ書き出してみてください。それだけで、次にやることが少し見えてきます。"))
    nodes.append(sp())

    nodes.append(real_photo_node())
    nodes.append(sp())
    nodes.append(link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan", "https://www.asunaru.jp/soudan"))
    return nodes

def find_index_after_text_contains(nodes, substr):
    for i, n in enumerate(nodes):
        if n.get("type") == "PARAGRAPH":
            for t in n.get("nodes", []):
                text = t.get("textData", {}).get("text", "")
                if substr in text:
                    return i
    return -1

def generate_image(prompt, filename):
    print(f"[gpt-image-1] generating: {filename}")
    resp = client.images.generate(model="gpt-image-1", prompt=prompt, size="1536x1024", quality="high", n=1)
    img_data = resp.data[0]
    if not img_data.b64_json:
        raise RuntimeError("b64_json missing")
    img_bytes = base64.b64decode(img_data.b64_json)
    local_path = os.path.join(IMAGES_DIR, filename)
    with open(local_path, "wb") as f:
        f.write(img_bytes)
    print(f"  保存完了: {local_path}")
    return local_path

def upload_image_file(local_path, filename):
    with open(local_path, "rb") as f:
        image_bytes = f.read()
    r = requests.post(f"{WIX_BASE}/site-media/v1/files/generate-upload-url", headers=wix_headers(),
                       json={"mimeType": "image/png", "displayName": filename}, timeout=30)
    if not r.ok:
        print("  upload URL failed:", r.status_code, r.text[:200]); return None
    data = r.json()
    upload_url = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    sep = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print("  upload failed:", ru.status_code, ru.text[:200]); return None
    file_obj = ru.json().get("file", {})
    if not file_obj.get("url"):
        print("  URL missing:", ru.json()); return None
    print(f"  -> {file_obj['url'][:80]}...")
    return file_obj

def create_draft():
    body = {
        "draftPost": {
            "title": TITLE,
            "richContent": {"nodes": build_nodes(), "metadata": {"version": 1}},
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "relatedPostIds": RELATED_POST_IDS,
            "excerpt": EXCERPT,
            "memberId": MEMBER_ID,
        },
        "publish": False,
    }
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(), json=body, timeout=30)
    if not r.ok:
        print("下書き作成失敗:", r.status_code, r.text[:500])
        return None
    draft = r.json()["draftPost"]
    print("下書き作成完了 ID:", draft["id"])
    return draft["id"]

def set_seo(draft_id):
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
    print("SEOメタ更新:", "完了" if rp.ok else f"失敗 {rp.status_code} {rp.text[:300]}")

def add_images(draft_id):
    base_style = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
                  "clear skin, real-world setting, professional lifestyle photography style, shallow depth of field, "
                  "clean bright modern atmosphere, no text, no warm yellowish tint")

    eyecatch_prompt = (base_style + ", a Japanese man and woman in their 30s sitting at a cafe table, "
        "both looking thoughtfully out the window rather than at each other, ambiguous unresolved mood, soft daylight")
    floating_prompt = (base_style + ", a Japanese woman in her 30s standing alone on a small boat drifting on "
        "calm water, symbolic of being unmoored and undecided, soft overcast light, wide shot")
    decision_prompt = (base_style + ", a Japanese woman in her 30s writing in a small notebook at a desk, "
        "calm focused expression, warm desk lamp light, cozy evening atmosphere")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-09-02_kugiri_danjo_eyecatch.png")
    floating_path = generate_image(floating_prompt, "2026-09-02_kugiri_danjo_floating.png")
    decision_path = generate_image(decision_prompt, "2026-09-02_kugiri_danjo_decision.png")

    files = {
        "floating": upload_image_file(floating_path, "2026-09-02_kugiri_danjo_floating.png"),
        "decision": upload_image_file(decision_path, "2026-09-02_kugiri_danjo_decision.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("これは、決断力がないからではありません。「区切り」がない環境に置かれれば、誰でも決めることが難しくなる。それだけのことなんです。", "floating", "区切りのない海を、一人で漂い続けていませんか。"),
        ("行動経済学の研究でも、人は自分で締め切りを設定するより、外側から区切りを与えられたほうが行動に移しやすいことが分かっています。ダイエットも貯金も、宣言したり誰かに管理してもらったりするほうが続きやすいのと同じ仕組みです。", "decision", "小さく書き出すだけで、決断は動き出します。"),
    ]
    insertions = []
    for substr, key, caption in insert_after:
        idx = find_index_after_text_contains(nodes, substr)
        if idx == -1:
            print("  挿入位置が見つかりません:", substr[:20]); continue
        insertions.append((idx, key, caption))
    insertions.sort(key=lambda x: x[0], reverse=True)
    for idx, key, caption in insertions:
        img = image_node(files[key], caption)
        nodes[idx+1:idx+1] = [sp(), img, sp()]

    patch_body = {"draftPost": {"richContent": {"nodes": nodes, "metadata": {"version": 1}}}, "fieldMask": "richContent"}
    rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=patch_body, timeout=30)
    print("本文への画像差し込み:", "完了" if rp.ok else f"失敗 {rp.status_code} {rp.text[:300]}")

    composed_path = os.path.join(IMAGES_DIR, "2026-09-02_kugiri_danjo_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=eyecatch_path,
        main_html='いつまでも<br><span class="accent">「まだ決めなくていい」</span>と<br>思っていませんか？',
        subtitle_text="――仮交際と真剣交際、区切りがある婚活の話",
        out_path=composed_path,
        main_size=54,
    )
    eyecatch_file = upload_image_file(composed_path, "2026-09-02_kugiri_danjo_eyecatch_composed.png")
    if not eyecatch_file:
        print("アイキャッチのアップロードに失敗しました。"); return
    media_patch = {
        "draftPost": {"media": {"custom": True, "wixMedia": {"image": {
            "id": eyecatch_file.get("id", ""), "url": eyecatch_file["url"],
            "height": eyecatch_file.get("height", 1024), "width": eyecatch_file.get("width", 1536),
            "filename": eyecatch_file.get("displayName", "eyecatch.png"),
        }}, "displayed": True}},
        "fieldMask": "media",
    }
    rm = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=media_patch, timeout=30)
    print("カバー画像設定:", "完了" if rm.ok else f"失敗 {rm.status_code} {rm.text[:300]}")

if __name__ == "__main__":
    existing = os.environ.get("EXISTING_DRAFT_ID")
    if existing:
        draft_id = existing
        print("既存下書きを使用:", draft_id)
    else:
        draft_id = create_draft()
        if draft_id:
            set_seo(draft_id)
    if draft_id:
        add_images(draft_id)
        print("\nDRAFT_ID =", draft_id)
        print(f"編集URL: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog/post/{draft_id}")
