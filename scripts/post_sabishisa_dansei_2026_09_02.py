"""
【男性向け】夜、なんとなく手が伸びる一杯。
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
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
]
RELATED_POST_IDS = [
    "cb957906-b9f4-47f2-9f2f-6352923232ab",
    "30697328-067a-47a1-a270-6ee7535acb09",
    "f226c440-936c-4ab0-9961-fcd06d19672a",
]

TITLE = "【男性向け】夜、なんとなく手が伸びる一杯。――その正体、実は「寂しさ」かもしれません"
EXCERPT = "「今日はもう一杯だけ」のつもりが、気づけば何杯も。その習慣の裏にあるものについて、公的データと研究をもとにお伝えします。"
FOCUS_KEYWORD = "男性 寂しい 結婚 婚活"

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

    nodes.append(p("仕事から帰って、一人の部屋。テレビをつけて、なんとなく缶を開ける。「今日はもう一杯だけ」のつもりが、気づけば何杯も空いている。そんな夜に、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("今日は、その「なんとなく」の正体について、少しだけ真面目にお話しさせてください。"))
    nodes.append(sp())

    nodes.extend(section_heading("それは、寂しさのサインかもしれません"))
    nodes.append(sp())
    nodes.append(p("男性は「寂しい」という感情を、素直に言葉にすることが苦手な傾向があると言われています。悲しい、辛いという感情の代わりに、なんとなく体を動かしたい、なんとなく飲みたい、という形で行動に出やすいんですね。"))
    nodes.append(sp())
    nodes.append(p("これは弱さでも、だらしなさでもありません。感情をそのまま出すより行動で処理するように育ってきた、多くの男性に共通する反応パターンです。右利きの人が意識せず右手を使うのと同じで、無意識に身についた習慣なんです。"))
    nodes.append(sp())
    # [IMG:room]
    nodes.append(p("アメリカ・ブリガムヤング大学のホルト＝ランスタッド教授が148件の研究・30万人以上のデータをまとめた分析では、孤独感がもたらす健康への悪影響は、1日にタバコを15本吸うことや、アルコール依存症と同程度だと報告されています。孤独は、気の持ちようで済ませられるものではなく、体に直接影響する現象なんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("こんなこと、心当たりはありませんか"))
    nodes.append(sp())
    nodes.append(p("休日、特に予定がないと、朝から一人で過ごす時間が長く感じる。"))
    nodes.append(sp())
    nodes.append(p("誰かに連絡したい気分なのに、結局誰にも連絡せずに一日が終わる。"))
    nodes.append(sp())
    nodes.append(p("お酒の量が、この数年で少しずつ増えてきた気がする。"))
    nodes.append(sp())
    nodes.append(p("――どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("「安らぎの場」は、思っている以上に大きい"))
    nodes.append(sp())
    nodes.append(p("国立社会保障・人口問題研究所の出生動向基本調査では、未婚男性が結婚に感じる利点として「精神的な安らぎの場が得られる」と答えた人が31.1%にのぼり、「子どもや家族をもてる」に次いで2番目に多い理由でした。多くの男性が、心のどこかでこの安らぎを求めているということです。"))
    nodes.append(sp())
    nodes.append(p("さらに、厚生労働省の人口動態統計をもとにした分析では、配偶者のいない男性の死亡年齢の中央値は67.2歳、配偶者のいる男性は81.2歳以上と、14年以上の差があると報告されています。年齢層による偏りを取り除いて50歳以上に絞って計算しても、その傾向は変わらないとされています。"))
    nodes.append(sp())
    # [IMG:warmth]
    nodes.append(p("誰かと暮らすということは、単に寂しさを紛らわすということ以上に、生活のリズムや食事、健康管理そのものを大きく変える力を持っているんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("お酒に頼る前に、素直になっていい"))
    nodes.append(sp())
    nodes.append(p("「寂しい」と認めるのは、格好悪いことではありません。むしろ、その気持ちに気づいて素直に行動を変えられる人のほうが、結果的に早く安らぎにたどり着きます。"))
    nodes.append(sp())
    nodes.append(p('一人で抱え込まず、素直に「誰かと一緒にいたい」という気持ちを認めて、婚活という形で一歩を踏み出す。私はそうした素直な選び方を"素直婚"と呼んでいます。'))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今夜、缶に手を伸ばす前に一度だけ、「今、寂しいのかな」と自分に聞いてみてください。それだけで十分です。"))
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

    eyecatch_prompt = (base_style + ", a Japanese man in his 30s sitting alone on a sofa at night in a dim "
        "living room, holding a can of beer, tired contemplative expression, TV glow light, quiet lonely mood")
    room_prompt = (base_style + ", a Japanese man in his 30s sitting alone at a small kitchen table late at "
        "night, a few empty cans nearby, looking down thoughtfully, dim warm lamp light, quiet apartment")
    warmth_prompt = (base_style + ", a Japanese man and woman in their 30s cooking together in a bright home "
        "kitchen, relaxed genuine smiles, warm evening light, cozy domestic atmosphere")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-09-02_sabishisa_dansei_eyecatch.png")
    room_path = generate_image(room_prompt, "2026-09-02_sabishisa_dansei_room.png")
    warmth_path = generate_image(warmth_prompt, "2026-09-02_sabishisa_dansei_warmth.png")

    files = {
        "room": upload_image_file(room_path, "2026-09-02_sabishisa_dansei_room.png"),
        "warmth": upload_image_file(warmth_path, "2026-09-02_sabishisa_dansei_warmth.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("これは弱さでも、だらしなさでもありません。感情をそのまま出すより行動で処理するように育ってきた、多くの男性に共通する反応パターンです。右利きの人が意識せず右手を使うのと同じで、無意識に身についた習慣なんです。", "room", "その一杯は、寂しさが姿を変えたものかもしれません。"),
        ("さらに、厚生労働省の人口動態統計をもとにした分析では、配偶者のいない男性の死亡年齢の中央値は67.2歳、配偶者のいる男性は81.2歳以上と、14年以上の差があると報告されています。年齢層による偏りを取り除いて50歳以上に絞って計算しても、その傾向は変わらないとされています。", "warmth", "誰かと暮らす日常が、生活そのものを変えていきます。"),
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

    composed_path = os.path.join(IMAGES_DIR, "2026-09-02_sabishisa_dansei_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=eyecatch_path,
        main_html='夜、なんとなく<br>手が伸びる<span class="accent">一杯</span>。',
        subtitle_text="――その正体、実は「寂しさ」かもしれません",
        out_path=composed_path,
        main_size=58,
    )
    eyecatch_file = upload_image_file(composed_path, "2026-09-02_sabishisa_dansei_eyecatch_composed.png")
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
