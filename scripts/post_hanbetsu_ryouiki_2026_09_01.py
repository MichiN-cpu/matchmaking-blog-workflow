"""
【男女共通】同じ村を、何度も訪ねていませんか。
カテゴリ: お見合い
2026-09-01
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
    "d372d6c7-06f8-47fe-a647-6229a0b94c80",  # お見合い
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "d3951cb7-1ad4-406d-9d61-544c4e155c9d",  # 相手の見極め方
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
]
RELATED_POST_IDS = [
    "96068104-095f-4934-b2bc-db6f60b98e11",  # 笑顔ひとつで、婚活は動き出します
    "d9f205bf-f8ee-45af-894e-62b0cb82d5dc",  # 男性のここを見ています
    "6a0539de-06c2-4325-8696-ff652805bb6d",  # 傷つかない見極め方
]

TITLE = "【男女共通】同じ村を、何度も訪ねていませんか。――婚活が長引く人と、早く決まる人の「たった一つ」の違い"
EXCERPT = "婚活が長引く人と早く決まる人の違いは、実力でも運でもなく「探す範囲」の広げ方にあります。愛媛・松山市の結婚相談所の仲人が、心理学と行動科学の視点からお話しします。"
FOCUS_KEYWORD = "婚活 長引く 特徴"

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

    nodes.append(p("婚活がすいすい進む方と、なかなか進まない方。この違いって何だと思いますか。"))
    nodes.append(sp())
    nodes.append(p("実力でも、条件の良さでも、運の良さでもないんです。私が仲人としてたくさんの方を見てきて感じるのは、たった一つ、「お申し込みする相手の選び方」なんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("同じ村を、何度も訪ねていませんか"))
    nodes.append(sp())
    nodes.append(p("ロールプレイングゲームを思い浮かべてみてください。"))
    nodes.append(sp())
    nodes.append(p("主人公は、次のヒントをもらうために村人に話しかけますよね。でも、もし主人公がずっと同じ村の、同じ人にしか話しかけなかったら、ゲームは一向に進みません。"))
    nodes.append(sp())
    nodes.append(p("違う村に足を運んでみる。これまで話したことのない人に、声をかけてみる。そうやって少しずつ知らない場所を歩いていくからこそ、思わぬヒントに出会えて、物語が前に進んでいくんです。"))
    nodes.append(sp())
    # [IMG:crossroads]
    nodes.append(p("婚活も、実はまったく同じ構造をしています。「こういう条件を満たしている人がいい」という理想を、誰でも持っています。それ自体は悪いことじゃありません。だけど、その条件を一度も動かさないまま、同じ範囲の中だけをぐるぐる探し続けている方が、案外多いんです。"))
    nodes.append(sp())
    nodes.append(p("活動の幅が一点に絞られていたら、出会う結果もずっと同じ。そうしているうちに、時間だけが過ぎていくんですよね。"))
    nodes.append(sp())

    nodes.extend(section_heading("その「条件」、本当にあなたの言葉ですか"))
    nodes.append(sp())
    nodes.append(p("心理学に「確証バイアス」という考え方があります。人は一度「こうだ」と思い込むと、それを裏付ける情報ばかりを無意識に集めてしまう、という性質のことです。"))
    nodes.append(sp())
    nodes.append(p("婚活の条件も、実はこれと似ています。身長は◯cm以上、年収は◯万円以上、エリアはここまで。そう決めた瞬間から、脳はその条件に合う人だけを探すフィルターをオンにしてしまいます。合わない人は、良いところがあってもスルーしてしまうんですね。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、条件を疑うことは、わがままでも妥協でもありません。これは本当に譲れないものなのか、それとも、なんとなく世間の\"普通\"を借りてきただけなのかを、一度立ち止まって確かめてみる。それだけで、見える景色がガラッと変わることがあります。"))
    nodes.append(sp())
    nodes.append(p("不安が強い方ほど、条件を細かく決めて安心しようとする傾向があります。でもそれは性格の問題ではなくて、その方がこれまで身につけてきた、いわば\"利き手\"のような無意識の反応パターンなんです。だから責める必要はまったくありません。パターンだと分かれば、変えていくこともできますから。"))
    nodes.append(sp())
    # [IMG:cafe]
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("プロフィールを見て、条件が一つでも合わないと、それだけで「違うな」と感じてしまう。"))
    nodes.append(sp())
    nodes.append(p("お見合いした後、良いところより先に、引っかかった小さな一点を数えてしまう。"))
    nodes.append(sp())
    nodes.append(p("「もっといい人がどこかにいるはず」と思いながら、実際には同じような人にばかりお申し込みしている。"))
    nodes.append(sp())
    nodes.append(p("――どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("「探す」と「決める」、配分を間違えていませんか"))
    nodes.append(sp())
    nodes.append(p("行動科学の世界には「探索と活用のジレンマ」という考え方があります。新しい選択肢を探し続ける「探索」と、今ある選択肢を活かして決断する「活用」。このバランスをどう取るかで、結果が大きく変わるという理論です。"))
    nodes.append(sp())
    nodes.append(p("婚活が長引いてしまう方は、実はこの配分を間違えていることが多いんです。探索の幅は狭いまま、でも決断は先延ばしにし続ける。これでは、同じ村で足踏みしているのと同じなんですよね。"))
    nodes.append(sp())
    nodes.append(p("反対に、早く決まっていく方は、探索の範囲は思い切って広げつつ、良いご縁だと感じたらしっかり向き合って決める。この切り替えが自然にできています。"))
    nodes.append(sp())
    nodes.append(p("そしてもう一つ、社会学には「適格者プール」という考え方もあります。私たちが結婚相手として意識する母集団は、実は自分で無意識に狭めてしまっていることが多い、というものです。エリアを1駅広げる、年齢の幅を1〜2歳広げる、これまで避けていたタイプの方にもお会いしてみる。たったそれだけで、母集団そのものが変わります。"))
    nodes.append(sp())

    nodes.extend(section_heading("隣町に、一歩を踏み出してみませんか"))
    nodes.append(sp())
    nodes.append(p("条件を広げるというと、「妥協する」ように感じる方もいらっしゃるかもしれません。でも、私はむしろ逆だと思っています。思い込みの条件をいったん脇に置いて、本当は何を大切にしたいのかに素直に立ち返ること。それこそが、遠回りに見えて一番の近道なんです。無理に相手に合わせるのでも、我慢して条件を飲み込むのでもない。自分の本音に、素直に向き合う。私はこれを\"素直婚\"と呼んでいます。"))
    nodes.append(sp())
    # [IMG:couple]
    nodes.append(p("実際に、当初思い描いていた条件とは違うタイプの方とお見合いをして、「まさかこの人と」と思うようなご縁から、笑顔の絶えない毎日につながった方を、私は何人も見てきました。隣町には、あなたが思っている以上に、あなたに合う方がいらっしゃるかもしれません。"))
    nodes.append(sp())
    nodes.append(p("条件を1つ緩めるたびに、出会いの母集団は静かに広がっていきます。そうやって視点を変えた先には、この人となら、ありのままでいられると感じる、穏やかな毎日が待っています。"))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、お申し込み検索の条件を1つだけ、少しだけ広げてみてください。エリアを1駅、年齢を1〜2歳。それだけで大丈夫です。"))
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

    eyecatch_prompt = (base_style + ", a Japanese woman in her 30s standing at a crossroads path outdoors, "
        "looking toward distant town lights at dusk, sense of possibility and hope, gentle golden hour light")
    cafe_prompt = (base_style + ", a Japanese woman in her 30s at a cafe looking at a tablet with a relieved, "
        "clear-minded expression, soft morning daylight through a window")
    couple_prompt = (base_style + ", a Japanese man and woman in their 30s facing each other, looking at each "
        "other not at camera, meeting for the first time with warm smiles, man in neat dark suit with dress shirt, "
        "woman in soft pink elegant dress with hair down in gentle waves, bright cafe setting")

    eyecatch_path = generate_image(eyecatch_prompt, "2026-09-01_hanbetsu_ryouiki_eyecatch.png")
    cafe_path     = generate_image(cafe_prompt, "2026-09-01_hanbetsu_ryouiki_cafe.png")
    couple_path   = generate_image(couple_prompt, "2026-09-01_hanbetsu_ryouiki_couple.png")

    files = {
        "eyecatch": upload_image_file(eyecatch_path, "2026-09-01_hanbetsu_ryouiki_eyecatch.png"),
        "cafe":     upload_image_file(cafe_path, "2026-09-01_hanbetsu_ryouiki_cafe.png"),
        "couple":   upload_image_file(couple_path, "2026-09-01_hanbetsu_ryouiki_couple.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("違う村に足を運んでみる。これまで話したことのない人に、声をかけてみる。そうやって少しずつ知らない場所を歩いていくからこそ、思わぬヒントに出会えて、物語が前に進んでいくんです。", "eyecatch", "違う村に、足を運んでみませんか。"),
        ("不安が強い方ほど、条件を細かく決めて安心しようとする傾向があります。でもそれは性格の問題ではなくて、その方がこれまで身につけてきた、いわば\"利き手\"のような無意識の反応パターンなんです。だから責める必要はまったくありません。パターンだと分かれば、変えていくこともできますから。", "cafe", "条件のフィルターを、一度外してみる。"),
        ("思い込みの条件をいったん脇に置いて、本当は何を大切にしたいのかに素直に立ち返ること。それこそが、遠回りに見えて一番の近道なんです。無理に相手に合わせるのでも、我慢して条件を飲み込むのでもない。自分の本音に、素直に向き合う。私はこれを\"素直婚\"と呼んでいます。", "couple", "隣町で、思わぬご縁に出会うかもしれません。"),
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
