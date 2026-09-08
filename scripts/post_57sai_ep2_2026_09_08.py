"""
【女性向け】57歳仲人、婚活始めました。（第2話：初めてのお見合い）
カテゴリ: 自己紹介 / 再婚の婚活
2026-09-08
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "133a60f7-a603-431d-8ca9-8ec82c2294c5",  # 自己紹介
    "bc14935b-78aa-4ee4-85bf-35ac04874fb3",  # 再婚の婚活
]
TAG_IDS = [
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "25417c41-e15f-4447-8e02-1e9b7ff48aec",  # 受け身
    "3c983f3c-50b7-4193-9d37-64a066c45d1c",  # ５０代
    "bc47248a-e548-43b9-bd31-8da1d1d4e189",  # 再婚
    "d454c1ff-e2b4-4d07-84dc-626693e74f61",  # 離婚
    "27815c19-e4df-4f86-9949-70c119f752d2",  # 書籍
    "d372d6c7-06f8-47fe-a647-6229a0b94c80",  # お見合い
]
RELATED_POST_IDS = [
    "771006c5-5963-457e-b7c9-cdf514e0a0ac",  # 第1話
    "40fce56b-d4f7-4f8b-969c-0220955813f9",  # こんにちは、あすなる愛媛の結婚相談所です【自己紹介その①】
    "7b7d916b-7cbf-41a2-9524-49736ac65699",  # 結婚生活破綻→離婚の背景【自己紹介その②】
]

TITLE = "【女性向け】57歳仲人、婚活始めました。（第2話）"
EXCERPT = "57歳と2ヶ月、初めてのお見合い。遠距離だったのでZoomでした。条件を聞き合う中で、ふと浮かんだ「私は我慢するの？」という問い。仲人自身の婚活実話、第2話。"
FOCUS_KEYWORD = "57歳 婚活 お見合い"
EP1_URL = "https://www.asunaru.jp/post/【女性向け】57歳仲人、婚活始めました。"
REAL_PHOTO_URL = "https://static.wixstatic.com/media/a4e52d_cf3f0f8fec8d40e4ac0e0bb6dfc4771d~mv2.png"

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "drafts", "images")

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
    print("SEOメタ・フォーカスキーワード設定:", "完了" if rp.ok else f"失敗 {rp.status_code} {rp.text[:300]}")

def build_nodes():
    nodes = []
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())
    nodes.append(p_with_link("", "前回", "に続いて、私自身の婚活の話、第2話です。57歳と2ヶ月、初めてのお見合いをしました。当時の日記を読み返しながら、書いていきますね。", EP1_URL))
    nodes.append(sp())

    body = [
        "仲人さんから紹介していただいた方でした。",
        "遠距離だったので、Zoomでのお見合いです。",
        "婚活で初めて会う人と話すとき、目の前にいるのは一人の人なんですよね。",
        "なのに、会話の中には、たくさんの「条件」が出てきます。",
        "お仕事は何をしているのか。",
        "勤務時間はどうなっているのか。",
        "どこに住んでいるのか。",
        "家は持ち家なのか。",
        "定年は何歳なのか。",
        "お酒は飲むのか。",
        "ギャンブルはするのか。",
        "休みの日は何をしているのか。",
        "質問だけを並べれば、まるで面接のようにも見えます。",
        "けれど、私が知りたかったのは、数字や肩書だけではありませんでした。",
        "その人の生活の中へ私が入ったら、どんな一日になるんだろう。",
        "朝は何時に起きるのか。",
        "食事は一緒に取れるのか。",
        "仕事から帰ってきたあと、どんなふうに過ごすのか。",
        "休みの日に出かけるのか、それとも、それぞれが好きなことをして過ごすのか。",
        "私は、条件の向こう側にある暮らしを、見ようとしていたんです。",
        "__IMG_MEMO__",
        "お相手は交替勤務で働いている方でした。",
        "日記には、朝から夜まで、夜から朝までという勤務時間が書かれています。",
        "家のことも、かなり具体的にメモしていました。",
        "3LDK。対面式の台所。和室や洋室。",
        "定年やローンのこと。",
        "定年後には日本各地を旅行したい、という話もありました。",
        "趣味として、御朱印集めやYouTube、音楽のことも書いています。",
        "こうして読み返すと、私はずいぶん細かく記録しているんですよね。",
        "その細かさは、条件のよい人かどうかを採点したかったからではないと思います。",
        "私はきっと、「この人と暮らす私」を、一生懸命に想像しようとしていたんです。",
        "話し方については、「ゆっくり」「わかりやすい」と書いていました。",
        "人柄は穏やかで、まじめそうだとも感じていました。",
        "プロフィールの文章だけでは分からなかったものが、声の速さや、言葉の選び方や、間の取り方から、少しずつ伝わってきたんです。",
        "だからといって、すぐに「この人だ」と思えたわけではありません。",
        "家のこと。旅行のこと。将来のこと。",
        "相手が思い描いている暮らしが見えてくるほど、別の問いが生まれてきました。",
        "そこに、私の望む暮らしはあるのだろうか。",
    ]
    for line in body:
        if line == "__IMG_MEMO__":
            continue
        nodes.append(p(line))
        nodes.append(sp())

    nodes.append(sp())

    body2 = [
        "翌日、電話で話しました。",
        "日記には、お金だけではなく、一緒に生活していくこと、家や庭のことが書かれています。",
        "そして、次のような意味の言葉を残していました。",
        "結婚は、一人で完成させた理想へ、もう一人を当てはめることではない。",
        "二人の希望が最初からぴったり同じことなど、たぶんない。",
        "暮らしたい場所も、家の形も、お金の使い方も、休日の過ごし方も違う。",
        "だから、話して、確かめて、少しずつすり合わせていく。",
        "頭では、その通りだと思うんです。",
        "けれど、「すり合わせる」という言葉を考えているうちに、私の中から別の声が出てきました。",
        "私は我慢するの？",
        "__IMG_TOI__",
        "相手に合わせることと、自分を抑えることは、同じではありません。",
        "相手を思いやることと、自分の希望を諦めることも、同じではありません。",
        "けれど私は、その境目が分からなくなることがあったんです。",
        "相手に喜んでもらいたい。",
        "関係を壊したくない。",
        "面倒な人だと思われたくない。",
        "そんな気持ちが出てくると、「私はどうしたいのか」よりも、「相手は何を望んでいるのか」を先に考えてしまう。",
        "それは優しさなのでしょうか。",
        "それとも、嫌われないための我慢なのでしょうか。",
        "この日の私は、まだ答えを持っていませんでした。",
        "コミュニケーション学の世界に、「アサーティブネス」という考え方があります。相手を尊重しながら、自分の気持ちや希望も同じように大切に伝える、というものです。「相手に合わせる」か「自分を通す」かの二択ではなく、その間に、ちゃんと居場所がある。",
        "でも、知識として知っていることと、目の前の人を前にそれができることは、別なんですよね。",
        "私自身、心理カウンセラーとしてこの考え方を人にお伝えする立場でありながら、いざ自分の婚活となると、うまくできませんでした。",
        "ただ、「私は我慢するの？」と書けたことには、意味があったと思います。",
        "婚活を始めた私は、相手に選んでもらうためだけに動いていたのではありませんでした。",
        "相手との会話を通して、これまで言葉にしてこなかった自分の望みを、探し始めていたんです。",
        "どんな家に住むか。",
        "どこへ旅行するか。",
        "何歳まで働くか。",
        "そうした答えは、あとから変わってもいいと思います。",
        "それより大切なのは、私の希望も、相手の希望と同じように、話し合いのテーブルへ置いていいと知ることでした。",
    ]
    for line in body2:
        if line == "__IMG_TOI__":
            continue
        nodes.append(p(line))
        nodes.append(sp())

    nodes.append(sp())

    body3 = [
        "婚活をしていると、「いい人だった」という言葉をよく使います。",
        "優しい。まじめ。仕事を続けている。家がある。話をきちんと聞いてくれる。",
        "どれも大切なことです。",
        "けれど、「いい人」と「一緒に暮らしたい人」は、必ずしも同じではないんですよね。",
        "相手に問題があるということではありません。",
        "私に問題があるということでもありません。",
        "ただ、二人の生活が重なるかどうかは、人柄のよさだけでは決まらない。",
        "どちらか一方の理想へ、もう一方が入り込むのでもない。",
        "二人がそれぞれに自分の人生を持ちながら、「自分のままで心地良くいられる」「一人よりも二人が、より喜びが増える」——そう思える場所を作れるかどうか。",
        "婚活を始めたばかりの私は、まだそのことをうまく説明できませんでした。",
        "それでも日記には、後の私につながる問いが、もう書かれていたんです。",
        "相手に合わせながら、自分が自分のしたいように生きられる人でいられるだろうか。",
        "この問いは、その後の婚活で何度も姿を変えて、私の前に現れることになります。",
        "続きはまた、次の話でお話しさせてくださいね。",
    ]
    for line in body3:
        nodes.append(p(line))
        nodes.append(sp())

    nodes.append(real_photo_node())
    nodes.append(sp())
    nodes.extend(cta_nodes())
    return nodes

def create_draft():
    body = {
        "draftPost": {
            "title": TITLE,
            "richContent": {"nodes": build_nodes(), "metadata": {"version": 1}},
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
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

def set_related_posts(draft_id):
    body = {"draftPost": {"relatedPostIds": RELATED_POST_IDS}, "fieldMask": "relatedPostIds"}
    r = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=body, timeout=30)
    print("関連記事設定:", "完了" if r.ok else f"失敗 {r.status_code} {r.text[:300]}")

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

def image_node(file_obj, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {
                "image": {"src": {"url": file_obj["url"]}}, "caption": caption,
                "containerData": {"width": {"size": "SMALL"}, "alignment": "CENTER"},
            }}

def find_index_after_text_contains(nodes, substr):
    for i, n in enumerate(nodes):
        if n.get("type") == "PARAGRAPH":
            for t in n.get("nodes", []):
                text = t.get("textData", {}).get("text", "")
                if substr in text:
                    return i
    return -1

def add_images(draft_id):
    files = {
        "eyecatch": upload_image_file(os.path.join(IMAGES_DIR, "2026-09-08_57sai_ep2_eyecatch_v2.png"), "2026-09-08_57sai_ep2_eyecatch_v2.png"),
        "memo": upload_image_file(os.path.join(IMAGES_DIR, "2026-09-08_57sai_ep2_memo_v2.png"), "2026-09-08_57sai_ep2_memo_v2.png"),
        "toi": upload_image_file(os.path.join(IMAGES_DIR, "2026-09-08_57sai_ep2_toi.png"), "2026-09-08_57sai_ep2_toi.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("私は、条件の向こう側にある暮らしを、見ようとしていたんです。", "memo", "条件の向こう側にある、暮らしを見ようとしていました。"),
        ("私は我慢するの？", "toi", "「私は我慢するの？」——そう書いた日がありました。"),
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
    draft_id = create_draft()
    if draft_id:
        set_related_posts(draft_id)
        set_seo(draft_id)
        add_images(draft_id)
