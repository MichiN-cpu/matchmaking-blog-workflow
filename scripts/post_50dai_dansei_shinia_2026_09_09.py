"""
【男性向け】"なんとなく気が重くて"後回しにしてきた50代の婚活、実は今、風向きが変わっています。
カテゴリ: シニアの婚活
2026-09-09
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
    "a65acc05-b781-4ec9-95d7-66c9daefc19f",  # シニアの婚活
]
TAG_IDS = [
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "3c983f3c-50b7-4193-9d37-64a066c45d1c",  # ５０代
    "3a8d9ef3-9a26-4099-8ac8-546957aa1043",  # シニア
    "a2ccc420-e138-466f-84b6-d196571108c9",  # 成婚白書
    "8e7391b9-306a-4007-9297-910418163203",  # データ分析
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
]
RELATED_POST_IDS = [
    "db72c191-573d-44af-8b90-8a2b208a15f3",  # 50代以上の入会者が約2倍に増加！（IBJデータ解説）
    "cfb9a391-d16f-41a0-8050-5ceffaf93740",  # シニア世代の婚活で、本当に考えてほしいたった一つのこと
    "db6f3405-8ac9-4f76-a575-c8579ea63941",  # 【男性向け】アラカン婚活男性への、正直な話
]

TITLE = "【男性向け】\"なんとなく気が重くて\"後回しにしてきた50代の婚活、実は今、風向きが変わっています。――データが示す「シニア婚」急増の理由"
EXCERPT = "「もう歳だから」と婚活を後回しにしていませんか。IBJ全体のデータでは、50代以上の成婚数がこの8年で約4倍に急増しています。公認心理師・仲人の中嶋美知が、今50代男性の婚活に追い風が吹いている理由と、動けない本当の原因を解説します。"
FOCUS_KEYWORD = "50代 婚活 男性 愛媛"
SOURCE_URL = "https://www.ibjapan.jp/mirai-lab/seikon-hakusho/871/"

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

def p_with_link(prefix, link_text, suffix, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": prefix, "decorations": []}},
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": link_text, "decorations": [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]}},
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": suffix, "decorations": []}},
    ], "paragraphData": {}}

def heading(text):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": 2}}

def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {"lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"}}

def section_heading(text):
    return [sp(), divider_node(), sp(), heading(text)]

def link_node_centered(text, url, underline=False):
    decos = [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]
    if underline:
        decos.append({"type": "UNDERLINE"})
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": decos}}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}

def cta_nodes():
    return [
        link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"),
        link_node_centered("https://www.asunaru.jp/soudan", "https://www.asunaru.jp/soudan", underline=True),
    ]

def real_photo_node():
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {
                "image": {"src": {"url": REAL_PHOTO_URL}},
                "containerData": {"width": {"size": "SMALL"}, "alignment": "CENTER"},
            }}

def image_node(file_obj, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {
                "image": {"src": {"url": file_obj["url"]}}, "caption": caption,
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

    nodes.append(p("「もう50代だし、今さら婚活なんて」"))
    nodes.append(sp())
    nodes.append(p("そう思って、心のどこかにフタをしてはいないでしょうか。誘われても気が重くて、婚活サイトを開いても指が止まる。それ、わりとよくあることなんです。"))
    nodes.append(sp())
    nodes.append(p("でも実はいま、50代以上の結婚市場で静かに、でも確実に大きな変化が起きています。"))
    nodes.append(sp())

    nodes.extend(section_heading("8年で約4倍。「シニア婚」は、もう特別な話じゃない"))
    nodes.append(sp())
    nodes.append(p_with_link("IBJ（日本結婚相談所連盟）が公開している", "成婚白書のデータ", "によると、50代以上の成婚数は2017年の348名から、2025年には1,389名まで増えています。約4倍です。しかも2023年以降は毎年右肩上がりで、一時的なブームではなく、はっきりとした流れになっていることがわかります。", SOURCE_URL))
    nodes.append(sp())
    nodes.append(p("さらに興味深いのは、男女それぞれの伸び方です。男性の成婚数が2017年の259名から869名（約3.4倍）に増えたのに対して、女性は89名から520名（約5.8倍）。女性の伸びのほうが、男性より1.7倍近く速いペースで増えているんです。"))
    nodes.append(sp())
    # [IMG:data]
    nodes.append(p("これが何を意味するかというと、50代で「本気で結婚したい」と考えている女性は、この数年でぐっと増えているのに、その気持ちに応えて動く男性の数が、同じスピードでは増えていないということなんですよね。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、なんです。今、腰を上げて動いた50代男性は、以前よりずっと出会いのチャンスに恵まれやすい環境にいます。"))
    nodes.append(sp())

    nodes.extend(section_heading("なぜ「今さら」と思ってしまうのか"))
    nodes.append(sp())
    nodes.append(p("ここで一つ、知っておいてほしいことがあります。「もう歳だから」「今さら恥ずかしい」という気持ちは、あなたの性格でも、あなたの本当の望みでもありません。"))
    nodes.append(sp())
    nodes.append(p("人は誰でも、右利きの人が意識せず右手を使うように、無意識に決まった反応を繰り返すパターンを持っています。婚活に対する「気が重い」も同じで、長年かけて身についた\"慣れた反応\"にすぎないんです。性格だから仕方ないのではなく、パターンだから、外すこともできる。そう考えると、少し肩の力が抜けませんか。"))
    nodes.append(sp())
    nodes.append(p("社会学者ゴッフマンは、人は社会の中で「こう見られたい自分」を演じながら生きていると説明しました。50代になると「結婚相談所に登録する自分」を想像するだけで、周囲にどう見られるかが気になってしまう。けれど実際のところ、50代の婚活はもう珍しいものではなく、堂々と選べる選択肢になっています。"))
    nodes.append(sp())

    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("婚活のことを考えると、なんとなく気分が沈む。「どうせ自分には無理だろう」と、試す前から決めつけている。家族や友人に婚活の話をするのが、少し気恥ずかしい。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("「こだわらない」人ほど、成婚に近づいている"))
    nodes.append(sp())
    nodes.append(p("先ほどのIBJのデータには、もう一つ見逃せない数字がありました。50代以上の会員のうち、子どもについて「希望しない」男性は、「希望する」男性に比べて約2.0倍成婚しやすく、「こだわらない」男性でも約1.7倍という結果が出ています。"))
    nodes.append(sp())
    nodes.append(p("これは行動科学でいう認知的柔軟性と重なる話です。条件を厳密に絞り込むほど選択肢は狭くなり、迷いも増えます。逆に「絶対にこうでなければ」という思い込みを一つ手放すだけで、目の前に現れる出会いの数も、進展しやすさも変わってくるんですよね。"))
    nodes.append(sp())
    nodes.append(p("厳しい条件を持つことが悪いわけではありません。ただ、50代からの婚活でうまくいく方は、若い頃の\"理想の結婚像\"をそのまま引きずるのではなく、今の自分に合った形へ、少しずつアップデートできる方が多い印象です。"))
    nodes.append(sp())

    nodes.extend(section_heading("動けない本当の理由は、\"孤独\"への慣れかもしれません"))
    nodes.append(sp())
    nodes.append(p("心身の健康の研究では、社会的なつながりの少なさが、喫煙や肥満と同じくらい健康リスクに影響するという報告があります（ホルト＝ランスタッドらの研究）。一人の時間に慣れてしまうと、それが「快適」だと錯覚しやすくなるのですが、実際には心と体にじわじわ負荷がかかっていることも少なくありません。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、まず動いてみることに意味があります。行動レベルでできるのは、無料相談で今の気持ちをそのまま話してみること。パターンを解除するレベルでは、「今さら」という思考グセそのものに気づき、それが自分の意志ではなく慣れた反応だったと理解すること。この二つがそろうと、婚活は驚くほど軽く動き出します。"))
    nodes.append(sp())
    nodes.append(p("あすなる愛媛がお勧めしたいのは、無理に自分を作らず、ありのままの自分で選び選ばれる\"素直婚\"という考え方です。50代からの結婚は、若い頃のような駆け引きではなく、お互いが素直に安心できる相手と出会うことが、何より大切になってきます。"))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、婚活のことを考えて気が重くなったら、「これは性格じゃなくて、慣れたパターンなだけ」と、心の中でひとこと言ってみてください。それだけで十分です。"))
    nodes.append(sp())

    nodes.extend(section_heading("想像してみてください"))
    nodes.append(sp())
    nodes.append(p("仕事から帰ってきて、玄関で「おかえり」と言ってくれる人がいる夜。今日あった小さな出来事を、誰かに聞いてもらえる安心感。50代からの結婚は、若い頃に思い描いていた形とは違うかもしれませんが、静かで確かな喜びに満ちています。"))
    nodes.append(sp())
    # [IMG:hope]
    nodes.append(p("データが教えてくれているのは、今まさにその扉が、以前より大きく開いているということ。あとは、あなたが一歩踏み出すだけなんです。"))
    nodes.append(sp())

    nodes.append(real_photo_node())
    nodes.append(sp())
    nodes.extend(cta_nodes())
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
                  "clean bright modern atmosphere, no text, no warm yellowish tint, "
                  "warm genuine smile, eyes bright with hope, NOT downcast, NOT teary, NOT vacant, "
                  "clean bright natural daylight, crisp clean colors, vivid but neutral tones, NOT pale, NOT gloomy, NOT sepia")

    eyecatch_prompt = (base_style + ", a Japanese man in his 50s sitting by a bright window with a cup of coffee, "
        "smart casual outfit, calm confident posture, soft natural daylight, wide shot")
    data_prompt = (base_style + ", a Japanese man in his 50s looking at a tablet with a calm curious expression, "
        "slight smile, bright modern living room, soft window light")
    hope_prompt = (base_style + ", a Japanese man and woman in their 50s facing each other, looking at each other "
        "not at camera, having a warm conversation over dinner at home, both smiling gently, cozy dining table")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-09-09_50dai_dansei_eyecatch.png")
    data_path = generate_image(data_prompt, "2026-09-09_50dai_dansei_data.png")
    hope_path = generate_image(hope_prompt, "2026-09-09_50dai_dansei_hope.png")

    files = {
        "data": upload_image_file(data_path, "2026-09-09_50dai_dansei_data.png"),
        "hope": upload_image_file(hope_path, "2026-09-09_50dai_dansei_hope.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("これが何を意味するかというと、50代で「本気で結婚したい」と考えている女性は、この数年でぐっと増えているのに、その気持ちに応えて動く男性の数が、同じスピードでは増えていないということなんですよね。", "data", "50代女性の「本気度」に、動く男性の数が追いついていません。"),
        ("データが教えてくれているのは、今まさにその扉が、以前より大きく開いているということ。あとは、あなたが一歩踏み出すだけなんです。", "hope", "静かで確かな喜びに満ちた、二人の時間。"),
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

    composed_path = os.path.join(IMAGES_DIR, "2026-09-09_50dai_dansei_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=eyecatch_path,
        main_html='"なんとなく気が重くて"<br>後回しにしてきた<br><span class="accent">50代の婚活</span>',
        subtitle_text="――データが示す「シニア婚」急増の理由",
        out_path=composed_path,
        main_size=44,
    )
    eyecatch_file = upload_image_file(composed_path, "2026-09-09_50dai_dansei_eyecatch_composed.png")
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
