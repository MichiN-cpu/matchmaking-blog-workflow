"""
【女性向け】その「もう疲れた」、気のせいじゃありません。
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
    "ce76d0c1-1fa1-4898-954b-2903a34dbcd4",  # マッチングアプリ
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
]
RELATED_POST_IDS = [
    "f226c440-936c-4ab0-9961-fcd06d19672a",
    "5810c39a-fdf2-495b-8150-55ec665eab2e",
    "eb8a7508-a182-4140-8591-5ad52870214e",
]

TITLE = "【女性向け】その「もう疲れた」、気のせいじゃありません。――マッチングアプリを頑張ってきた人にこそ伝えたいこと"
EXCERPT = "マッチングアプリを頑張るほど疲れてしまうのは、あなたの心が弱いからではありません。心理学と行動科学の視点から、その疲れの正体と、立ち止まっていい理由をお伝えします。"
FOCUS_KEYWORD = "マッチングアプリ 疲れた 女性"

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

    nodes.append(p("マッチングアプリを頑張ってきたあなたへ、まず伝えたいことがあります。"))
    nodes.append(sp())
    nodes.append(p("「もう疲れた」と感じてしまうのは、あなたの心が弱いからでも、婚活の仕方が下手だからでもありません。"))
    nodes.append(sp())

    nodes.extend(section_heading("その疲れには、ちゃんと理由があります"))
    nodes.append(sp())
    nodes.append(p("心理学に「選択のパラドックス」という考え方があります。選択肢が多ければ多いほど人は幸せになれそうに思えますが、実際には選択肢が増えるほど、決断すること自体が苦しくなっていくという性質のことです。"))
    nodes.append(sp())
    nodes.append(p("マッチングアプリは、その選択肢を無限に近い形で見せてくれる仕組みです。次から次へとプロフィールをめくれるからこそ、「今の人でいいのか」「もっと合う人がいるかもしれない」という比較が、終わることなく続いてしまうんですよね。"))
    nodes.append(sp())
    nodes.append(p("さらに行動科学の視点では、意思決定を繰り返すこと自体が脳のエネルギーを消耗させる「決断疲れ」という現象も知られています。一日に何十人分ものプロフィールを判断し続けていれば、心が疲れてしまうのは当然の反応なんです。"))
    nodes.append(sp())
    # [IMG:scrolling]
    nodes.append(p("これは、右利きの人が意識せず右手を使うのと同じで、「もっといい人がいるかも」と探し続けてしまうことも、多くの人が自然と身につけてしまう反応パターンなんです。性格の弱さでも、婚活が下手なわけでもありません。"))
    nodes.append(sp())

    nodes.extend(section_heading("こんなこと、心当たりはありませんか"))
    nodes.append(sp())
    nodes.append(p("マッチした後も、本当にこの人でいいのか気になって他のプロフィールを見てしまう。"))
    nodes.append(sp())
    nodes.append(p("メッセージのやり取りに疲れて、既読のまま返す気力が湧かない日がある。"))
    nodes.append(sp())
    nodes.append(p("せっかく会えても、また一からやり直しかと思うと気持ちが重くなる。"))
    nodes.append(sp())
    nodes.append(p("――どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("「探す」を、誰かに預けてもいい"))
    nodes.append(sp())
    nodes.append(p("社会学者ジグムント・バウマンは、現代の恋愛や結婚が「いつでも他の選択肢に乗り換えられる」流動的な関係になっていることを指摘しています。自由であることは心地よい反面、常に自分一人で選び続けなければならない負担も生んでいます。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、婚活には「一人で探し続けない」という選択肢があってもいいと思うんです。仲人がいる婚活は、プロフィールを無限にめくり続ける代わりに、あなたに合いそうな方をこちらである程度絞ってお伝えする形になります。"))
    nodes.append(sp())
    # [IMG:relief]
    nodes.append(p("「探す」という一番エネルギーを使う部分を預けられるだけで、驚くほど気持ちが軽くなる方が多いんです。無理に自分を追い込んで探し続けるのではなく、素直に「もう少し力を抜きたい」と思う自分を認めてあげる。それも立派な婚活の進め方だと私は思います。"))
    nodes.append(sp())
    nodes.append(p('望みや不安を無理に一人で抱え込まず、素直に人に預けながら進めていく。私はこれを"素直婚"と呼んでいます。'))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、アプリを開く前に一度だけ「今、疲れていないかな」と自分に聞いてみてください。疲れていたら、今日は開かなくて大丈夫です。"))
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

    eyecatch_prompt = (base_style + ", in her late 20s, sitting on a sofa at night looking at a smartphone "
        "with a tired weary expression, phone screen glow on her face, soft dim room lighting")
    scrolling_prompt = (base_style + ", close up of hands holding a smartphone scrolling through profile "
        "photos, blurred background, focused on the phone screen and hands only, no visible profile content")
    relief_prompt = (base_style + ", in her late 20s, sitting by a window with a cup of tea, phone face-down "
        "on the table beside her, calm relieved expression, soft morning daylight")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-09-02_app_tsukare_josei_eyecatch.png")
    scrolling_path = generate_image(scrolling_prompt, "2026-09-02_app_tsukare_josei_scrolling.png")
    relief_path = generate_image(relief_prompt, "2026-09-02_app_tsukare_josei_relief.png")

    files = {
        "scrolling": upload_image_file(scrolling_path, "2026-09-02_app_tsukare_josei_scrolling.png"),
        "relief":    upload_image_file(relief_path, "2026-09-02_app_tsukare_josei_relief.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("さらに行動科学の視点では、意思決定を繰り返すこと自体が脳のエネルギーを消耗させる「決断疲れ」という現象も知られています。一日に何十人分ものプロフィールを判断し続けていれば、心が疲れてしまうのは当然の反応なんです。", "scrolling", "終わりのないスクロールが、心を静かに消耗させていきます。"),
        ("だからこそ、婚活には「一人で探し続けない」という選択肢があってもいいと思うんです。仲人がいる婚活は、プロフィールを無限にめくり続ける代わりに、あなたに合いそうな方をこちらである程度絞ってお伝えする形になります。", "relief", "「探す」を預けるだけで、心はふっと軽くなります。"),
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

    # アイキャッチはタイトルのフックを文字焼き込みしてから設定
    composed_path = os.path.join(IMAGES_DIR, "2026-09-02_app_tsukare_josei_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=eyecatch_path,
        main_html='その「もう疲れた」、<br><span class="accent">気のせいじゃありません</span>',
        subtitle_text="――マッチングアプリを頑張ってきた人にこそ伝えたいこと",
        out_path=composed_path,
    )
    eyecatch_file = upload_image_file(composed_path, "2026-09-02_app_tsukare_josei_eyecatch_composed.png")
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
