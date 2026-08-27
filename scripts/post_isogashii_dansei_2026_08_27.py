"""
【男性向け】忙しい人ほど、婚活はうまくいく。
カテゴリ: 無料相談の前に読む
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
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む
]
TAG_IDS = [
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
]
RELATED_POST_IDS = [
    "48661e48-abd6-4d17-8ea0-3b9fe10a2c0b",  # 「なんでできないんだろう」を卒業する
    "97989a04-0b1e-471f-929d-7d34528d6b32",  # "弱音を吐けない"をやめた男性から
    "a795be5b-c16c-4fed-9d55-1623b103fa25",  # 「結婚はまだ先でいい」と思っていた男性たち
]

TITLE = "【男性向け】忙しい人ほど、婚活はうまくいく。"
EXCERPT = "「仕事が忙しくてデートの時間が取れない」——婚活を始める前にそう感じている男性へ。実は忙しさは、婚活が進まない本当の理由ではないかもしれません。忙しい人ほどうまくいく婚活の考え方をお伝えします。"
FOCUS_KEYWORD = "婚活 忙しい 時間がない 男性"

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

    nodes.append(p("今日は、無料相談でとてもよく聞かれる質問についてお話ししたいと思います。"))
    nodes.append(sp())
    nodes.append(p("「仕事が忙しくて、なかなかデートの時間が取れないから婚活できない」って、本当なんでしょうか。"))
    nodes.append(sp())
    nodes.append(p("正直に言うと、これ、半分は本当で、半分は違うんです。今日はその「違う半分」の話をさせてください。"))
    nodes.append(sp())

    nodes.extend(section_heading("帰りの電車で、もうぐったり"))
    nodes.append(sp())
    nodes.append(p("平日は朝から晩まで仕事。帰りの電車では座った瞬間に目を閉じてしまう。休日は溜まった家事や睡眠に充てて、気づけば週末も終わっている。"))
    nodes.append(sp())
    nodes.append(p("そんな毎日を送っていると、「婚活」なんて言葉自体が、なんだか自分には縁遠いもののように感じられてくるんですよね。"))
    nodes.append(sp())
    nodes.append(p("デートの約束をする気力もないし、そもそも新しい人と会って気を遣うこと自体が、もう一つの仕事のように重く感じられる。"))
    nodes.append(sp())
    nodes.append(p("わかります。それ、サボっているわけでも、結婚する気がないわけでもないんですよね。ただ、単純に、体力と気力の残量がゼロに近いだけなんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("それ、性格じゃなくて「いつものクセ」かもしれません"))
    nodes.append(sp())
    nodes.append(p("面白いことに、私たちは疲れているとき、無意識に「省エネモード」に入ります。新しいことより慣れたことを選ぶ、決断を先延ばしにする、今日はいいやと後回しにする。"))
    nodes.append(sp())
    nodes.append(p("これ、右利きの人が疲れているときほど無意識に右手を使ってしまうのと同じで、脳が一番エネルギーを使わない道を自動的に選んでいるだけなんです。"))
    nodes.append(sp())
    nodes.append(p("つまり「婚活する気力がない」は、性格の問題ではなく、疲れた脳が選ぶいつもの反応パターンだということ。"))
    nodes.append(sp())
    nodes.append(p("これに気づかないまま、「自分は結婚に向いていないのかも」「本気度が足りないのかも」と自分を責めてしまう男性が、実はとても多いんです。"))
    nodes.append(sp())
    nodes.append(p("行動科学の世界では、これは「意思決定疲労（ディシジョン・ファティーグ）」と呼ばれています。1日にたくさんの判断をこなした脳は、夕方には新しい選択をする力がほとんど残っていない状態になる。"))
    nodes.append(sp())
    nodes.append(p("婚活のような「新しい決断の連続」が、疲れた脳にとって一番後回しにされやすいのは、実はとても理にかなったことなんですね。"))
    nodes.append(sp())
    # [IMG:night]
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("平日の夜、マッチングアプリを開いても、メッセージを打つ気力が出ない。休日にお見合いの予定を入れようとして、「今週はちょっと」と先延ばしにしてしまう。婚活したい気持ちはあるのに、いざとなると新しい予定を組むこと自体が億劫に感じる。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("忙しさより、実は「消耗」の使い道が問題"))
    nodes.append(sp())
    nodes.append(p("もう一つ、大事な視点をお伝えします。社会学の視点で見ると、今の日本の働き方は、独身の男性にとってかなり不利にできています。"))
    nodes.append(sp())
    nodes.append(p("長時間労働が当たり前だった時代の名残で、「出会いは自然に生まれるもの」という前提で社会の仕組みが作られたままなんです。でも実際は、職場恋愛も合コンも減っている今、意識して機会を作らないと、出会いは向こうからやってきません。"))
    nodes.append(sp())
    nodes.append(p("さらに、心身の健康の観点でも興味深いデータがあります。睡眠不足やストレスが続くと、恋愛や新しい関係づくりへの意欲そのものが下がることがわかっています。"))
    nodes.append(sp())
    nodes.append(p("忙しさそのものより、忙しさによる「慢性的な消耗」が、婚活への一歩を重くしているケースが、実はとても多いんです。"))
    nodes.append(sp())
    nodes.append(p("だとすれば、対処法は「もっと頑張って時間を作る」ことじゃないんですよね。限られた時間とエネルギーを、どこに使うかを変えることなんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("具体的にできること、根っこから変わること"))
    nodes.append(sp())
    nodes.append(p("まず、今日からできる小さなことから。婚活を「新しい負担」として自分の可処分時間の中に押し込もうとすると、必ず後回しになります。"))
    nodes.append(sp())
    nodes.append(p("そうではなく、「婚活のことは、任せられる部分は任せる」という発想に切り替えてみてください。"))
    nodes.append(sp())
    nodes.append(p("お相手探し、日程調整、当日の段取り。ここを一人で抱え込まずに仲人に任せてしまえば、男性側がやることは「決められた日時に、決められた場所へ行く」だけになります。"))
    nodes.append(sp())
    nodes.append(p("実際、私たちのところでは、お見合いが組めなかった会員は今のところ一人もいません。忙しい方ほど、この「決断の外注」が効くんです。"))
    nodes.append(sp())
    nodes.append(p("そしてもう一つ、もう少し根っこの話をさせてください。「忙しいから」を理由にし続けてしまう背景には、実は「本当に向き合うのが少し怖い」という気持ちが隠れていることもあります。"))
    nodes.append(sp())
    nodes.append(p("忙しさは、便利な避難場所にもなり得るんですね。これは弱さではなく、誰にでもある自然な反応です。"))
    nodes.append(sp())
    nodes.append(p("この「いつものクセ」に思い当たる節があるならば、心理カウンセラーでもある仲人の私と一緒に、少しずつ手放していきませんか？手放せば手放すほど、婚活も、その先の結婚生活も、驚くほど軽やかに進み始めます。"))
    nodes.append(sp())

    nodes.extend(section_heading("じんわり、でも確かに変わっていく"))
    nodes.append(sp())
    nodes.append(p("忙しさを言い訳にしなくなった男性たちを見ていると、共通していることがあります。それは、婚活を「もう一つのタスク」ではなく、「一日の中の、ほっとする時間」に変えていくことです。"))
    nodes.append(sp())
    nodes.append(p("仕事終わりのカフェで、仲人からのメッセージを見て小さく笑う。週末の予定に、お見合いという新しい楽しみが一つ増える。忙しい毎日の中に、自分のための時間がちゃんとあることに気づく。"))
    nodes.append(sp())
    nodes.append(p("そうやって少しずつ、婚活自体が「疲れることリスト」から「楽しみなことリスト」に移っていくんです。"))
    nodes.append(sp())
    # [IMG:cafe]
    nodes.append(p("そしてその先には、仕事で疲れて帰った夜に、玄関で「おかえり」と言ってくれる人がいる暮らしが待っています。"))
    nodes.append(sp())
    nodes.append(p("忙しい毎日だからこそ、隣で笑ってくれる人の存在が、何よりの支えになるんですよね。"))
    nodes.append(sp())
    nodes.append(p("エネルギーチャージの時間になる結婚生活が、私のお勧めしたい”素直婚”なんです💕"))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今週、婚活のことを考える時間が5分も取れなかったとしても大丈夫です。まずは「今の忙しさは、自分を否定する理由じゃない」と、一度だけ自分に言ってあげてください。それだけで十分です。"))
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
                  "handsome Japanese man in his 30s, natural refined features, model-like appearance, clear skin, "
                  "real-world setting, professional lifestyle photography style, shallow depth of field, "
                  "clean bright modern atmosphere, no text, no warm yellowish tint")

    eyecatch_prompt = (base_style + ", sitting alone on a train seat with eyes closed, tired but peaceful "
        "expression, evening city lights blurred through the window, business suit, briefcase on his lap")
    night_prompt = (base_style + ", sitting at a desk late in the evening, looking at a smartphone screen "
        "showing a messaging app, hesitant thoughtful expression, warm desk lamp light, clean modern room")
    cafe_prompt = (base_style + ", sitting across from a Japanese woman at a cozy cafe table, both smiling "
        "warmly at each other, soft evening light, relaxed happy atmosphere, professional lifestyle photography")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-08-27_isogashii_dansei_eyecatch.png")
    night_path    = generate_image(night_prompt, "2026-08-27_isogashii_dansei_night.png")
    cafe_path     = generate_image(cafe_prompt, "2026-08-27_isogashii_dansei_cafe.png")

    files = {
        "eyecatch": upload_image_file(eyecatch_path, "2026-08-27_isogashii_dansei_eyecatch.png"),
        "night":    upload_image_file(night_path, "2026-08-27_isogashii_dansei_night.png"),
        "cafe":     upload_image_file(cafe_path, "2026-08-27_isogashii_dansei_cafe.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("婚活のような「新しい決断の連続」が、疲れた脳にとって一番後回しにされやすいのは、実はとても理にかなったことなんですね。", "night", "メッセージを開いても、指が止まってしまう夜もある。"),
        ("そうやって少しずつ、婚活自体が「疲れることリスト」から「楽しみなことリスト」に移っていくんです。", "cafe", "忙しい毎日の中に、こんな時間が増えていく。"),
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
