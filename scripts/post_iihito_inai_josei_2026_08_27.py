"""
【女性向け】本当は、素敵な人はちゃんといます。
カテゴリ: お見合い
2026-08-27
"""
import os, uuid, base64, requests
from openai import OpenAI

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")

client = OpenAI(api_key=OPENAI_KEY)

CATEGORY_IDS = [
    "5089ac63-e2ce-4de1-b472-3512a77401af",  # お見合い
]
TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "d372d6c7-06f8-47fe-a647-6229a0b94c80",  # お見合い
    "c2b8cde4-4435-435b-8b65-e02c2ba9e761",  # プロフィール
]
RELATED_POST_IDS = [
    "14ec5353-eba7-4b05-88fa-16d99fd521d1",  # 受け身をやめたら、半年でご成婚できた話。
    "2cf3dbc8-6b9d-471a-bc78-8fe3c75f4ff4",  # 「聞き上手」をやめたら、うまくいく
    "da8998ae-c9f4-42f1-beb6-84d1b348d133",  # "一人で踏み出すのが怖い"人ほど、実は婚活がうまくいく
]

TITLE = "本当は、素敵な人はちゃんといます。"
EXCERPT = "「いい人がいない」——婚活中の女性からよく聞く言葉です。でも実は、プロフィールだけで\"ピンとくる\"人が多い方が、むしろ珍しいのかもしれません。松山市の結婚相談所あすなる愛媛の中嶋美知が、その理由と試してほしいワークをお伝えします。"
FOCUS_KEYWORD = "婚活 いい人がいない 女性 お見合い"

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

    nodes.append(p("無料相談でよくお聞きするのが、「いい人がいないんです」というお言葉です。そのお気持ち、わからなくもないんです。ただ、今日は少しだけ違う角度からお話をさせてください。"))
    nodes.append(sp())
    nodes.append(p("一つ、質問させてください。これまで、あなたが「ビビッときた」男性は、どれくらいいらっしゃいますか。"))
    nodes.append(sp())

    nodes.extend(section_heading("一目惚れは、実はそんなに多くない"))
    nodes.append(sp())
    nodes.append(p("多くの女性にとって、誰かを好きになったきっかけは、実は一目惚れではないと思うんです。よほど特別な出会いでない限り、たいていは、同じクラスだったり、同じ部活だったり、同じ職場だったり、同じ趣味のサークルで一緒に練習したり。そうやって関わるうちに、だんだんとその人の人柄がわかってきて、最初は何も感じなかった相手が、少しずつ素敵に見えてくる。そんなパターンがほとんどなんですよね。"))
    nodes.append(sp())
    nodes.append(p("これは心理学でも説明できることで、「単純接触効果」と呼ばれています。人は繰り返し接するものに対して、自然と好意を持ちやすくなるという心の働きです。恋愛も同じで、時間をかけて関わるうちに好きになっていく人の方が、実はとても多いんです。"))
    nodes.append(sp())
    nodes.append(p("だけど、結婚相談所でのお見合いとなると、まず並ぶのはプロフィール写真とプロフィール文章です。声も聞いていないし、話しているときの表情も、言葉のリズムもトーンも、どんな背景からその行動をしているのか、どんな思いでその言葉を言ってくれたのかも、まだ何もわかりません。優しさや思いやり、可愛らしい不器用さにも、まだ気づけない状態なんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("ピンとこないのは、自然なことです"))
    nodes.append(sp())
    nodes.append(p("コミュニケーション学の研究でも、私たちが相手から受け取る情報のうち、言葉そのものよりも、声のトーンや表情、間の取り方といった非言語の部分がとても大きな役割を果たしていると言われています。プロフィールには、まさにその大切な部分が抜け落ちているんです。だから「ピンとこない」のは、当たり前のことなんです。"))
    nodes.append(sp())
    nodes.append(p("もし写真と文字の情報だけで「いい人だ」と思える相手が、ものすごくたくさんいるという方がいらっしゃったら、その方はきっと、あっという間にご成婚されると思います。そのくらい、紙の情報だけで恋心が動く人は、実は少数派なんですよね。"))
    nodes.append(sp())
    nodes.append(p("これは、右利きの人が意識せず右手を使うのと似ています。「関わりながら好きになっていく」というのは、多くの人にとって自然な、慣れた反応パターンなんです。性格の問題でも、相性が悪いわけでもありません。"))
    nodes.append(sp())
    # [IMG:contact]
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("お見合い写真を見ても、特に何も感じない。"))
    nodes.append(sp())
    nodes.append(p("プロフィール文を読んでも、「悪くはないけど……」で止まってしまう。"))
    nodes.append(sp())
    nodes.append(p("会ったこともないのに、なんとなく「違うかも」と思ってしまう。"))
    nodes.append(sp())
    nodes.append(p("――どれか一つでも「あるかも」と思った方は、このあとのお話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("駅前100人ワーク"))
    nodes.append(sp())
    nodes.append(p("そこで、よくお勧めしているワークがあります。"))
    nodes.append(sp())
    nodes.append(p("駅前で、通りすがりの男性を一人ずつ見てみてください。あなたにふさわしい年齢の男性が100人目の前を通ったとしたら、そのうち何人を「素敵だな」と思えそうか、想像してみるんです。"))
    nodes.append(sp())
    nodes.append(p("もし100人中50人くらい、「お見合いしてもいいな」「デートしてみたいな」と思えるなら、あなたはきっと、そんなに悩んでいないはずです。"))
    nodes.append(sp())
    # [IMG:station]
    nodes.append(p("もし100人中10人も「いいな」と思えないとしたら――それは、あなたが相手をよく知ってからでないと好きになれないタイプだということです。だとしたら、成功への一番の近道は、まず出会ってみること。まず話してみること。まずデートしてみることなんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("じんわり、でも確かに変わっていく"))
    nodes.append(sp())
    nodes.append(p("写真や文章だけで判断しようとするのをやめて、実際に会って、話して、少しずつ相手を知っていく。そうすると、最初は「特に何も感じなかった」相手の、ふとした優しさや、話し方の温かさ、笑ったときの表情に気づく瞬間がやってきます。それは、ドラマのような激しい高まりではないかもしれません。でも、じんわりと、確かに育っていく好きという気持ちです。"))
    nodes.append(sp())
    nodes.append(p("自分の思いを押し付けるでもなく、遠慮するでもなく、素直に「いいな」と思ったことを、ふたりで少しずつ確かめ合いながら進んでいく。それが私のお勧めしたい\"素直婚\"です。"))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今週、駅やお店で誰かとすれ違うとき、一度だけ「この人はどうかな」と、ほんの少し想像してみてください。それだけで、自分がどんなタイプなのか、ヒントが見えてくるはずです。"))
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

    eyecatch_prompt = (base_style + ", in her 30s, sitting alone at a cafe table looking at a smartphone "
        "showing a profile photo, thoughtful neutral expression, natural daylight through a window")
    contact_prompt = (base_style + ", a small group of Japanese people in their 20s-30s at a casual hobby "
        "club or workplace setting, chatting and smiling naturally together, warm daytime light")
    station_prompt = (base_style + ", in her 30s, standing at a train station plaza, looking thoughtfully "
        "at the passing crowd, soft daylight")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-08-27_iihito_inai_josei_eyecatch.png")
    contact_path  = generate_image(contact_prompt, "2026-08-27_iihito_inai_josei_contact.png")
    station_path  = generate_image(station_prompt, "2026-08-27_iihito_inai_josei_station.png")

    files = {
        "eyecatch": upload_image_file(eyecatch_path, "2026-08-27_iihito_inai_josei_eyecatch.png"),
        "contact":  upload_image_file(contact_path, "2026-08-27_iihito_inai_josei_contact.png"),
        "station":  upload_image_file(station_path, "2026-08-27_iihito_inai_josei_station.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("これは、右利きの人が意識せず右手を使うのと似ています。「関わりながら好きになっていく」というのは、多くの人にとって自然な、慣れた反応パターンなんです。性格の問題でも、相性が悪いわけでもありません。", "contact", "関わるうちに、だんだんと素敵に見えてくる。"),
        ("もし100人中50人くらい、「お見合いしてもいいな」「デートしてみたいな」と思えるなら、あなたはきっと、そんなに悩んでいないはずです。", "station", "100人のうち、何人が素敵に見えるでしょうか。"),
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
