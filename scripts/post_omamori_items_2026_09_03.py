"""
【男女共通】婚活中の自分を、そっと励ます3つの道具。
カテゴリ: お知らせ
2026-09-03
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
    "fc247847-d52b-438c-ab23-95bae771dc0a",  # お知らせ
]
TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
]
RELATED_POST_IDS = [
    "935c10a3-40fd-4a54-92af-68cc5596df81",
    "cb957906-b9f4-47f2-9f2f-6352923232ab",
    "eb8a7508-a182-4140-8591-5ad52870214e",
]

TITLE = "【男女共通】婚活中の自分を、そっと励ます3つの道具。――NLPカウンセラーが作った、日々のためのお守り"
EXCERPT = "婚活は、頑張り続けるほど心が疲れやすくなります。公認心理師・NLPカウンセラーの中嶋美知が作った、日々の心を整える3つのアイテムをご紹介します。"
FOCUS_KEYWORD = "婚活 メンタル NLP グッズ"

REAL_PHOTO_URL = "https://static.wixstatic.com/media/a4e52d_cf3f0f8fec8d40e4ac0e0bb6dfc4771d~mv2.png"

LINK_VIDEO = "https://line-harness.design-3333.workers.dev/t/EdUBGbA"
LINK_CALENDAR = "https://line-harness.design-3333.workers.dev/t/lr7c7en"
LINK_CARDS = "https://line-harness.design-3333.workers.dev/t/iz9NLm8"

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

def p_link(text, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]}}
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

    nodes.append(p("今日は少し趣向を変えて、婚活と直接は関係のないお知らせをさせてください。実は私、心理カウンセラー・NLPコミュニケーション心理学の講師として、婚活とは別に「office de・Sign」という活動もしていて、そこで作った3つのアイテムをご紹介したいんです。"))
    nodes.append(sp())
    nodes.append(p("婚活は、真剣に向き合えば向き合うほど、心が疲れやすくなります。今日ご紹介するのは、そんな毎日にそっと寄り添うための道具たちです。"))
    nodes.append(sp())

    nodes.extend(section_heading("① 動画で学ぶコミュニケーション心理学"))
    nodes.append(sp())
    nodes.append(p("NLPコミュニケーション心理学のプラクティショナーコース全10日間を、動画で学べる講座です。グループワークがないので、自分のペースで、誰にも気を遣わずに視聴できます。"))
    nodes.append(sp())
    nodes.append(p("お見合いや会話に自信が持てない、相手の気持ちを読み取るのが苦手、そんな悩みの多くは、コミュニケーションの「型」を知らないだけということが少なくありません。"))
    nodes.append(sp())
    # [IMG:study]
    nodes.append(p_link("▶ 動画で学ぶコミュニケーション心理学を見る", LINK_VIDEO))
    nodes.append(sp())

    nodes.extend(section_heading("② 日めくりカレンダー「今日もニャイス！」"))
    nodes.append(sp())
    nodes.append(p("猫のイラストと一緒に、31日分の小さなメッセージが届く万年カレンダーです。「肩の力が抜ける」一言を、毎朝めくって確認するだけ。婚活中、頑張りすぎてしまう自分に気づいたときに、そっと力を抜く合図として使ってみてください。"))
    nodes.append(sp())
    # [IMG:calendar]
    nodes.append(p_link("▶ 日めくりカレンダーを見る", LINK_CALENDAR))
    nodes.append(sp())

    nodes.extend(section_heading("③ にゃんコーチングカード"))
    nodes.append(sp())
    nodes.append(p("16枚のカードに、32のメッセージが込められたセルフコーチングカードです。「これでいいのかな」とぐるぐる考えてしまう夜、1枚引いてみることで、自分の中にある答えのヒントに気づけることがあります。"))
    nodes.append(sp())
    nodes.append(p("お見合いの前、返事に迷ったとき、なんとなく心がざわつくとき。占いではなく、自分の潜在意識に問いかけるためのツールとして作りました。"))
    nodes.append(sp())
    nodes.append(p_link("▶ にゃんコーチングカードを見る", LINK_CARDS))
    nodes.append(sp())

    nodes.extend(section_heading("頑張るあなたに、休む理由を"))
    nodes.append(sp())
    nodes.append(p("婚活相談所の仲人として、そして心理カウンセラーとして、私がずっと伝えたいと思ってきたのは「頑張り方」だけでなく「休み方」です。走り続けるための道具ではなく、立ち止まっていい、と思わせてくれる道具を、これからも作っていけたらと思っています。"))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、3つのうちどれか一つだけ、リンクを開いて眺めてみてください。気になったら、それがきっと今のあなたに必要なサインです。"))
    nodes.append(sp())

    nodes.append(real_photo_node())
    nodes.append(sp())
    nodes.append(link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan", "https://www.asunaru.jp/soudan"))
    return nodes

def find_index_after_text_contains(nodes, substr):
    for i, n in enumerate(nodes):
        if n.get("type") == "PARAGRAPH":
            text = "".join(t.get("textData", {}).get("text", "") for t in n.get("nodes", []))
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
    base_style = ("Photorealistic, cinematic quality, natural soft lighting, clear skin, "
                  "real-world setting, professional lifestyle photography style, shallow depth of field, "
                  "clean bright modern atmosphere, no text, no warm yellowish tint")

    eyecatch_prompt = (base_style + ", flatlay of a cozy desk scene with a notebook, a warm cup of tea, "
        "a small stack of cards, and a laptop showing a video course, soft morning window light, calming aesthetic")
    study_prompt = (base_style + ", a Japanese woman in her 30s relaxed on a sofa at home watching a laptop "
        "screen with headphones on, taking notes in a notebook, cozy evening light")
    calendar_prompt = (base_style + ", close up of a small desk calendar and a warm cup of coffee on a wooden "
        "desk near a sunny window, peaceful morning routine mood")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-09-03_omamori_items_eyecatch.png")
    study_path = generate_image(study_prompt, "2026-09-03_omamori_items_study.png")
    calendar_path = generate_image(calendar_prompt, "2026-09-03_omamori_items_calendar.png")

    files = {
        "study": upload_image_file(study_path, "2026-09-03_omamori_items_study.png"),
        "calendar": upload_image_file(calendar_path, "2026-09-03_omamori_items_calendar.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("お見合いや会話に自信が持てない、相手の気持ちを読み取るのが苦手、そんな悩みの多くは、コミュニケーションの「型」を知らないだけということが少なくありません。", "study", "自分のペースで、何度でも学び直せます。"),
        ("猫のイラストと一緒に、31日分の小さなメッセージが届く万年カレンダーです。「肩の力が抜ける」一言を、毎朝めくって確認するだけ。婚活中、頑張りすぎてしまう自分に気づいたときに、そっと力を抜く合図として使ってみてください。", "calendar", "毎朝、1ページだけめくる小さな習慣。"),
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

    composed_path = os.path.join(IMAGES_DIR, "2026-09-03_omamori_items_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=eyecatch_path,
        main_html='婚活中の自分を、<br>そっと<span class="accent">励ます</span>3つの道具。',
        subtitle_text="――NLPカウンセラーが作った、日々のためのお守り",
        out_path=composed_path,
        main_size=48,
    )
    eyecatch_file = upload_image_file(composed_path, "2026-09-03_omamori_items_eyecatch_composed.png")
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
