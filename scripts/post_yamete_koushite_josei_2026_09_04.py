"""
【女性向け】その「やめて」、彼にはうまく届いていないかもしれません
カテゴリ: 仮交際
2026-09-04
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
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "a1cddd3a-c52b-47f4-b1bf-3c8ce905ebc5",  # コミュニケーション心理学
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
]
RELATED_POST_IDS = [
    "d9f205bf-f8ee-45af-894e-62b0cb82d5dc",
    "35d610c7-50ee-45ad-8d0a-310b7893b9b6",
    "f71ec040-995d-4853-96b3-79d663703958",
]

TITLE = "【女性向け】その「やめて」、彼にはうまく届いていないかもしれません"
EXCERPT = "「前も言ったのに」その一言、実は半分も伝わっていないのかもしれません。女性の高い察する力と、男性が苦手な察すること。心理学の視点から、伝わる伝え方をお伝えします。"
FOCUS_KEYWORD = "男性 コミュニケーション 伝わらない"

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

    nodes.append(p("「前にも言ったよね」「なんで同じことするの」って、思わずため息をついたこと、ありませんか。"))
    nodes.append(sp())
    nodes.append(p("女性って、本当に察する力が高いんですよね。相手が「やめて」って言えば、その裏にある「本当はこうしてほしい」まで、瞬時に汲み取ってしまう。言葉にならない部分まで補って理解する、ある意味すごい能力なんです。"))
    nodes.append(sp())
    nodes.append(p("でもね、男性はそこが本当に苦手なんです。これは冷たいとか愛がないとかじゃなくて、単純に「察する」というコミュニケーションのOSが違うだけ、というのが私の実感です。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、彼に「やめて」と言うだけでは、実は半分も伝わっていないことが多いんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("「やめて」は、なぜ届かないのか"))
    nodes.append(sp())
    nodes.append(p("面白い実験があって。「今からシロクマのことを考えないでください」と言われると、逆にシロクマのことで頭がいっぱいになってしまう、という心理学の有名な研究があります（ダニエル・ウェグナーの「シロクマ実験」）。人間の脳は「〜しない」を理解するとき、一度その行動そのものを思い浮かべてからじゃないと否定できない、という不思議な仕組みを持っているんですね。"))
    nodes.append(sp())
    nodes.append(p("「やめて」も同じです。彼の頭の中では、一瞬「やめてと言われたその行動」がくっきり浮かぶ。でも、その代わりに何をすればいいのかは、教えてもらっていない。"))
    nodes.append(sp())
    # [IMG:frozen]
    nodes.append(p("そしてここでもう一つ、男性特有の傾向が重なります。正解がわからないと、動けなくなってしまう。失敗するのが怖くて、フリーズしてしまうんです。「察しろ」と言われても、正解の選択肢がいくつもある中でどれが正解かわからないから、結局何もできない。悪気があるわけじゃなく、本当に「わからなくて動けない」だけのことが多いんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("「やめて」を「こうして」に変えてみる"))
    nodes.append(sp())
    nodes.append(p("だから、こう言い換えてみてほしいんです。"))
    nodes.append(sp())
    nodes.append(p("「やめて」ではなく「こうして」。"))
    nodes.append(sp())
    nodes.append(p('たとえば、「スマホばかり見ないで」ではなく「10分だけでいいから、私の話を聞いてほしいな」。「もっと連絡して」ではなく「寝る前に"おやすみ"の一言だけでも嬉しいな」というふうに。'))
    nodes.append(sp())
    # [IMG:conversation]
    nodes.append(p("行動科学の世界では、これを「ポジティブ・インストラクション」と呼んだりします。禁止形の指示より、具体的にしてほしい行動を伝えるほうが、脳は圧倒的に処理しやすく、実行に移しやすいことがわかっています。相手を責めているわけじゃなくて、「こうしてくれると嬉しい」という、あなたの願いを伝えるだけ。それだけで、彼にとっての「正解」が、急にはっきり見えてくるんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("心の中で思っているだけ、は伝わっていない"))
    nodes.append(sp())
    nodes.append(p("ここでもう一つ、大事な話をさせてください。"))
    nodes.append(sp())
    nodes.append(p("「本当はやめてほしいのに」と心の中で思っているだけ、というパターンもよくあります。言わなくてもわかってほしい、察してほしい、という気持ち、すごくよくわかります。私自身も、かつてそうでした。でも、彼にとってはそれ、存在していないのと同じなんですよね。"))
    nodes.append(sp())
    nodes.append(p("そして「なんでそんなことするの？」という聞き方も、実はほとんど意味をなしません。これは心理学者ジョン・ゴットマンが「批判」と呼ぶコミュニケーションの型に近くて、相手を責める言葉として脳に届いてしまう。責められた、と感じた瞬間、男性の脳は「防御」か「撤退」というスイッチが入りやすいと言われています。素直に応じるどころか、心を閉ざしてしまう。結果的に、あなたが本当は求めていた「近づいてほしい」という気持ちとは真逆に、彼との距離がどんどん遠のいていってしまうんです。"))
    nodes.append(sp())

    nodes.append(p("だからこそ、伝え方を変えてみる。それだけで、関係はけっこう変わります。"))
    nodes.append(sp())
    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("これは仮交際・真剣交際に進んでいくお相手との間でも、実はすごく大事なポイントです。「言わなくてもわかってほしい」を手放して、「こうしてくれると嬉しいな」を口にする練習を、婚活のうちから少しずつ始めてみませんか。きっと、この先の結婚生活でも、ずっと役立つスキルになるはずです。"))
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

    eyecatch_prompt = (base_style + ", a Japanese man in his 30s sitting on a sofa looking uncertain and a bit lost, "
        "a Japanese woman nearby with a gentle patient expression, soft evening indoor light, calm mood")
    frozen_prompt = (base_style + ", a Japanese man in his 30s standing still indoors with a puzzled, frozen expression, "
        "hand near his head, unsure what to do, soft daylight through a window")
    conversation_prompt = (base_style + ", a Japanese couple in their 30s sitting across a small table having a calm, "
        "warm conversation, both leaning slightly forward, soft smiles, cozy cafe interior, gentle daylight")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-09-04_yamete_koushite_eyecatch.png")
    frozen_path = generate_image(frozen_prompt, "2026-09-04_yamete_koushite_frozen.png")
    conversation_path = generate_image(conversation_prompt, "2026-09-04_yamete_koushite_conversation.png")

    files = {
        "frozen": upload_image_file(frozen_path, "2026-09-04_yamete_koushite_frozen.png"),
        "conversation": upload_image_file(conversation_path, "2026-09-04_yamete_koushite_conversation.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("そしてここでもう一つ、男性特有の傾向が重なります。正解がわからないと、動けなくなってしまう。失敗するのが怖くて、フリーズしてしまうんです。「察しろ」と言われても、正解の選択肢がいくつもある中でどれが正解かわからないから、結局何もできない。悪気があるわけじゃなく、本当に「わからなくて動けない」だけのことが多いんですよね。", "frozen", "正解がわからないと、彼はただ立ち尽くしてしまいます。"),
        ("行動科学の世界では、これを「ポジティブ・インストラクション」と呼んだりします。禁止形の指示より、具体的にしてほしい行動を伝えるほうが、脳は圧倒的に処理しやすく、実行に移しやすいことがわかっています。相手を責めているわけじゃなくて、「こうしてくれると嬉しい」という、あなたの願いを伝えるだけ。それだけで、彼にとっての「正解」が、急にはっきり見えてくるんです。", "conversation", "「こうしてくれると嬉しい」――それだけで、彼にも正解が見えてきます。"),
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

    composed_path = os.path.join(IMAGES_DIR, "2026-09-04_yamete_koushite_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=eyecatch_path,
        main_html='その<span class="accent">「やめて」</span>、<br>彼にはうまく<br>届いていないかもしれません',
        subtitle_text="――男性が苦手な「察する」を超える、伝え方の話",
        out_path=composed_path,
        main_size=50,
    )
    eyecatch_file = upload_image_file(composed_path, "2026-09-04_yamete_koushite_eyecatch_composed.png")
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
