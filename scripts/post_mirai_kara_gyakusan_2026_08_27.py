"""
【男女共通】未来の夫婦は、もう"今のあなた"の中にいます。
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
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
]
RELATED_POST_IDS = [
    "29af95af-c7da-4507-bdbe-f53aa9f54309",  # 迷ったときほど、答えは頭の外にある。
    "78d9e1c5-9567-4c4c-a7d8-9b318a131ee9",  # 「どこ行こうか」から、ふたりは始まる。
    "fc45007d-dda4-487e-a7e4-af38ac063665",  # 言葉にしなくていい。触れるだけで、消えていく。
]

TITLE = "未来の夫婦は、もう\"今のあなた\"の中にいます。"
EXCERPT = "婚活を始めるとき、多くの人は「今」から「未来」へ一歩ずつ進んでいくイメージを持ちます。でも実は、その逆——すでに叶った未来から今を見つめる方法があります。NLPトレーナーでもある中嶋美知が、婚活を軽くする\"逆算\"の考え方をお伝えします。"
FOCUS_KEYWORD = "婚活 未来 NLP 逆算 会話"

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

    nodes.append(p("婚活を始めるとき、多くの方が「今」という場所から、少しずつ「未来」に向かって歩みを進めていくイメージを持っていらっしゃいます。それはそれで自然なことなんですが、実はこのイメージのまま進むと、なかなかうまくいかない方も多いんです。なぜなら、一つひとつハードルを超えていかなければならない、というイメージになってしまうからなんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("未来から、今を作るという発想"))
    nodes.append(sp())
    nodes.append(p("私は、願望実現のNLPトレーナーでもあります。NLPでは、未来から歴史を作るという考え方をします。もうそうなった未来から逆算して、今の自分を設定していくんです。"))
    nodes.append(sp())
    nodes.append(p("ぜひ、あなたが望む結婚をしている、その未来にまず行ってみてください。そして、その未来から振り返って、どうやってそこにたどり着いたのか。もし大きなターニングポイントが3つあったとしたら、それはどんな出来事だったのか。もう既にそうなっている未来の自分として、「そういえば、ここに来るまでに、こんなことがあってね。その前には、こんなこともあってね」と、語ってみてください。"))
    nodes.append(sp())

    nodes.extend(section_heading("夫婦の会話は、特別なことばかりじゃありません"))
    nodes.append(sp())
    nodes.append(p("面白いのは、未来のご夫婦って、実は毎日そんな特別な話ばかりしているわけじゃないということです。日常ですから、夫婦ですから、特別なイベントは、多くても3つくらいで十分なんです。それ以外の、お見合いから今日までの日々の中身は、本当に何でもない、たわいもない話がほとんどなんですよね。"))
    nodes.append(sp())
    nodes.append(p("仕事に行って、帰ってきて、電話したり、LINEを送ったり。その内容も、「今日、職場でこんな人がいてね」「今日、こんなもの食べたよ」「部屋の掃除をしたよ」といった、些細なこと。テレビの話、YouTubeの話、ニュースの話。「そろそろ車を買い替えようかな」「庭の木が大きくなってきたから切りたいけど、なんだか面倒だな」——そんな会話です。"))
    nodes.append(sp())
    # [IMG:kitchen]
    nodes.append(p("社会学者のゴッフマンは、こうした日常のちょっとしたやりとりが、実は人と人との関係を支える大切な土台になっていると指摘しています。特別な出来事よりも、何でもない会話の積み重ねの方が、実は関係の安心感をつくっているんですね。"))
    nodes.append(sp())

    nodes.extend(section_heading("未来まで、待たなくていいんです"))
    nodes.append(sp())
    nodes.append(p("ということは、未来がそうなっているとしたら、今から、その雰囲気で接してみればいいということなんです。未来のふたりと同じ、同じエネルギー、同じ安心感、同じくつろぎ、同じ信頼。それを、今のお相手との関わりの中で試してみてください。"))
    nodes.append(sp())
    nodes.append(p("「未来に向かって、一段ずつハードルを乗り越えていかなきゃ」と思ってしまうのも、実は右利きの人が無意識に右手を使ってしまうのと同じで、多くの人が気づかないうちに選んでいる考え方のクセなんです。性格の問題ではなく、単なる反応パターン。だから、変えることもできます。"))
    nodes.append(sp())
    nodes.append(p("心理学の研究でも、「未来の自分」をどれだけ身近に、現実味を持って感じられるかが、今の行動の選び方に大きく影響することがわかっています。未来の自分を、遠い他人のように感じている人ほど、今の一歩をためらいやすい。逆に、未来の自分をすでに親しい存在として感じられると、今の選択が自然と軽くなっていくんです。"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("お見合いの前に、何か気の利いた話題を用意しなきゃと身構えてしまう。"))
    nodes.append(sp())
    nodes.append(p("何でもない会話をしていると、「これでいいのかな」と物足りなく感じてしまう。"))
    nodes.append(sp())
    nodes.append(p("婚活そのものが、乗り越えるべき課題の連続のように見えてしまう。"))
    nodes.append(sp())
    nodes.append(p("――どれか一つでも「あるかも」と思った方は、このあとのお話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("もし、それがあまりにも難しい相手なら"))
    nodes.append(sp())
    nodes.append(p("もし、未来のふたりと同じ雰囲気で接することが、あまりにも難しい相手だとしたら、それは一つの大切なサインです。無理に合わせようとせず、少し立ち止まって考えてみるポイントになります。"))
    nodes.append(sp())
    # [IMG:window]
    nodes.append(p("逆に、どんな雰囲気で、どんな話で、どんなペースで、どんな会話のキャッチボールをしていたら、自分は無理せずエネルギーをチャージできるのか。家庭に帰りたくなるのか。それを、まず自分の中で未来設定して、ありありと感情まで感じて浸ってみてください。そうすると不思議なのですが、その自分として生きることに無理のないお相手は、自然と出会いやすくなっていくんですよ、不思議とこれが！"))
    nodes.append(sp())

    nodes.extend(section_heading("じんわり、でも確かに変わっていく"))
    nodes.append(sp())
    nodes.append(p("特別な演出をしようとせず、素直に「今日こんなことがあってね」と話し合える。そんな何でもない毎日を、ふたりで積み重ねていく。それが私のお勧めしたい\"素直婚\"の日常です。"))
    nodes.append(sp())
    nodes.append(p("仕事で疲れて帰った夜、玄関で顔を合わせて、今日あったちょっとしたことを話す。それだけで、なんだか安心する。そんな未来の暮らしは、実はもう、今のあなたの中に眠っているんですよね。"))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今週、数分だけでいいので、望む未来の自分になったつもりで、ターニングポイントを一つだけ想像して書き出してみてください。よくわからなければ、無料相談で私に聞かせてくださいね。一緒に未来から逆算してみましょう。"))
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
                  "real-world setting, professional lifestyle photography style, shallow depth of field, "
                  "clean bright modern atmosphere, no text, no warm yellowish tint")

    eyecatch_prompt = (base_style + ", a Japanese couple in their 30s sitting together on a sofa at home "
        "in the evening, relaxed comfortable posture, gentle warm expressions, casual homewear, "
        "clean bright modern living room")
    kitchen_prompt = (base_style + ", a Japanese couple in their 30s in a kitchen in the evening, casually "
        "chatting while one washes dishes and the other leans against the counter holding a phone, "
        "relaxed everyday atmosphere")
    window_prompt = (base_style + ", a Japanese person in their 30s sitting by a window with a notebook, "
        "looking outward with a calm hopeful expression as if imagining the future, soft daylight")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-08-27_mirai_kara_gyakusan_eyecatch.png")
    kitchen_path  = generate_image(kitchen_prompt, "2026-08-27_mirai_kara_gyakusan_kitchen.png")
    window_path   = generate_image(window_prompt, "2026-08-27_mirai_kara_gyakusan_window.png")

    files = {
        "eyecatch": upload_image_file(eyecatch_path, "2026-08-27_mirai_kara_gyakusan_eyecatch.png"),
        "kitchen":  upload_image_file(kitchen_path, "2026-08-27_mirai_kara_gyakusan_kitchen.png"),
        "window":   upload_image_file(window_path, "2026-08-27_mirai_kara_gyakusan_window.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("テレビの話、YouTubeの話、ニュースの話。「そろそろ車を買い替えようかな」「庭の木が大きくなってきたから切りたいけど、なんだか面倒だな」——そんな会話です。", "kitchen", "特別ではない会話が、関係を支えています。"),
        ("もし、未来のふたりと同じ雰囲気で接することが、あまりにも難しい相手だとしたら、それは一つの大切なサインです。無理に合わせようとせず、少し立ち止まって考えてみるポイントになります。", "window", "未来から、今を見つめてみる。"),
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
