"""
嬉しいような、残念なような——ある退会のお話をさせてください
カテゴリ: 無料相談の前に読む / 恋愛経験が少ない人の婚活
2026-06-10
"""
import os, re, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む
    "69d23361-4fe7-4af6-a69e-2276e1f08417",  # 恋愛経験が少ない人の婚活
]

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "aa4700b5-badc-4875-91eb-d0026633922e",  # 婚活カウンセリング
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
]

RELATED_POST_IDS = [
    "ef922c0a-d808-4a03-aef8-c9be3c9c66b5",  # 20年後の幸せな自分から（女性向け）
    "19d45af3-381f-45b0-8f38-a9449c47addf",  # こんな私でも大丈夫？
    "488657cb-6e61-4104-b88d-d146349fd377",  # 言えなかった本音の疑問
]

TITLE   = "嬉しいような、残念なような——ある退会のお話をさせてください"
EXCERPT = "成婚退会じゃないけど、書かずにはいられませんでした。自己肯定感の低さ・気持ちのアップダウンを抱えて入会した彼女が、毎週のカウンセリングを通じて変わっていった話。そして予想外の結末と、仲人のリアルな気持ちをぶっちゃけます。"
SEO_DESC = "自己肯定感が低く、思い込みや過去の恋愛を引きずって入会した女性が、心理カウンセリングを通じて自分を取り戻していった記録。成婚退会ではないけれど、これも一つの婚活の成果だと感じた、仲人の正直なぶっちゃけブログです。"

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural daylight, East Asian appearance, no text. "
            "A beautiful Japanese woman in her late 20s to early 30s, sitting at a bright modern café, "
            "looking peacefully out the window with a gentle confident smile, black hair. "
            "Clean contemporary interior, soft natural light, professional lifestyle photography."
        ),
        "filename": "2026-06-10_jibun_wo_ikiru_eyecatch.png",
        "caption": "",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural daylight, East Asian appearance, no text. "
            "A Japanese woman in her late 20s sitting at a bright desk, writing thoughtfully in a journal or planner, "
            "with a serene and self-assured expression, black hair. "
            "Clean modern home setting, books and a small plant nearby, professional lifestyle photography."
        ),
        "filename": "2026-06-10_jibun_wo_ikiru_journal.png",
        "caption": "自分の気持ちを言葉にしていくことで、内側が少しずつ変わっていきます",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural daylight, East Asian appearance, no text. "
            "A Japanese woman in her late 20s walking alone outdoors on a bright sunny path, "
            "smiling joyfully, looking free and radiant, black hair, light casual outfit. "
            "Fresh green surroundings, cheerful open atmosphere, professional lifestyle photography."
        ),
        "filename": "2026-06-10_jibun_wo_ikiru_free.png",
        "caption": "自分でハンドルを握る感覚——それが、彼女が手に入れたものです",
    },
]

client = OpenAI(api_key=OPENAI_KEY)


def wix_headers():
    return {
        "Authorization": WIX_API_KEY,
        "wix-site-id":   WIX_SITE_ID,
        "Content-Type":  "application/json",
    }


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


def h(text, level=2):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": level}}


def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}


def section(heading_text):
    return [sp(), divider_node(), sp(), h(heading_text)]


def image_node(url, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": url}}, "caption": caption}}


def cta_node():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": "⬇️あなたに合った婚活を。無料相談はこちらから！⬇️",
            "decorations": [{"type": "LINK", "linkData": {
                "link": {"url": "https://www.asunaru.jp/soudan", "target": "BLANK"}
            }}]
        }}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}


