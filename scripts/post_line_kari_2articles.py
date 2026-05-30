"""
仮交際×LINE 2記事投稿スクリプト
- 女性向け:「仮交際中、彼からLINEが来ない。それって、もう脈なし？」
- 男性向け:「仮交際中、LINEを送らない男性へ。女性が求めているのは「量」じゃなかった。」
2026-05-30
"""
import os, re, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_ID = "3f5f378d-a4f4-47e0-90a7-ab4daa27504e"  # 仮交際

TAG_FEMALE = [
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "a8fd177f-b3ba-4a57-9f81-c26ba1ec0488",  # 婚活相談
]
TAG_MALE = [
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "a8fd177f-b3ba-4a57-9f81-c26ba1ec0488",  # 婚活相談
]
RELATED = [
    "fe3d5fee-62be-4fdc-a23c-774eb57ff158",  # 仮交際で毎日連絡
    "78d9e1c5-9567-4c4c-a7d8-9b318a131ee9",  # 共同体験デート
    "5d049496-8d26-4eec-ae46-c27904067e5b",  # 仮交際をすぐ終えてしまう人
]

BASE_STYLE = (
    "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
    "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
    "real-world setting, professional lifestyle photography style, "
    "shallow depth of field, clean bright modern atmosphere, no text"
)

client = OpenAI(api_key=OPENAI_KEY)

def wix_headers():
    return {"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID, "Content-Type": "application/json"}

def nid():
    return str(uuid.uuid4())[:8]

def sp():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}
    ], "paragraphData": {}}

def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}

def make_text_nodes(text):
    result, pos = [], 0
    for m in re.compile(r'https?://\S+').finditer(text):
        if m.start() > pos:
            result.append({"type": "TEXT", "id": nid(), "nodes": [],
                           "textData": {"text": text[pos:m.start()], "decorations": []}})
        result.append({"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": m.group(0), "decorations": [
                           {"type": "LINK", "linkData": {"link": {"url": m.group(0), "target": "BLANK"}}}
                       ]}})
        pos = m.end()
    if pos < len(text):
        result.append({"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": text[pos:], "decorations": []}})
    return result or [{"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}]

def p(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": make_text_nodes(text), "paragraphData": {}}

def p_center(text):
    nodes = make_text_nodes(text)
    return {"type": "PARAGRAPH", "id": nid(), "nodes": nodes,
            "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}

def bold(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [],
         "textData": {"text": text, "decorations": [{"type": "BOLD", "fontWeightValue": 700}]}}
    ], "paragraphData": {}}

def h(text, level=2):
    return {"type": "HEADING", "id": nid(),
            "nodes": [{"type": "TEXT", "id": nid(), "nodes": [],
                        "textData": {"text": text, "decorations": []}}],
            "headingData": {"level": level}}

def heading_block(text, level=2):
    return [sp(), divider_node(), sp(), h(text, level)]

def image_node(file_info):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": file_info["url"]}}, "caption": ""}}

def cta():
    return [
        sp(),
        p_center("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan"),
    ]

def generate_and_upload(prompt_text, filename):
    print(f"  生成中: {filename}")
    resp = client.images.generate(
        model="gpt-image-1", prompt=prompt_text, size="1536x1024", quality="medium", n=1
    )
    image_bytes = base64.b64decode(resp.data[0].b64_json)
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "displayName": filename}, timeout=30,
    )
    if not r.ok:
        print(f"  URL取得失敗: {r.status_code}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    sep = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print(f"  アップロード失敗: {ru.status_code}")
        return None
    url = ru.json().get("file", {}).get("url", "")
    if not url:
        print("  URL取得失敗")
        return None
    print(f"  完了: {url[:70]}...")
    return {"url": url}

def post_draft(title, nodes, cover, tag_ids, excerpt, meta_desc):
    m = re.search(r"/media/([^?#\s]+)", cover["url"]) if cover else None
    cover_id = m.group(1) if m else ""

    body = {
        "draftPost": {
            "title": title,
            "richContent": {"nodes": nodes, "metadata": {"version": 1}},
            "categoryIds": [CATEGORY_ID],
            "memberId": MEMBER_ID,
            "tagIds": tag_ids,
            "excerpt": excerpt,
            "relatedPostIds": RELATED,
            "media": {
                "custom": True,
                "displayed": True,
                "wixMedia": {"image": {"id": cover_id, "url": cover["url"],
                                       "height": 1024, "width": 1536,
                                       "filename": cover["filename"]}},
            } if cover else {},
        }
    }
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(), json=body, timeout=30)
    if not r.ok:
        print(f"  投稿失敗: {r.status_code} {r.text[:300]}")
        return None
    draft_id = r.json().get("draftPost", {}).get("id")
    print(f"  下書き作成完了: {draft_id}")

    # メタディスクリプション
    requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
        headers=wix_headers(),
        json={"draftPost": {"seoData": {"description": meta_desc}}, "fieldMask": "seoData.description"},
        timeout=30,
    )
    return draft_id


