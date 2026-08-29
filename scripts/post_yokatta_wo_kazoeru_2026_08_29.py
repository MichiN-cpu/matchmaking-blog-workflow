"""
【男女共通】婚活が続く人ほど、実は「小さなよかった」を数えている。
カテゴリ: 仮交際
2026-08-29
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "3f5f378d-a4f4-47e0-90a7-ab4daa27504e",  # 仮交際
]
TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
]
RELATED_POST_IDS = [
    "29af95af-c7da-4507-bdbe-f53aa9f54309",  # 交際継続？交際終了？迷ったときほど答えは頭の外にある。
    "f71ec040-995d-4853-96b3-79d663703958",  # "リードしなきゃ"を、一人で抱えなくていい。
    "35d610c7-50ee-45ad-8d0a-310b7893b9b6",  # 「この人で本当にいいのかな」
]

TITLE = "【男女共通】婚活が続く人ほど、実は「小さなよかった」を数えている。――ドラマチックな出会いより、地味な習慣が結果を分ける話"
EXCERPT = "「また今回もダメだったかも」——婚活を続けていると、そんな気持ちに何度も出会います。実は婚活を続けられる人と、途中で心が折れてしまう人の違いは、才能でも運でもありません。松山市の結婚相談所あすなる愛媛の中嶋美知が、婚活を続けるための小さな習慣についてお伝えします。"
FOCUS_KEYWORD = "婚活 続かない 心が折れる 続けるコツ"

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

    nodes.append(p("今日は、婚活が「続く人」と「途中でしんどくなってしまう人」の違いについてお話ししたいと思います。実はこの違い、性格でも、運の良さでもないんです。"))
    nodes.append(sp())

    nodes.extend(section_heading("お見合いの帰り道、何を一番覚えていますか"))
    nodes.append(sp())
    nodes.append(p("お見合いや初デートが終わった帰り道。あなたは、何を一番よく覚えていますか。"))
    nodes.append(sp())
    nodes.append(p("「感じが良かったな」という印象より先に、「あそこ、ちょっと変な間があったな」「あの質問、変に思われたかな」ということの方が、なぜか強く残っていたりしませんか。"))
    nodes.append(sp())
    nodes.append(p("これ、実はあなたのせいではありません。私たちの脳は、放っておくと自然に「悪かった方」を優先的に拾い上げるようにできているんです。"))
    nodes.append(sp())
    nodes.append(p("心理学にはネガティビティ・バイアスという言葉があります。人の脳は、狩猟採集時代の名残で、良い出来事より悪い出来事、危険の兆候の方を強く記憶するようにできている。良いことと悪いことが同じ重さで起きても、記憶に残るのは悪いことの方が数倍強い——そんな研究結果もあるくらいです。"))
    nodes.append(sp())
    nodes.append(p("つまり「良かったことより、気になったことばかり思い出してしまう」のは、性格の弱さではなく、脳がもともと持っている反応パターンなんですね。これは、右利きの人が意識しなければ自然と右手を使ってしまうのと同じで、意識しない限り、脳は自動的に「悪い方」を選んで記憶してしまうんです。"))
    nodes.append(sp())
    # [IMG:station]
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("お見合いの後、良かった点よりも先に「でも、あそこがちょっと」と気になった点から思い出してしまう。LINEの返信が来ても、内容よりも「既読がつくまでの時間」の方が気になってしまう。せっかく楽しい時間を過ごしたはずなのに、家に着く頃には「今回もダメだったかもしれない」という気持ちの方が大きくなっている。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section_heading("「よかった」を数えられる人が、婚活を続けられる本当の理由"))
    nodes.append(sp())
    nodes.append(p("ここで面白いデータをひとつ。ポジティブ心理学の研究者バーバラ・フレドリクソンは、「拡張-形成理論」という考え方を提唱しています。ポジティブな感情を感じたとき、人の視野は物理的にも心理的にも広がり、次にとれる行動の選択肢が自然と増えるというものです。逆に、不安や落胆を感じているときは、視野が狭まり、「もうやめようかな」という選択肢しか見えなくなってしまう。"))
    nodes.append(sp())
    nodes.append(p("婚活を続けられる人は、実は特別に強い人でも、鈍感な人でもありません。彼らは意識的に——ときには無意識に——「今日、ちょっとよかったこと」を拾う習慣を持っているだけなんです。お見合いで一瞬でも笑えたこと。プロフィールを読んで「素敵だな」と思ってもらえたこと。緊張しながらも、自分から質問できたこと。そのひとつひとつは、劇的な「運命の出会い」ではありません。でも、この小さな「よかった」の積み重ねが、脳の中でドーパミンという物質を少しずつ分泌させ、「また次も頑張ってみようかな」という気持ちを作っていくんです。"))
    nodes.append(sp())
    nodes.append(p("感謝や良かったことを記録する習慣についての研究でも、同じような結果が出ています。毎日でなくても、週に数回「よかったこと」を書き留める人は、そうでない人に比べて主観的な幸福感が高く、睡眠の質も良い傾向にあるという報告があります。婚活のように、結果がすぐに出ない・浮き沈みのある道のりでは、この「よかった探し」の力が、想像以上に大事になってくるんですね。"))
    nodes.append(sp())
    nodes.append(p("愛媛・松山で婚活をしている30代の会員さんとお話ししていても、続けられる方に共通しているのは、実はこの「よかった探し」の上手さだったりします。"))
    nodes.append(sp())

    nodes.extend(section_heading("今日からできること、そして根っこから変えていくこと"))
    nodes.append(sp())
    nodes.append(p("まず、今日からできる小さなことから。お見合いやデートのあと、家に着いたらスマホのメモでも手帳でも構いません。「今日、よかったこと」をひとつだけ書き留めてみてください。「会話が続いた」でも「時間通りに会えて安心した」でも、どんなに小さなことでも大丈夫です。気になった点を反省するのは、その後でいいんです。"))
    nodes.append(sp())
    nodes.append(p("そしてもう一つ、少し根っこの話をさせてください。「気になる点ばかり思い出してしまう」というクセが強すぎる場合、それは単なる習慣というより、過去の経験からできあがった、もっと深い反応パターンであることも少なくありません。以前傷ついた経験があると、脳は「また同じことが起きないように」と、無意識に悪い兆候ばかりを探すようになっているんです。これは本人を守るために脳が頑張っている証拠でもあるのですが、婚活を続ける上では、少ししんどい働き方をしてしまっている状態とも言えます。"))
    nodes.append(sp())
    nodes.append(p("もしこのパターンに心当たりがあるなら、書き留める習慣だけでなく、心理カウンセラーでもある仲人の私と一緒に、そのパターンそのものを緩めていくこともできます。習慣を変えるより、パターンの根っこにアプローチする方が、実は近道になることも多いんですよ。"))
    nodes.append(sp())

    nodes.extend(section_heading("「よかった」の積み重ねの先にあるもの"))
    nodes.append(sp())
    nodes.append(p("小さな「よかった」を数える習慣は、婚活中だけのものではありません。結婚してからも、実はとても大事な力になります。"))
    nodes.append(sp())
    nodes.append(p("一緒に暮らし始めると、毎日が特別なことの連続ではなくなります。でも、夕食の後に「今日のお味噌汁、おいしかったよ」と言ってもらえたこと。忙しい一日の終わりに、ソファで隣に座って「お疲れさま」と言い合えること。そんな、ドラマチックとは程遠い小さな瞬間を、ちゃんと「よかった」として受け取れる人ほど、結婚生活を長く、穏やかに続けていけるんです。"))
    nodes.append(sp())
    # [IMG:couple]
    nodes.append(p("お互いに完璧を求め合うのではなく、日々の小さな「よかった」を、素直に伝え合いながら、ふたりでちょうどいい着地点を見つけていく。そんな関わり方を、私は\"素直婚\"と呼んでお勧めしています。婚活中の今、小さな「よかった」を拾う練習をしておくことは、そのまま将来の結婚生活の土台になっていくんですよ。"))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("次にお見合いやデートをした帰り道、家に着く前に、スマホのメモに「今日よかったこと」をひとつだけ書いてみてください。それだけで十分です。"))
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
    eyecatch_path = os.path.join(IMAGES_DIR, "2026-08-29_yokatta_wo_kazoeru_eyecatch.png")
    station_path  = os.path.join(IMAGES_DIR, "2026-08-29_yokatta_wo_kazoeru_station.png")
    couple_path   = os.path.join(IMAGES_DIR, "2026-08-29_yokatta_wo_kazoeru_couple.png")

    files = {
        "eyecatch": upload_image_file(eyecatch_path, "2026-08-29_yokatta_wo_kazoeru_eyecatch.png"),
        "station":  upload_image_file(station_path, "2026-08-29_yokatta_wo_kazoeru_station.png"),
        "couple":   upload_image_file(couple_path, "2026-08-29_yokatta_wo_kazoeru_couple.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("これは、右利きの人が意識しなければ自然と右手を使ってしまうのと同じで、意識しない限り、脳は自動的に「悪い方」を選んで記憶してしまうんです。", "station", "良かったことより、気になったことの方が先に浮かんでしまう夜もある。"),
        ("そんな、ドラマチックとは程遠い小さな瞬間を、ちゃんと「よかった」として受け取れる人ほど、結婚生活を長く、穏やかに続けていけるんです。", "couple", "「お疲れさま」と言い合えること自体が、もう「よかった」の一つ。"),
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
