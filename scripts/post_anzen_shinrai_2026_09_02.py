"""
【男女共通】その「素敵な人」、写真の通りだと思いますか？
カテゴリ: 結婚相談所の始め方（IBJ・流れ・費用）
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
    "0122d61b-14c6-42d9-a950-d4b527ea39d1",  # 結婚相談所の始め方
]
TAG_IDS = [
    "61acc4f3-6c16-4653-995b-dd6d9136c1d3",  # IBJ
    "ce76d0c1-1fa1-4898-954b-2903a34dbcd4",  # マッチングアプリ
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
    "a8fd177f-b3ba-4a57-9f81-c26ba1ec0488",  # 婚活相談
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
]
RELATED_POST_IDS = [
    "935c10a3-40fd-4a54-92af-68cc5596df81",
    "bcfd8e8d-e405-4d6f-80e5-769e88851536",
    "3f84d312-9c4f-40b7-8476-963876091b38",
]

TITLE = "【男女共通】その「素敵な人」、写真の通りだと思いますか？――婚活で、心と一緒に守ってほしいもの"
EXCERPT = "警察庁の統計では、SNS型ロマンス詐欺の被害額は2024年に約397億円、前年比2.2倍に増えています。婚活で心を開くことと、身を守ることは両立できます。公的データをもとにお伝えします。"
FOCUS_KEYWORD = "婚活 詐欺 安全 結婚相談所"

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

    nodes.append(p("婚活の話をするとき、私はいつも「心を開くこと」の大切さをお伝えしています。でも今日は、その前提として知っておいてほしい、少し厳しい数字の話をさせてください。"))
    nodes.append(sp())

    nodes.extend(section_heading("「素敵だな」と思った瞬間、警戒心は下がります"))
    nodes.append(sp())
    nodes.append(p("心理学に「ハロー効果」という考え方があります。見た目や第一印象が良いと、その人の他の面まで無条件に良く見えてしまうという心の働きのことです。プロフィール写真が素敵だと、その人の言葉も人柄も、実際以上に信頼してしまいやすくなるんですね。"))
    nodes.append(sp())
    nodes.append(p("警察庁が2025年2月に発表した統計によると、SNSやマッチングアプリをきっかけにした「ロマンス詐欺」の被害額は、2024年だけで約397億円。前年の2.2倍という急激な増え方をしています。"))
    nodes.append(sp())
    # [IMG:screen]
    nodes.append(p("これは特別な人だけが引っかかる話ではありません。「素敵だな」と感じた瞬間に警戒心が下がるのは、人間の心の自然な仕組みだからです。騙されやすい性格だからではなく、誰にでも起こりうる反応パターンだということを、まず知っておいてほしいんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("こんなこと、心当たりはありませんか"))
    nodes.append(sp())
    nodes.append(p("会ったことのない相手なのに、もう長い付き合いのように感じて安心してしまっている。"))
    nodes.append(sp())
    nodes.append(p("お金や個人的な事情の相談を、まだ数回しかやり取りしていない相手からされたことがある。"))
    nodes.append(sp())
    nodes.append(p("「この人は特別だから大丈夫」と、自分に言い聞かせるように思ってしまうことがある。"))
    nodes.append(sp())
    nodes.append(p("――どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("「確認された安心」という選択肢"))
    nodes.append(sp())
    nodes.append(p("東京都消費生活総合センターの相談データでは、婚活・マッチング関連のトラブルによる平均被害額は約185万円（2023年度）、相談者の9割が20〜30代にのぼります。金銭的な被害だけでなく、人を信じる気持ちそのものが傷ついてしまうことも少なくありません。"))
    nodes.append(sp())
    nodes.append(p("結婚相談所での婚活は、この部分の設計が根本的に違います。IBJに加盟する結婚相談所では、入会時に独身証明書をはじめとする各種証明書の提出が必須です。年齢や身分を偽ったまま活動を続けることが、そもそも構造としてできない仕組みになっています。"))
    nodes.append(sp())
    # [IMG:document]
    nodes.append(p("コミュニケーション学では、信頼は「言葉の内容」よりも「確認できる事実の積み重ね」によって築かれると言われています。素敵な言葉をかけられることより、証明書という動かない事実があることのほうが、実は安心につながるんですね。"))
    nodes.append(sp())

    nodes.extend(section_heading("疑うことは、冷たいことじゃありません"))
    nodes.append(sp())
    nodes.append(p("「せっかく良い出会いなのに、疑うなんて申し訳ない」——そう感じてしまう方もいらっしゃいます。でも、自分を守る心構えを持つことと、相手を信じて心を開くことは、両立できるものです。"))
    nodes.append(sp())
    nodes.append(p('素直に心を開きながらも、素直に自分の身も心も守る。そのどちらも我慢しなくていい婚活のかたちを、私は"素直婚"と呼んでいます。仲人が間に入るからこそ、安心してその両方を大事にできるんです。'))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("もし今、気になっている相手がいるなら、「この人について、自分が確認できている事実は何だろう」と、一つだけ書き出してみてください。"))
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

    eyecatch_prompt = (base_style + ", a Japanese woman in her 30s looking at a smartphone screen with a "
        "cautious thoughtful expression, soft evening light indoors, contemplative mood")
    screen_prompt = (base_style + ", close up of a smartphone screen glowing in a dim room, hands holding it, "
        "blurred chat bubble shapes visible but no readable text, moody dim lighting")
    document_prompt = (base_style + ", close up of hands neatly placing official documents and a pen on a "
        "clean desk, soft natural window light, calm orderly professional atmosphere, no readable text on documents")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-09-02_anzen_shinrai_eyecatch.png")
    screen_path = generate_image(screen_prompt, "2026-09-02_anzen_shinrai_screen.png")
    document_path = generate_image(document_prompt, "2026-09-02_anzen_shinrai_document.png")

    files = {
        "screen": upload_image_file(screen_path, "2026-09-02_anzen_shinrai_screen.png"),
        "document": upload_image_file(document_path, "2026-09-02_anzen_shinrai_document.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("警察庁が2025年2月に発表した統計によると、SNSやマッチングアプリをきっかけにした「ロマンス詐欺」の被害額は、2024年だけで約397億円。前年の2.2倍という急激な増え方をしています。", "screen", "画面の向こうの「素敵な人」、実在を確認できていますか。"),
        ("結婚相談所での婚活は、この部分の設計が根本的に違います。IBJに加盟する結婚相談所では、入会時に独身証明書をはじめとする各種証明書の提出が必須です。年齢や身分を偽ったまま活動を続けることが、そもそも構造としてできない仕組みになっています。", "document", "「確認された事実」が、安心の土台になります。"),
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

    composed_path = os.path.join(IMAGES_DIR, "2026-09-02_anzen_shinrai_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=eyecatch_path,
        main_html='その「素敵な人」、<br><span class="accent">写真の通り</span>だと<br>思いますか？',
        subtitle_text="――婚活で、心と一緒に守ってほしいもの",
        out_path=composed_path,
        main_size=52,
    )
    eyecatch_file = upload_image_file(composed_path, "2026-09-02_anzen_shinrai_eyecatch_composed.png")
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
