"""
【男女共通】困った時、あなたは「縮む」人ですか、それとも「広げる」人ですか
カテゴリ: 無料相談の前に読む
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
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む
]
TAG_IDS = [
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "1571190e-c478-41bd-89b7-aa88c9747b98",  # 決断できない
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
]
RELATED_POST_IDS = [
    "eb8a7508-a182-4140-8591-5ad52870214e",
    "f226c440-936c-4ab0-9961-fcd06d19672a",
    "29af95af-c7da-4507-bdbe-f53aa9f54309",
]

TITLE = "【男女共通】困った時、あなたは「縮む」人ですか、それとも「広げる」人ですか"
EXCERPT = "人間関係でもお金でも、困った時の反応パターンは大きく二つに分かれます。同じパターンでずっとうまくいっていないなら、婚活でも一度逆を試してみると、案外うまくいくことがあります。"
FOCUS_KEYWORD = "婚活 うまくいかない パターン"

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

    nodes.append(p("人間関係でつまずいた時、お金に困った時、なんだか調子が出ない時。そんな「困った」に直面したとき、人の反応って、実はだいたい二つのタイプに分かれるんですよね。"))
    nodes.append(sp())
    nodes.append(p("一つは、縮こまるタイプ。人との関わりを減らす、お金を使わないようにする、動くエネルギーを最小限にする。じっと守りに入る人。"))
    nodes.append(sp())
    nodes.append(p("もう一つは、広げるタイプ。誰かに会いに行く、お金や時間を使ってなんとかしようとする、動き回ってエネルギーを発散する。外に向かって動く人。"))
    nodes.append(sp())

    nodes.extend(section_heading("どちらも、行き過ぎると苦しくなる"))
    nodes.append(sp())
    nodes.append(p("縮こまりすぎると、人とのつながりが減って孤立していく。心身の健康の研究でも、社会的孤立が心臓病や早期死亡のリスクを高めることが分かっていて（ホルト=ランスタッドという研究者の有名な調査があります）、守りに入りすぎることは、実は結構コストが高いんです。"))
    nodes.append(sp())
    # [IMG:shrink]
    nodes.append(p("逆に広げすぎると、エネルギーやお金を使い果たして疲弊してしまう。次から次へと手を広げるうちに、一つ一つとちゃんと向き合えなくなってしまうんですね。"))
    nodes.append(sp())

    nodes.extend(section_heading("大体の人は、どちらかに偏っている"))
    nodes.append(sp())
    nodes.append(p("面白いのは、多くの人がこの二つのうち、どちらか一方に偏った生き方のパターンを持っている、ということなんです。困った時はいつも縮こまる。あるいは、困った時はいつも広げる。それを、人生のいろんな場面でずっと繰り返している。"))
    nodes.append(sp())
    nodes.append(p("心理学には「防衛機制」という考え方があって、人はストレスに対して自分なりの決まった対処パターンを無意識に使う、と言われています。一度うまくいったやり方を、脳は「安全な型」として記憶して、また同じ場面で自動的に繰り返そうとするんですね。それ自体は悪いことじゃないんですが、そのパターンが今の状況に合っていないのに使い続けてしまうと、ずっと同じところでつまずくことになってしまいます。"))
    nodes.append(sp())

    nodes.extend(section_heading("恋愛・婚活も、実は同じ"))
    nodes.append(sp())
    nodes.append(p("これ、恋愛や結婚、婚活の場面でもまったく同じことが起きます。"))
    nodes.append(sp())
    nodes.append(p("たとえば、広げるタイプの人。一人の人とうまくいかないと感じた瞬間、「この人とは合わなかった」と、すぐに次のパーティーやマッチングアプリ、次の出会いへと手を広げてしまう。動くこと自体は悪くないんですが、いつもこのパターンばかりだと、実は一人ひとりとちゃんと向き合う前に離れてしまっていることに、本人も気づいていなかったりします。"))
    nodes.append(sp())
    # [IMG:onepersonn]
    nodes.append(p("そんな時こそ、あえて「縮こまる」を試してみる。次の出会いに手を伸ばす代わりに、少し立ち止まって自分の内側を見つめてみるんです。本当は何を求めているのか。逆に、自分は何を避けようとしているのか。そして、目の前の一人の人と、たくさん話をしてみる。理解しようとしてみる。理解してもらおうとしてみる。それだけで、今まで見えていなかったものが、案外見えてくることがあります。"))
    nodes.append(sp())
    nodes.append(p("逆に、縮こまりがちな人であれば、少し「広げる」を試してみる。一人で抱え込まずに、誰かに話してみる、新しい場に飛び込んでみる。今までとは逆の動きをしてみることで、これまで見えなかった景色に出会えることがあるんです。"))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("大切なのは、「縮こまる」も「広げる」も、どちらが正しいということじゃなくて、今の自分にはどちらが必要なのか、を選び直せるということ。同じパターンでずっとうまくいっていないのなら、一度、逆をやってみる。それだけで、婚活の景色が変わることは、案外あるものです。"))
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

    eyecatch_prompt = (base_style + ", a Japanese man and woman in their 30s standing at a fork in a quiet path "
        "outdoors, one path narrow and shaded, one path open and sunlit, symbolic of choosing a different direction, "
        "soft natural daylight, wide shot")
    shrink_prompt = (base_style + ", a Japanese woman in her 30s sitting alone on a chair with arms folded close to "
        "her body, withdrawn posture, dim soft indoor light, quiet contemplative mood")
    onperson_prompt = (base_style + ", a Japanese man and woman in their 30s sitting closely at a small table, deeply "
        "engaged in a calm one on one conversation, warm gentle expressions, soft window light, intimate cafe setting")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-09-04_chijikomaru_hirogeru_eyecatch.png")
    shrink_path = generate_image(shrink_prompt, "2026-09-04_chijikomaru_hirogeru_shrink.png")
    onperson_path = generate_image(onperson_prompt, "2026-09-04_chijikomaru_hirogeru_oneperson.png")

    files = {
        "shrink": upload_image_file(shrink_path, "2026-09-04_chijikomaru_hirogeru_shrink.png"),
        "oneperson": upload_image_file(onperson_path, "2026-09-04_chijikomaru_hirogeru_oneperson.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("縮こまりすぎると、人とのつながりが減って孤立していく。心身の健康の研究でも、社会的孤立が心臓病や早期死亡のリスクを高めることが分かっていて（ホルト=ランスタッドという研究者の有名な調査があります）、守りに入りすぎることは、実は結構コストが高いんです。", "shrink", "縮こまりすぎることにも、実はコストがあります。"),
        ("たとえば、広げるタイプの人。一人の人とうまくいかないと感じた瞬間、「この人とは合わなかった」と、すぐに次のパーティーやマッチングアプリ、次の出会いへと手を広げてしまう。動くこと自体は悪くないんですが、いつもこのパターンばかりだと、実は一人ひとりとちゃんと向き合う前に離れてしまっていることに、本人も気づいていなかったりします。", "oneperson", "一人の人と、たくさん話をしてみる。それだけで見えてくるものがあります。"),
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

    composed_path = os.path.join(IMAGES_DIR, "2026-09-04_chijikomaru_hirogeru_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=eyecatch_path,
        main_html='困った時、あなたは<br><span class="accent">「縮む」人</span>ですか、<br>それとも<span class="accent">「広げる」人</span>ですか',
        subtitle_text="――うまくいかない時こそ、逆のパターンを試してみる話",
        out_path=composed_path,
        main_size=46,
    )
    eyecatch_file = upload_image_file(composed_path, "2026-09-04_chijikomaru_hirogeru_eyecatch_composed.png")
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
