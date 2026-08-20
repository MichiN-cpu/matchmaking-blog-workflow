"""
【男性向け】「彼女、最近ちょっと元気ない気がする」——そんなあなたへ。
カテゴリ: 真剣交際
2026-08-21
"""
import os, time, uuid, base64, requests
from openai import OpenAI

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")

client = OpenAI(api_key=OPENAI_KEY)

CATEGORY_IDS = [
    "5414dab5-ded7-4b15-a88a-d679d6fd3c71",  # 真剣交際
]
TAG_IDS = [
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "0ddde006-b527-4852-8056-8cdb87174e82",  # 真剣交際
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
]
RELATED_POST_IDS = [
    "d62fc137-2e3b-494b-bf2f-c4a121f342c4",  # 【男性向け】結婚がリアルになってきて「なんだか気分が重い」
    "97989a04-0b1e-471f-929d-7d34528d6b32",  # 【男性向け】"弱音を吐けない"をやめた男性から
    "35d610c7-50ee-45ad-8d0a-310b7893b9b6",  # 【女性向け】この人で本当にいいのかな（対の記事）
]

TITLE = "「彼女、最近ちょっと元気ない気がする」——そんなあなたへ。"
EXCERPT = "真剣交際が具体的になるにつれて、彼女の様子がなんとなくいつもと違う——そんな時、実は彼女の中で静かな緊張が起きているのかもしれません。その正体と、男性にできる寄り添い方についてお話しします。"
FOCUS_KEYWORD = "真剣交際 彼女の様子 プレッシャー"

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
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    nodes.append(p("彼女、最近ちょっと元気ない気がする。理由を聞いても「大丈夫」としか言わない。でも、なんとなくいつもと違う気がする。"))
    nodes.append(sp())
    nodes.append(p("——そんな感覚、ありませんか。それ、実は彼女の中で静かに起きていることかもしれません。今日はその正体と、そんな時に男性ができることについてお話ししたいと思います。"))
    nodes.append(sp())
    nodes.append(p("真剣交際に入ると、お互いの家族への挨拶、結婚式のこと、そして指輪のこと。いろんなことが一気に具体的になっていきます。女性の中には、転職や転勤を考えて進めていく方もいらっしゃいます。今まで「いつか」だった話が、急に「来月」「来年」という現実の予定に変わっていくんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("それ、身体の方が先に気づいていることがあります"))
    nodes.append(sp())
    nodes.append(p("本人が思っている以上に、頭と心は動いています。そして、それが自覚できる不安として形になる前に、身体の凝りや不調として先に出てしまうことがあるんです。夜、なんだか変な夢を見たと話す。そんなサインも実は珍しくありません。"))
    nodes.append(sp())
    nodes.append(p("心理学の世界に「社会的再適応評価尺度」という考え方があります。人生の大きな出来事がどれだけ心身の負担になるかを数値化したもので、結婚や婚約は、たとえポジティブな出来事であっても、上位に位置づけられるほどの負荷として扱われています。嬉しいことのはずなのに、身体はちゃんと「大きな変化」として受け止めて緊張している。それくらい自然な反応なんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("実は、私もそうでした"))
    nodes.append(sp())
    nodes.append(p("真剣交際に入って、プロポーズも決まって。嬉しいはずなのに、気づいたら肩や首がガチガチに凝っていて、口内炎までできていました。"))
    nodes.append(sp())
    nodes.append(p("このままで本当に大丈夫なのかな、という漠然とした不安が、身体の方に先に出ていたんだと思います。"))
    nodes.append(sp())
    # [IMG:tension]
    nodes.append(p("そんな時、私はプレッシャーを感じているかもしれない、と彼に話してみたんです。そうしたら彼が、「ひとりで考えないで、一緒に一つ一つ進めていこう。先のことまで考えても決められないこと沢山あるから、目の前の一つを終えることから一緒にやっていこう」と言ってくれて。"))
    nodes.append(sp())
    nodes.append(p("その言葉を聞いた瞬間、あんなに酷かった肩の凝りが、スーッと消えていったんです。不思議なくらいでした。"))
    nodes.append(sp())

    nodes.extend(section_heading("不安は、性格ではなく反応パターンです"))
    nodes.append(sp())
    nodes.append(p("右利きの人が意識せず右手を使うのと同じように、「一人で抱え込んで、全部を先まで見通そうとする」というのも、実は一つの慣れた反応パターンなんです。彼女の性格が心配性だから、というわけじゃありません。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、パターンを変えることもできます。「全部を一気に決めなきゃ」から、「目の前の一つずつ、一緒に」に切り替えるだけで、身体の反応まで変わっていくんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("こんなこと、心当たりはありませんか"))
    nodes.append(sp())
    nodes.append(p("彼女が最近、肩や首をやたら揉んでいたり。急に口内炎ができていたり。「変な夢見た」と話す回数が増えていたり。"))
    nodes.append(sp())
    nodes.append(p("理由を聞いても「大丈夫、なんでもない」としか返ってこない。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("彼女のペースを大事にしてあげてください"))
    nodes.append(sp())
    nodes.append(p("真剣交際に入って、プロポーズも決まったら、安心してゴンゴン進めたくなる気持ち、よくわかります。でもそんな時こそ、彼女をよく見てあげてください。"))
    nodes.append(sp())
    nodes.append(p("「大丈夫、落ち着いて」と、彼女のペースを大事にしてあげること。そして、全部を一気に決めようとせず、目の前の一つを一緒に終えることから始めること。それだけで、彼女の中の緊張はゆるんでいきます。"))
    nodes.append(sp())
    nodes.append(p("そうすると彼女も、イレギュラーなことが起きた時に頼りになる人、やっぱりこの人でよかった、とますます信頼を深めてくれるはずです。結婚式の準備で予定外のことが起きた時も、新しい生活でトラブルがあった時も、「この人となら大丈夫」と思える関係が、ここから育っていきます。"))
    nodes.append(sp())
    # [IMG:together]

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
    base_style = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
                  "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
                  "real-world setting, professional lifestyle photography style, shallow depth of field, "
                  "clean bright modern atmosphere, no text, black hair")

    eyecatch_prompt = (base_style + ", a Japanese couple in their early thirties sitting together on a sofa "
        "at home in the evening, the man gently placing his hand on the woman's shoulder with a calm "
        "reassuring expression, the woman looking down thoughtfully with a subtle worried expression, "
        "a notebook and papers about wedding planning on the low table in front of them")
    tension_prompt = (base_style + ", a Japanese woman in her early thirties sitting alone at a table near "
        "a window, pressing her own fingers into her shoulder and neck as if relieving stiffness, a "
        "distant thoughtful expression, a cup of tea on the table")
    together_prompt = (base_style + ", a Japanese couple in their early thirties sitting side by side at a "
        "table, both looking together at a small notebook and smiling gently, calm and relaxed atmosphere")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-08-21_kanojo_genkinai_eyecatch.png")
    tension_path  = generate_image(tension_prompt, "2026-08-21_kanojo_genkinai_tension.png")
    together_path = generate_image(together_prompt, "2026-08-21_kanojo_genkinai_together.png")

    files = {
        "eyecatch": upload_image_file(eyecatch_path, "2026-08-21_kanojo_genkinai_eyecatch.png"),
        "tension":  upload_image_file(tension_path, "2026-08-21_kanojo_genkinai_tension.png"),
        "together": upload_image_file(together_path, "2026-08-21_kanojo_genkinai_together.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("このままで本当に大丈夫なのかな、という漠然とした不安が、身体の方に先に出ていたんだと思います。", "tension", "身体の方が、先に緊張を教えてくれることがあります。"),
        ("「この人となら大丈夫」と思える関係が、ここから育っていきます。", "together", "一つずつ、一緒に。それだけで安心は育っていきます。"),
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

    eyecatch = files["eyecatch"]
    media_patch = {
        "draftPost": {"media": {"custom": True, "wixMedia": {"image": {
            "id": eyecatch.get("id", ""), "url": eyecatch["url"],
            "height": eyecatch.get("height", 1024), "width": eyecatch.get("width", 1536),
            "filename": eyecatch.get("displayName", "eyecatch.png"),
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