# ─────────────────────────────────────────────
# 記事①：女性向け
# ─────────────────────────────────────────────

def build_female(imgs):
    i1, i2, i3 = imgs[0], imgs[1], imgs[2]
    n = []

    n.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    n.append(sp())
    n.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    n.append(sp())
    n.append(p("今日は、仲人をしていてほんとうによく聞く話をしようと思います。"))
    n.append(sp())
    n.append(p("「仮交際に入ったんですが、彼からLINEが全然来なくて……もう脈ないのかな」"))
    n.append(sp())
    n.append(p("そう打ち明けてくれる女性の多いこと。しかも、こちらから連絡したら返信はちゃんと来る。お見合いでは楽しそうにしていた。なのに、自分からは動いてこない。"))
    n.append(sp())
    n.append(p("気になりますよね。それは当然のことだと思います。"))
    n.append(sp())

    if i1:
        n.append(image_node(i1)); n.append(sp())

    n.extend(heading_block("彼がLINEを送らない理由、正直に言うと"))
    n.append(p("まず知っておいてほしいのは、男性の多くにとってLINEは「連絡のためのツール」だということ。"))
    n.append(sp())
    n.append(p("「次のデートは○日の△時に、○○で待ち合わせ」——この情報を伝えたら、そのLINEの役割は完了しているんです。「連絡完了！」と頭の中でひとまず完結してしまう。だから次のデートまで何も送ってこない、という男性がけっこういます。"))
    n.append(sp())
    n.append(p("さらに、「余計なことをして失敗したくない」という気持ちも働いていることがある。「変なことを送ってひかれたらどうしよう」「しつこいと思われたくない」——相手のことを大切にしているからこその遠慮が、LINEを遠ざけているケースも多いんです。"))
    n.append(sp())
    n.append(p("一方、女性にとってLINEはおしゃべりのツールであることが多い。1日に何度かやりとりがあるのが当たり前、という感覚で育ってきた方も少なくない。"))
    n.append(sp())
    n.append(p("この「前提のズレ」が、「LINEが来ない=気持ちが冷めた」という誤解を生んでしまうんですよね。"))
    n.append(sp())
    n.append(p("ちなみに、男性でもこまめにLINEをやりとりできる方がいますが、そういう方は女性と付き合ってきた経験が多く、女性のLINE文化に慣れていることが多い。仮交際中の不慣れな男性がLINEを送れないのは、ある意味で当然のことでもあります。"))

    n.extend(heading_block("こんなこと、ありませんか。"))
    n.append(p("彼からLINEが来ないと、スマホをつい何度も確認してしまう。"))
    n.append(sp())
    n.append(p("「もしかして、他の人と進めることにしたのかな」とネガティブな方向に考え始める。"))
    n.append(sp())
    n.append(p("次に会ったとき、探るような目で彼の表情を読もうとしてしまう。"))
    n.append(sp())
    n.append(p("——どれかひとつでも「あるかも」と思った方、その感覚はとても自然です。でもその不安が積み重なると関係を窮屈にしてしまうことがあるので、一緒に整理しましょう。"))
    n.append(sp())
    n.append(p('「LINEしない」は、彼の"慣れた反応パターン"かもしれない——右手で字を書く人が、左手で書こうとするとぎこちなくなる。でもそれは左手が下手なのではなく、右手が「慣れた動き」として体に刻まれているだけですよね。不安は性格ではなく、反応パターンです。「LINEが来ない=脈なし」と読んでしまうのも、過去の経験から学んだパターンが自動的に動いているだけかもしれない。そう思うと、少し楽になりませんか。'))

    n.extend(heading_block("仮交際に入ったら、最初に話しておくといいこと"))
    n.append(p("私がいつも会員さんにすすめているのは、仮交際に入ってすぐ、「どんな連絡の仕方が嬉しいか」をお互いに話してみること、です。"))
    n.append(sp())
    n.append(p("「LINEはどれくらいのペースが好きですか？」「電話の方がいいですか？」——そう聞いてみるだけで、かなりすれ違いが減ります。大事なのは「中間どころ」を一緒に決めること。どちらかが我慢するのではなく、お互いの真ん中を探して、やってみて、不満があれば少しずつ微調整していく。それでいいんです。"))
    n.append(sp())
    n.append(p("連絡の形は、LINEだけじゃありません。朝の「おはよう」一言でも、道端で見かけた猫や花の写真を送るだけでも、今日聞いていた曲を共有するのでも——形は何でもいい。「あなたのことを思い出した」が届けばいい。つながっている安心感が、多くの女性には大事なんですよね。頻度より、感じられることが大切です。"))
    n.append(sp())

    if i2:
        n.append(image_node(i2)); n.append(sp())

    n.extend(heading_block("ちなみに、私はLINEが少ない派（笑）"))
    n.append(p("余談ですが、私自身はLINEが苦手なタイプで、用件があるときに1回送って完結させたい人間なんです（笑）。女性の中にも、毎日のやりとりが疲れるという方はいます。だから「女性はみんなLINEをたくさんしたい」というわけでも、じつはないんですよ。"))
    n.append(sp())
    n.append(p("だからこそ、「どんな連絡スタイルが心地よいか」をお互いに話してみることが大事で。それが、関係の土台を作っていきます。"))

    n.extend(heading_block("LINEが少なくても、ご成婚した方がいます"))
    n.append(p("仲人をしていて、「彼からほとんど連絡が来ない」と悩んでいた女性が、ご成婚退会された例があります。交際中、彼からのLINEは週に1、2回。でも会うたびに誠実で、デートの計画もきちんと立ててくれて。「LINEは少ないけど、会えばちゃんとわかる」と彼女自身が気づいてから、関係が一気に深まりました。"))
    n.append(sp())
    n.append(p("LINEの頻度は、愛情のバロメーターではないんです。ただし——返信がいつも遅い、デートの約束もなかなか進まない、という場合は別の話。そのときは遠慮なく仲人に相談してください。"))
    n.append(sp())

    if i3:
        n.append(image_node(i3)); n.append(sp())

    n.extend(heading_block("今日の一歩"))
    n.append(p("次に彼と会うとき、または次のLINEで、一言聞いてみてください。「連絡って、どれくらいのペースが好きですか？」って。緊張するかもしれないけど、聞けた自分を、ちょっと褒めてあげてください。"))

    n += cta()
    return n


