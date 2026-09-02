"""
【女性向け】その将来不安、一人で抱えなくていいのかもしれません。
カテゴリ: 無料相談の前に読む
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
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む
]
TAG_IDS = [
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
]
RELATED_POST_IDS = [
    "935c10a3-40fd-4a54-92af-68cc5596df81",
    "5810c39a-fdf2-495b-8150-55ec665eab2e",
    "eb8a7508-a182-4140-8591-5ad52870214e",
]

TITLE = "【女性向け】その将来不安、一人で抱えなくていいのかもしれません。――結婚で得られる「頼れる人がいる」という安心"
EXCERPT = "老後のこと、お金のこと、何かあったときのこと。一人で考えると際限なく膨らむ将来不安について、公的データと心理学の視点からお伝えします。"
FOCUS_KEYWORD = "女性 将来不安 結婚 安心"

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

    nodes.append(p("夜、ふとしたときに「この先、ずっと一人だったらどうしよう」と考えてしまう。老後のお金は足りるだろうか、体調を崩したとき誰に頼ればいいんだろう。そんな不安が頭をよぎることはありませんか。"))
    nodes.append(sp())
    nodes.append(p("今日は、その将来不安について、少し立ち止まって考えてみたいと思います。"))
    nodes.append(sp())

    nodes.extend(section_heading("その不安は、あなただけのものじゃありません"))
    nodes.append(sp())
    nodes.append(p("国立社会保障・人口問題研究所の出生動向基本調査では、未婚女性が結婚に感じる利点として「経済的余裕が持てる」と答えた人が20.4%にのぼりました。これは同じ質問への男性の回答（5.9%）の3倍以上で、女性のほうが経済的な安心を結婚に強く求めている傾向がはっきり表れています。"))
    nodes.append(sp())
    nodes.append(p("さらに「精神的な安らぎの場が得られる」と答えた女性も28.1%と、決して少なくありません。多くの女性が、心のどこかで同じような不安を抱え、同じように安心できる居場所を求めているということなんです。"))
    nodes.append(sp())
    # [IMG:night]
    nodes.append(p("これは弱さでも、考えすぎでもありません。一人で将来のあらゆる可能性に備えようとすること自体が、とても大きな負荷のかかる作業なんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("こんなこと、心当たりはありませんか"))
    nodes.append(sp())
    nodes.append(p("体調を崩したとき、真っ先に頭に浮かぶ「誰かに頼れる」相手がいない。"))
    nodes.append(sp())
    nodes.append(p("老後の資金や住まいのことを考え始めると、際限なく不安が膨らんでしまう。"))
    nodes.append(sp())
    nodes.append(p("大きな決断をするとき、いつも自分一人で全部背負っている感覚がある。"))
    nodes.append(sp())
    nodes.append(p("――どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("「頼れる人がいる」ことの、確かな効果"))
    nodes.append(sp())
    nodes.append(p("アメリカ・ブリガムヤング大学のホルト＝ランスタッド教授が148件の研究・30万人以上のデータを分析した結果では、社会的なつながりの薄さによる死亡リスクの上昇は、社会的孤立で29%、孤独感で26%、一人暮らしで32%にのぼると報告されています。この影響の大きさは、肥満や運動不足を上回るとされているんです。"))
    nodes.append(sp())
    nodes.append(p("一方で、内閣府の調査では、一人暮らしの高齢者のうち「頼れる人がいない」と答えた女性は9.3%にのぼります。これは裏を返せば、9割以上の方が誰かに頼れる関係を持っているということでもありますが、その「頼れる人」を自分の意思で作っていけるのが、婚活という選択肢の価値だと私は思っています。"))
    nodes.append(sp())
    # [IMG:together]
    nodes.append(p("将来の不安を一人で抱え続けるのではなく、一緒に考えてくれる人がいる。それだけで、同じ不安でも重さがまったく違って感じられるようになります。"))
    nodes.append(sp())

    nodes.extend(section_heading("素直に「支えてほしい」と思っていい"))
    nodes.append(sp())
    nodes.append(p("「一人でも生きていけるようにならなきゃ」と、自分に言い聞かせてきた方も多いと思います。それ自体はとても大切な力です。でも、支えてほしいと思う気持ちを持つことは、その力と矛盾しません。"))
    nodes.append(sp())
    nodes.append(p('強くあろうとする自分と、素直に頼りたい自分。そのどちらも我慢せず、両方を大事にしながら進んでいく婚活のかたちを、私は"素直婚"と呼んでいます。'))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、将来の不安が頭に浮かんだら、「これを一緒に考えてくれる人がいたら」と、一度だけ想像してみてください。"))
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
                  "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
                  "real-world setting, professional lifestyle photography style, shallow depth of field, "
                  "clean bright modern atmosphere, no text, no warm yellowish tint")

    eyecatch_prompt = (base_style + ", in her mid 30s, sitting alone on her bed at night, hugging her knees "
        "slightly, looking out a dark window with a pensive worried expression, soft lamp light")
    night_prompt = (base_style + ", in her mid 30s, lying awake in bed at night looking at the ceiling, "
        "moonlight through curtains, quiet contemplative mood, soft blue night tones")
    together_prompt = (base_style + ", a Japanese man and woman in their 30s sitting together on a sofa "
        "looking at documents and a laptop together, calm supportive teamwork mood, warm home lighting")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-09-02_anshin_josei_eyecatch.png")
    night_path = generate_image(night_prompt, "2026-09-02_anshin_josei_night.png")
    together_path = generate_image(together_prompt, "2026-09-02_anshin_josei_together.png")

    files = {
        "night": upload_image_file(night_path, "2026-09-02_anshin_josei_night.png"),
        "together": upload_image_file(together_path, "2026-09-02_anshin_josei_together.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("これは弱さでも、考えすぎでもありません。一人で将来のあらゆる可能性に備えようとすること自体が、とても大きな負荷のかかる作業なんです。", "night", "眠れない夜に浮かぶ不安は、あなただけのものではありません。"),
        ("一方で、内閣府の調査では、一人暮らしの高齢者のうち「頼れる人がいない」と答えた女性は9.3%にのぼります。これは裏を返せば、9割以上の方が誰かに頼れる関係を持っているということでもありますが、その「頼れる人」を自分の意思で作っていけるのが、婚活という選択肢の価値だと私は思っています。", "together", "一緒に考えてくれる人がいる、という安心。"),
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

    composed_path = os.path.join(IMAGES_DIR, "2026-09-02_anshin_josei_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=eyecatch_path,
        main_html='その将来不安、<br><span class="accent">一人で抱えなくて</span><br>いいのかもしれません。',
        subtitle_text="――結婚で得られる「頼れる人がいる」という安心",
        out_path=composed_path,
        main_size=50,
    )
    eyecatch_file = upload_image_file(composed_path, "2026-09-02_anshin_josei_eyecatch_composed.png")
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
