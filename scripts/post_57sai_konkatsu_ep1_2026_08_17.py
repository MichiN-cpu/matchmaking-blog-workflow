"""
【女性向け】57歳、仲人婚活始めました。
カテゴリ: 自己紹介 / 再婚の婚活
2026-08-17
"""
import os, uuid, base64, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")

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
]
RELATED_POST_IDS = [
    "40fce56b-d4f7-4f8b-969c-0220955813f9",  # こんにちは、あすなる愛媛の結婚相談所です【自己紹介その①】
    "7b7d916b-7cbf-41a2-9524-49736ac65699",  # 結婚生活破綻→離婚の背景【自己紹介その②】
    "0454c26c-59f7-45bf-885f-5919287fc081",  # どんな妻/夫/結婚生活になる？未来を透視する方法【自己紹介その③】
]

TITLE = "【女性向け】57歳、仲人婚活始めました。"
EXCERPT = "「もう遅いかもしれない」。57歳で婚活を決めた仲人自身の実話、連載スタート。心理学を学んで気づいた無意識のパターン、そして\"今すぐ動くしかない\"と腹をくくった、ある女性会員との出会いについて。"
FOCUS_KEYWORD = "57歳 婚活 女性"

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

def link_node_centered(text, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]}}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}

def build_nodes():
    nodes = []
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())
    nodes.append(p("今日は少し趣向を変えて、新しいシリーズの第1話をお届けします。仲人としてではなく、一人の女性として婚活をしてきた、私自身の話です。何歳から始めても、ちゃんと道は開ける——そのことを、私の実体験を通してお伝えできたらと思っています。"))
    nodes.append(sp())

    nodes.append(p("30代半ばで離婚してから、私の中にはずっとある思いがありました。"))
    nodes.append(sp())
    nodes.append(p("もう一度、心を許せるパートナーシップを築きたい。"))
    nodes.append(sp())
    nodes.append(p("このまま、残念な結末のままでは終わりたくない。"))
    nodes.append(sp())
    nodes.append(p("そう思いながらも、なかなか一歩を踏み出せずにいた頃、私は心理学を学び始めました。"))
    nodes.append(sp())
    nodes.append(p("そこで気づいたことがあります。"))
    nodes.append(sp())
    nodes.append(p("お相手との関わり方も、家族との関わり方も、そもそも誰に惹かれるかということさえも、実は自分の内面がつくり出しているものだったんです。"))
    nodes.append(sp())
    nodes.append(p("相手のどんな資質を引き出すかさえ、自分次第だった。"))
    nodes.append(sp())
    nodes.append(p("「彼氏欲しいなぁ」なんて、口ではしょっちゅう言っていました。"))
    nodes.append(sp())
    nodes.append(p("でも本当は、ずっと気づいていなかったんです。"))
    nodes.append(sp())
    nodes.append(p("私には「好意を感じた人の前で良い子ぶって素の自分を出さない」「受け身」という二つのパターンがありました。"))
    nodes.append(sp())
    nodes.append(p("婚活をしていく中で、他のパターンにもいくつか気づいていくのですが、この二つが特に大きく影響を与えていたことに、後々気づくことになります。"))
    nodes.append(sp())
    nodes.append(p("自分からいいなと思う人にアプローチすることもなければ、相手からのアプローチにあからさまに嬉しい反応を返すこともない。"))
    nodes.append(sp())
    nodes.append(p("これでは、恋愛に発展しようがありません。"))
    nodes.append(sp())
    nodes.append(p("心理学の世界には「好意の返報性」という言葉があります。相手に好意を向けられたとき、こちらも好意で応えると、関係はぐっと近づく。逆にその反応が薄いと、相手は次のアクションを起こしにくくなってしまうんですね。"))
    nodes.append(sp())
    nodes.append(p("私はまさに、それをやっていました。"))
    nodes.append(sp())
    nodes.append(p("気になる人にほど、そういう反応をしてしまう。"))
    nodes.append(sp())
    nodes.append(p("だから余計に、うまくいかなかった。"))
    nodes.append(sp())
    nodes.append(p("そのことが少しずつわかってきたのが、あの頃でした。"))
    nodes.append(sp())
    # [IMG:kizuki]

    nodes.append(p("そんな私が、57歳になっていました。"))
    nodes.append(sp())
    nodes.append(p("ヒプノセラピー（催眠療法）で起業し、NLPを学び、NLPの講座を始め、TFTという心理療法も学びながら、ずっと心理カウンセリングを続けてきました。"))
    nodes.append(sp())
    nodes.append(p("そしてある時、幸せな夫婦関係から、幸せな家族が始まる。私たちは、その家族の影響をとても大きく受けている。そう強く感じるようになって、結婚相談所を始めたんです。"))
    nodes.append(sp())
    nodes.append(p("開業から半年ほど経った頃、一人の女性が入会されました。"))
    nodes.append(sp())
    nodes.append(p("50代半ば、私より年下で、ずいぶんお綺麗な方でした。"))
    nodes.append(sp())
    nodes.append(p("若く見えて、表情も声も会話もチャーミング。この方ならすぐに決まるだろうな、と正直、私は思っていました。"))
    nodes.append(sp())
    nodes.append(p("ところが、お申し込みは想像より年齢が上の方が多くて、同じ連盟に登録されている、ふさわしい年齢の男性会員の数も、思っていたよりずっと少なかったんです。"))
    nodes.append(sp())
    nodes.append(p("真摯にお見合いを重ねる彼女を見ていて、ふと、この先の自分の姿が頭をよぎりました。"))
    nodes.append(sp())
    nodes.append(p("彼女よりも年齢を重ねていて、彼女ほど華やかでもない私が、これから数年のんびりしていたとして、彼女より楽に婚活できるでしょうか。"))
    nodes.append(sp())
    nodes.append(p("すぐに60が来る。"))
    nodes.append(sp())
    nodes.append(p("50代で活動するのと、60代で活動するのとでは、大きな差が生まれる。それは、仲人としてたくさんの方を見てきたからこそ、はっきりと見えていました。50代の中でも、前半と後半とではもう明らかにハンデが違う。"))
    nodes.append(sp())
    nodes.append(p("だったら、今すぐやるしかない。"))
    nodes.append(sp())
    nodes.append(p("いえ、それよりも先に、こんな後悔が押し寄せてきました。"))
    nodes.append(sp())
    nodes.append(p("結婚相談所を始める前に、婚活しておけばよかった。"))
    nodes.append(sp())
    nodes.append(p("なぜなら、自社の中で自分が婚活することはできないからです。日本最大級の結婚相談所ネットワークであるIBJでも、私自身は活動できない。"))
    nodes.append(sp())
    nodes.append(p("これには、正直ショックを受けました。"))
    nodes.append(sp())
    nodes.append(p("どうしよう、何をしたらいいんだろう——そう思っていた57歳の春、ご縁があって、うちとは別の連盟の結婚相談所さんとお話しする機会がありました。"))
    nodes.append(sp())
    nodes.append(p("「うちの相談所に入会して、うちの連盟で活動されたらどうですか」"))
    nodes.append(sp())
    nodes.append(p("そう提案をいただいて、1日でも早く動くしかない、とその場で入会を決めました。"))
    nodes.append(sp())
    # [IMG:kesshin]

    nodes.append(p("めちゃくちゃドキドキしましたよ。"))
    nodes.append(sp())
    nodes.append(p("私自身、仲人という仕事をしているので、他の会員さんが感じるようなことは、きっと私も一通り感じたと思います。"))
    nodes.append(sp())
    nodes.append(p("お相手が見つからなかったら格好悪いな、とか。"))
    nodes.append(sp())
    nodes.append(p("ショックだろうな、とか。"))
    nodes.append(sp())
    nodes.append(p("見つからなかったら、お金の無駄遣いになってしまうな、もったいないな、とか。"))
    nodes.append(sp())
    nodes.append(p("その一方で、夢はどんどん膨らんでいって、今度こそ、めちゃくちゃ素敵な人と再婚するんだ、なんて思ったりもして。"))
    nodes.append(sp())
    nodes.append(p("そんなスタートでした。"))
    nodes.append(sp())
    nodes.append(p("そのときの私はまだ、これから2年、59歳になるまで婚活を続けることになるなんて、想像もしていませんでした。"))
    nodes.append(sp())
    nodes.append(p("数ヶ月あれば、いい方が見つかるはず。"))
    nodes.append(sp())
    nodes.append(p("そのくらいの気持ちで、少し浮かれていたように思います。"))
    nodes.append(sp())
    nodes.append(p("今振り返ると、あの頃の私を動かしていたのは、二つのことでした。"))
    nodes.append(sp())
    nodes.append(p("一つは、自分の中にある「受け身」「良い子ぶってしまう」というパターンに、気づいたこと。"))
    nodes.append(sp())
    nodes.append(p("もう一つは、婚活は年齢とともに条件が変わっていくという現実から、目を背けなかったことです。"))
    nodes.append(sp())
    nodes.append(p_bold("もし今、「まだ大丈夫」と思いながら、心のどこかで足踏みしている方がいたら。この二つだけ、頭の片隅に置いておいてもらえたら嬉しいです。"))
    nodes.append(sp())
    nodes.append(p("続きはまた、次の話でお話しさせてくださいね。"))
    nodes.append(sp())

    nodes.append(p_bold("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("「もう歳だから」と、心のどこかで諦めていることがあれば、その気持ちに一度だけ、こう聞き返してみてください。「本当に、遅いのかな？」それだけで大丈夫です。"))
    nodes.append(sp())

    nodes.append(link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"))
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
            "imageData": {"image": {"src": {"url": file_obj["url"]}}, "caption": caption}}

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
        "eyecatch": upload_image_file(os.path.join(IMAGES_DIR, "2026-08-17_57sai_eyecatch.png"), "2026-08-17_57sai_eyecatch.png"),
        "kizuki": upload_image_file(os.path.join(IMAGES_DIR, "2026-08-17_57sai_kizuki.png"), "2026-08-17_57sai_kizuki.png"),
        "kesshin": upload_image_file(os.path.join(IMAGES_DIR, "2026-08-17_57sai_kesshin.png"), "2026-08-17_57sai_kesshin.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insert_after = [
        ("そのことが少しずつわかってきたのが、あの頃でした。", "kizuki", "気づいたのは、自分の中の\"受け身\"というパターンでした。"),
        ("そう提案をいただいて、1日でも早く動くしかない、とその場で入会を決めました。", "kesshin", "1日でも早く。そう思って、その場で入会を決めました。"),
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
            "height": eyecatch.get("height", 1024), "width": eyecatch.get("width", 1024),
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
        add_images(draft_id)
        print("\nDRAFT_ID =", draft_id)
        print(f"編集URL: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog/post/{draft_id}")