# ─────────────────────────────────────────────
# 記事②：男性向け
# ─────────────────────────────────────────────

def build_male(imgs):
    i1, i2, i3 = imgs[0], imgs[1], imgs[2]
    n = []

    n.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    n.append(sp())
    n.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    n.append(sp())
    n.append(p("今日は、仮交際に入った男性からよく出てくる疑問にお答えします。"))
    n.append(sp())
    n.append(p("「LINEって、どれくらい送ればいいんですか？」"))
    n.append(sp())
    n.append(p("「次のデートの日時は伝えたし、それで十分かなと思って……」"))
    n.append(sp())
    n.append(p("正直に言ってくれてありがとうございます（笑）。これ、ほんとうによくある話なんですよ。"))
    n.append(sp())

    if i1:
        n.append(image_node(i1)); n.append(sp())

    n.extend(heading_block("男性にとってのLINEと、女性にとってのLINE"))
    n.append(p("まず、ここから話しましょう。"))
    n.append(sp())
    n.append(p("男性の多くにとって、LINEは「連絡ツール」です。「次のデートは○日の△時」と伝えた時点で、そのLINEの役割は完了。「連絡完了！」と頭の中でひとまず完結してしまう。だからデートまで何も送らない、という男性が多い。男性社会では、用件がないのにメッセージを送り合う文化がそもそもないですよね。"))
    n.append(sp())
    n.append(p("それに、「余計なことをして失敗したくない」という気持ちも大きい。「変なことを送ってひかれたらどうしよう」「既読スルーされたら恥ずかしい」——そう思って、結局送らないままになる。これも、相手を大切にしているからこその遠慮だったりします。"))
    n.append(sp())
    n.append(p("一方、女性の多くにとってLINEは「おしゃべりのツール」。1日に何度かやりとりがあるのが自然で、それで「関係が続いている」という安心感を感じている方が多い。会っていない時間の関係を、LINEが繋いでいるんですよね。"))
    n.append(sp())
    n.append(p("この「前提のズレ」を知っているだけで、すれ違いがかなり減ります。"))

    n.extend(heading_block("こんなこと、心当たりはありませんか。"))
    n.append(p("お見合いでは楽しく話せたのに、LINEになると何を書けばいいかわからなくなる。"))
    n.append(sp())
    n.append(p("「また今度」と思っているうちに3日経っていた、なんてことがある。"))
    n.append(sp())
    n.append(p("相手から来たLINEには返すけど、自分からはほとんど送ったことがない。"))
    n.append(sp())
    n.append(p("——どれかひとつでも「あるかも」と思った方、その傾向を少し意識するだけで、関係の育ち方が変わるかもしれません。"))
    n.append(sp())
    n.append(p("「LINEしない」は自分の慣れたパターンかもしれない——右手で字を書くように、それがデフォルトになっているだけで、変えられないわけじゃないんです。不安は性格ではなく反応パターン、それはあなたも彼女も同じです。"))

    n.extend(heading_block("「送らない」が、彼女の不安を育てている"))
    n.append(p("人間の脳は、情報が少ないとき、ネガティブな方向で補完しようとします。「彼からLINEが来ない」→「もう気持ちが冷めたのかも」→「次のデートが怖くなってきた」——こういう連鎖が、LINEが来ない数日間で静かに起きていることがある。"))
    n.append(sp())
    n.append(p("あなたに悪意はない。ただ、何も送らなかっただけで、彼女の中では関係が後退しているかもしれない。それは、もったいないですよね。"))
    n.append(sp())

    if i2:
        n.append(image_node(i2)); n.append(sp())

    n.extend(heading_block("仮交際に入ったら、最初に話しておくといいこと"))
    n.append(p("実は、女性も全員が「毎日たくさんLINEしたい」わけではないんですよ。用件があるときに1回で完結させたい、という女性もいます（私自身もそのタイプです・笑）。"))
    n.append(sp())
    n.append(p("だから、仮交際に入ってすぐ、「連絡って、どれくらいのペースが好きですか？」と一度聞いてみることをお勧めします。お互いの好みを話して、ちょうどいい中間どころをひとまずやってみる。不満があれば少し微調整すればいい。それだけで、ぐっとすれ違いが減ります。"))
    n.append(sp())
    n.append(p("連絡の方法も、LINEだけじゃなくていい。電話が得意なら短い電話でもいい。朝に「おはよう」の一言でもいい。道端で見かけた猫や花の写真を送るだけでもいい。今日聞いていた曲を共有するのでもいい。「あなたのことを思い出した」が届けば、それで十分なんです。"))
    n.append(sp())
    n.append(p("つながっている安心感が、多くの女性には大事。頻度より、感じられることが大切です。"))

    n.extend(heading_block("LINEが苦手な男性が、ご成婚した話"))
    n.append(p("「LINEが苦手で、交際中もあまり送れていなかった」という男性がご成婚退会された例があります。あるとき「先生、LINEって何を送ればいいんですか」と正直に聞いてくれて。一緒に考えながら少しずつ送り始めたら——相手の女性の表情が変わって、デートの雰囲気も変わって。最終的にご成婚まで進みました。"))
    n.append(sp())
    n.append(p("LINEが苦手でも、大丈夫です。「送ろうとしている」という姿勢が伝わるかどうかが、大きいんです。それだけで、関係はじんわりと温かくなっていきます。"))
    n.append(sp())

    if i3:
        n.append(image_node(i3)); n.append(sp())

    n.extend(heading_block("今日の一歩"))
    n.append(p("今夜、彼女に一言だけ送ってみてください。内容は本当に何でもいい。「今日はお疲れでしたか」「先日は楽しかったです」——それだけで十分です。送った後の自分の気持ちを、少しだけ観察してみてください。"))

    n += cta()
    return n