def upload_image_binary(image_bytes, filename):
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "displayName": filename},
        timeout=30,
    )
    if not r.ok:
        print(f"  アップロードURL取得失敗: {r.status_code}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        print(f"  uploadUrl取得失敗: {data}")
        return None
    sep  = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print(f"  アップロード失敗: {ru.status_code} {ru.text[:200]}")
        return None
    file_obj = ru.json().get("file", {})
    url = file_obj.get("url", "")
    fid = file_obj.get("id", "")
    if not url:
        print(f"  URL取得失敗: {ru.json()}")
        return None
    m = re.search(r"/media/([^?#\s]+)", url)
    print(f"  → {url[:70]}...")
    return {"url": url, "id": m.group(1) if m else fid}


def generate_and_import_image(prompt, filename):
    print(f"\n[gpt-image-1] 生成中: {filename}")
    resp = client.images.generate(
        model="gpt-image-1", prompt=prompt, size="1536x1024", quality="high", n=1,
    )
    img_data = resp.data[0]
    if not img_data.b64_json:
        print("  b64_json取得失敗")
        return None
    print("  生成完了。Wixにアップロード中...")
    return upload_image_binary(base64.b64decode(img_data.b64_json), filename)


def build_nodes(img_eyecatch=None, img_journal=None, img_free=None):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # イントロ
    nodes.append(p("今日はね、ちょっと複雑な気持ちのご報告をさせてください。"))
    nodes.append(sp())
    nodes.append(p("成婚退会ではないんです。でも、書かずにはいられませんでした。"))
    nodes.append(sp())

    # セクション1
    nodes.extend(section("入会のきっかけ"))
    nodes.append(sp())
    nodes.append(p("婚活イベントに何度も足を運んでいたけれど、いつも同じ顔ぶれで。良い出会いに恵まれないまま時間だけが経ち、どんな人とフィーリングが合うのかも、どうやって関係を進めていけばいいのかも、だんだんわからなくなっていました。"))
    nodes.append(sp())
    nodes.append(p("以前の彼のことも、まだどこかに引きずっていて。"))
    nodes.append(sp())
    nodes.append(p("「寂しさを埋めるためじゃなく、ちゃんと自分の軸を持って、一緒に歩んでいける人に出会いたい。それも、本気で結婚を考えている男性と」"))
    nodes.append(sp())
    nodes.append(p("そういう思いで入会してくださいました。"))
    nodes.append(sp())
    nodes.append(p("最初のミーティングで、彼女は少し遠慮がちにこう言っていました。「自己肯定感が低くて、私なんかではいけないんじゃないかと思って…」と。"))
    nodes.append(sp())
    nodes.append(p("気持ちのアップダウンも、けっこうありました。"))
    nodes.append(sp())

    if img_eyecatch:
        nodes.append(image_node(img_eyecatch["url"], ""))
        nodes.append(sp())

    # セクション2
    nodes.extend(section("毎週のミーティングで、少しずつ"))
    nodes.append(sp())
    nodes.append(p("うちの相談所は、心理カウンセリングが得意です。だから毎週のようにミーティングを重ねながら、セルフイメージや、恋愛・結婚に関する思い込みを少しずつほぐしていきました。"))
    nodes.append(sp())
    nodes.append(p("これまでの恋愛で染みついた、偏った男性像や「女性はこうしなければ」という思い込み。気づかないうちに自分を縛っていた、そういうパターンをひとつひとつ見ていく作業です。"))
    nodes.append(sp())
    nodes.append(p("最初は、自分のためだけにお金や時間やエネルギーを使うことが、なんとなく苦手だとおっしゃっていました。誰かに尽くすことはできるけれど、誰かに助けてもらうこと、愛情を注いでもらうことが、うまく受け取れませんでした。"))
    nodes.append(sp())
    nodes.append(p("だからまず、過去の深い悲しみを癒すことから始めました。自分が情熱を注いでいたことを思い出したり、好きなことを少しずつ増やしていったり。自分の気持ちを大切にすること、自分のしたいことをさせてあげること。他者の意見を聞きすぎる癖を見直し、「他者基準」から「自分基準」で選択できるように。"))
    nodes.append(sp())
    nodes.append(p("お見合いやデートで出てくる、我慢する・遠慮する・合わせすぎるという癖も、一緒に丁寧に見ていきました。力を抜いて甘えられるように、ありのままでいられるように。"))
    nodes.append(sp())
    nodes.append(p("変化は、一直線ではありませんでした。後戻りしそうな気分になることも、もちろんありました。でも彼女は、そのたびに踏ん張りました。だんだんと大局観が育ってきて、ご自身の人生を俯瞰して語れるようになってきました。"))
    nodes.append(sp())
    nodes.append(p("最初は話があちこちに飛んでいたのが、整理されて、わかりやすくなっていきました。それが私には、すごくすごく嬉しかったです。"))
    nodes.append(sp())

    if img_journal:
        nodes.append(image_node(img_journal["url"], img_journal.get("caption", "")))
        nodes.append(sp())

    # セクション3
    nodes.extend(section("そして彼女が変わりました"))
    nodes.append(sp())
    nodes.append(p("気づけば、お見合いでの彼女がまったく違う人になっていました。"))
    nodes.append(sp())
    nodes.append(p("最初の頃と比べて、自分の意見を自然に言えるようになって。NOも、穏やかに言えるようになって。自分で自分のことを選べるようになって。"))
    nodes.append(sp())
    nodes.append(p("「自分が自分をご機嫌にする」ということが、少しずつわかってきました。足りないものに焦点を当てるんじゃなく、すでに満ち足りているものに意識が向くようになりました。自己受容が、じわじわと育ってきました。"))
    nodes.append(sp())
    nodes.append(p("そして彼女がある日、こう言ってくれました。"))
    nodes.append(sp())
    nodes.append(p("「今は、自分1人でも寂しくなくて。やってみたいことが増えて、誰に気兼ねすることもなく、自分で決めて、自分の気持ちを感じて、自分でやれる。その喜びと楽しさが、自信なのかわかんないけど、じわじわ湧いてきたんです。自分でハンドルを握ってる感覚、すごいなぁって」"))
    nodes.append(sp())
    nodes.append(p("「パートナーがいてもいなくても幸せで。以前のような重い気分の世界に、戻りにくくなった」"))
    nodes.append(sp())
    nodes.append(p("「パラレルワールドの、別の自分に移ってるのかもしれない」"))
    nodes.append(sp())
    nodes.append(p("そして、とっておきの一言。"))
    nodes.append(sp())
    nodes.append(p("「脳って、いかようにもなるんですね！！」"))
    nodes.append(sp())
    nodes.append(p("（もう、この言葉だけで、全部報われた気がしました）"))
    nodes.append(sp())

    # セクション4
    nodes.extend(section("仲人の、正直な気持ち"))
    nodes.append(sp())
    nodes.append(p("まさかのまさかで、中途退会になりました。"))
    nodes.append(sp())
    nodes.append(p("理由は——「まずは婚活より、自分を生きてみたい」"))
    nodes.append(sp())
    nodes.append(p("仲人の私としては、「せっかくいい感じになってきた——！」と思っていたところに（笑）。複雑ですよ。正直言えば。嬉しいような、残念なような、これでよかったのかなっていう戸惑いも、ちゃんとあります。"))
    nodes.append(sp())
    nodes.append(p("でも同時に、心のどこかで「そうか、よかった」とも思っています。"))
    nodes.append(sp())
    nodes.append(p("婚活がゴールではなくて、彼女が彼女らしく生きられるようになることの方が、ずっと大事なんじゃないかって。心理カウンセラーの自分が言っちゃいけないのかもしれないけれど（笑）、そう思っているのは本当のことです。"))
    nodes.append(sp())
    nodes.append(p("自分のハンドルを握り直した彼女が、これからどんな人生を歩んでいくのか。それが楽しみで、嬉しいです。"))
    nodes.append(sp())

    if img_free:
        nodes.append(image_node(img_free["url"], img_free.get("caption", "")))
        nodes.append(sp())

    # セクション5
    nodes.extend(section("最後に"))
    nodes.append(sp())
    nodes.append(p("自分1人を存分に楽しんで。やりたいことをやって、好きなものを好きと言えるようになって。それでもまた「パートナーと歩みたい」と思ったとき、ぜひまた一緒に婚活に取り組ませてほしいなぁと思っています。"))
    nodes.append(sp())
    nodes.append(p("声をかけてくれるのを、待っています。"))
    nodes.append(sp())
    nodes.append(p("そして今日これを読んでくださっている方へ。"))
    nodes.append(sp())
    nodes.append(p("婚活って、お相手を探す場所でもあるけれど、本来の自分を取り戻す場所でもあると、私は思っています。あすなる愛媛は、そういう伴走ができる相談所でありたいと、いつも思っています。"))
    nodes.append(sp())

    # CTA（中央寄せ）
    nodes.append(cta_node())

    return nodes


def main():
    # Step 1: 画像3枚を生成・アップロード
    img_eyecatch = generate_and_import_image(IMAGE_PROMPTS[0]["prompt"], IMAGE_PROMPTS[0]["filename"])
    img_journal  = generate_and_import_image(IMAGE_PROMPTS[1]["prompt"], IMAGE_PROMPTS[1]["filename"])
    if img_journal:
        img_journal["caption"] = IMAGE_PROMPTS[1]["caption"]
    img_free = generate_and_import_image(IMAGE_PROMPTS[2]["prompt"], IMAGE_PROMPTS[2]["filename"])
    if img_free:
        img_free["caption"] = IMAGE_PROMPTS[2]["caption"]

    # Step 2: richContent構築
    nodes = build_nodes(img_eyecatch=img_eyecatch, img_journal=img_journal, img_free=img_free)

    # Step 3: 下書き作成
    print("\n[Wix] 下書き作成中...")
    body = {
        "draftPost": {
            "title": TITLE,
            "memberId": MEMBER_ID,
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "relatedPostIds": RELATED_POST_IDS,
            "language": "ja",
            "richContent": {"nodes": nodes, "metadata": {"version": 1}},
            "excerpt": EXCERPT,
        }
    }
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(), json=body, timeout=30)
    if not r.ok:
        print(f"下書き作成失敗: {r.status_code} {r.text[:400]}")
        return
    draft_id = r.json().get("draftPost", {}).get("id")
    print(f"下書き作成完了: {draft_id}")

    # Step 4: カバー画像PATCH
    if img_eyecatch and draft_id:
        print("[Wix] カバー画像をPATCH中...")
        rp = requests.patch(
            f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
            headers=wix_headers(),
            json={
                "draftPost": {
                    "media": {
                        "wixMedia": {"image": {"id": img_eyecatch["id"], "url": img_eyecatch["url"]}},
                        "displayed": True,
                        "custom": False,
                    }
                },
                "fieldMask": "media"
            },
            timeout=30,
        )
        print("カバー画像PATCH完了" if rp.ok else f"失敗: {rp.status_code} {rp.text[:200]}")

    # Step 5: SEO PATCH（カバーと分けて送る）
    if draft_id:
        print("[Wix] SEO DESCをPATCH中...")
        rs = requests.patch(
            f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
            headers=wix_headers(),
            json={"draftPost": {"seoData": {"description": SEO_DESC}}, "fieldMask": "seoData.description"},
            timeout=30,
        )
        print("SEO PATCH完了" if rs.ok else f"SEO失敗: {rs.status_code} {rs.text[:200]}")

    print(f"\n✅ 完了！")
    print(f"下書きID: {draft_id}")
    print(f"タイトル: {TITLE}")
    print(f"\n⚠️  投稿後に確認してください:")
    print(f"  - 記事内の画像が正しく表示されているか")
    print(f"  - カバー画像が設定されているか")
    print(f"  - SEOフォーカスキーワードを手動で設定する（Wixエディター）")


if __name__ == "__main__":
    main()