# ─────────────────────────────────────────────
# メイン
# ─────────────────────────────────────────────

FEMALE_IMAGES = [
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A Japanese woman in her late 20s sitting alone at a bright café, "
            "holding her phone and looking at it with a thoughtful, slightly uncertain expression. "
            "Soft window light, white and neutral tones, calm and introspective mood."
        ),
        "filename": "2026-05-30_line_female_img1.png",
    },
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "Two Japanese people, a man and a woman in their late 20s to early 30s, "
            "sitting across from each other at a bright café table, talking naturally and smiling. "
            "Relaxed and open atmosphere, casual setting, warm daylight."
        ),
        "filename": "2026-05-30_line_female_img2.png",
    },
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A happy Japanese couple in their early 30s walking side by side in a bright urban park, "
            "smiling and relaxed, casual outfits, soft green background blurred. "
            "Joyful and comfortable atmosphere."
        ),
        "filename": "2026-05-30_line_female_img3.png",
    },
]

MALE_IMAGES = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "handsome Japanese man in his late 20s to early 30s, clean-cut appearance, clear skin, "
            "real-world setting, professional lifestyle photography style, "
            "shallow depth of field, clean bright modern atmosphere, no text. "
            "Man sitting at a desk or café, looking at his phone with a thoughtful, slightly puzzled expression. "
            "Soft neutral tones, contemplative mood."
        ),
        "filename": "2026-05-30_line_male_img1.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "real-world setting, professional lifestyle photography style, "
            "shallow depth of field, clean bright modern atmosphere, no text. "
            "Close-up of a smartphone screen on a white table showing a chat conversation, "
            "soft light, minimal and clean composition. No identifiable faces."
        ),
        "filename": "2026-05-30_line_male_img2.png",
    },
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A happy Japanese couple in their early 30s sitting together at a bright café table, "
            "both smiling naturally and relaxed, facing each other, warm and comfortable atmosphere. "
            "Soft blurred background, sense of ease and connection."
        ),
        "filename": "2026-05-30_line_male_img3.png",
    },
]


def main():
    # ── 女性向け ──────────────────────────────
    print("\n" + "=" * 50)
    print("【女性向け】画像生成中...")
    print("=" * 50)
    female_imgs = []
    for info in FEMALE_IMAGES:
        result = generate_and_upload(info["prompt"], info["filename"])
        female_imgs.append(result)

    print("\n【女性向け】本文構築・投稿中...")
    female_nodes = build_female(female_imgs)
    cover_f = {**female_imgs[0], "filename": FEMALE_IMAGES[0]["filename"]} if female_imgs[0] else None
    fid = post_draft(
        title="【女性向け】仮交際中、彼からLINEが来ない。それって、もう脈なし？",
        nodes=female_nodes,
        cover=cover_f,
        tag_ids=TAG_FEMALE,
        excerpt="仮交際中、彼からLINEが来ない日が続くとき。「もう興味なくなったの？」と不安になりますよね。でも実は、LINEをしない男性にはある理由があります。仲人カウンセラーが正直に解説します。",
        meta_desc="仮交際中、彼からLINEが来ない日が続くとき。「もう興味なくなったの？」と不安になりますよね。でも実は、LINEをしない男性にはある理由があります。仲人カウンセラーが正直に解説します。",
    )
    print(f"女性向け下書きID: {fid}")

    # ── 男性向け ──────────────────────────────
    print("\n" + "=" * 50)
    print("【男性向け】画像生成中...")
    print("=" * 50)
    male_imgs = []
    for info in MALE_IMAGES:
        result = generate_and_upload(info["prompt"], info["filename"])
        male_imgs.append(result)

    print("\n【男性向け】本文構築・投稿中...")
    male_nodes = build_male(male_imgs)
    cover_m = {**male_imgs[0], "filename": MALE_IMAGES[0]["filename"]} if male_imgs[0] else None
    mid = post_draft(
        title="【男性向け】仮交際中、LINEを送らない男性へ。女性が求めているのは「量」じゃなかった。",
        nodes=male_nodes,
        cover=cover_m,
        tag_ids=TAG_MALE,
        excerpt="仮交際中のLINE、何を送ればいいかわからない。でも実は、女性が求めているのは「文章の量」じゃなく「つながっている感覚」。仲人カウンセラーが男性向けに正直に解説します。",
        meta_desc="仮交際中のLINE、何を送ればいいかわからない。でも実は、女性が求めているのは「文章の量」じゃなく「つながっている感覚」。仲人カウンセラーが男性向けに正直に解説します。",
    )
    print(f"男性向け下書きID: {mid}")

    print("\n" + "=" * 50)
    print("✅ 2記事投稿完了！")
    print(f"  女性向け: {fid}")
    print(f"  男性向け: {mid}")
    print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")
    print("=" * 50)
    print("\n📌 次のステップ（Wixで手動）:")
    print("  1. 2記事ともフォーカスキーワードを設定（仮交際 LINE しない 男性）")
    print("  2. 女性向け → 来週水曜9:00 公開スケジュール")
    print("  3. 男性向け → 来週木曜9:00 公開スケジュール")
    print("  4. 画像が正しく表示されているか確認")


if __name__ == "__main__":
    main()
