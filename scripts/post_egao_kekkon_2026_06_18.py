"""
【女性向け】笑顔が、婚活を変える。——お見合いで次のデートにつながる女性がやっていること
カテゴリ: お見合い
公開予定: 2026-06-18（水）下書き保存のみ
"""
import os, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["5089ac63-e2ce-4de1-b472-3512a77401af"]  # お見合い

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "d372d6c7-06f8-47fe-a647-6229a0b94c80",  # お見合い
    "021e7932-59b1-43ae-9c76-4b00cd73b587",  # 好印象
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
]

RELATED_POST_IDS = [
    "ef922c0a-d808-4a03-aef8-c9be3c9c66b5",  # 20年後の幸せな自分から（女性向け）
    "e4c0a476-25f8-4c5b-b78e-5eaae44ef39c",  # IBJプロフィール写真で「選ばれる」女性の服装ルール
    "59111839-05a2-4b2a-afeb-87acd564b09f",  # 軽く、軽く（女性向け）
]

TITLE   = "【女性向け】笑顔が、婚活を変える。——お見合いで次のデートにつながる女性がやっていること"
EXCERPT = "お見合いで「また会いたい」と思ってもらえる女性と、そうでない女性の違いは何でしょう？男性が女性を好きになる理由と、今日から始められる笑顔の習慣についてお伝えします。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman in her 30s, elegant refined features, model-like appearance, clear skin, "
            "sitting across a table in a bright modern cafe, warm genuine smile directed toward the viewer, "
            "real-world setting, professional lifestyle photography style, "
            "shallow depth of field, clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-18_egao_eyecatch.png",
        "caption": "笑顔が、次のデートへの扉を開く。",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman in her 30s, clear skin, "
            "standing at a convenience store counter, warm natural smile, "
            "handing over a card or cash with a gentle smile, "
            "real-world lifestyle setting, professional photography style, "
            "clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-18_egao_convenience.png",
        "caption": "日常のひとつひとつが、笑顔の練習になる。",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman in her 30s, "
            "sitting at a desk with a laptop, glancing at a small round mirror placed beside the laptop, "
            "gentle self-aware smile, modern home office or workspace setting, "
            "professional lifestyle photography style, shallow depth of field, "
            "clean bright atmosphere, no text"
        ),
        "filename": "2026-06-18_egao_mirror.png",
        "caption": "鏡はいちばんの婚活ツール。",
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


def p_bold(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": text,
            "decorations": [{"type": "BOLD", "boldData": {"bold": True}}]
        }}
    ], "paragraphData": {}}


def h(text, level=2):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": level}}


def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}


def section(heading_text, level=2):
    return [sp(), divider_node(), sp(), h(heading_text, level)]


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


def build_nodes(url_eyecatch, url_convenience, url_mirror):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())
    nodes.append(p("今日は、お見合いを重ねてもなかなか仮交際に進めない……という女性にぜひ読んでほしい話です。"))
    nodes.append(sp())
    nodes.append(p("男性が女性を好きになる理由、実はシンプルに2つが大きく関わっているんですよね。これを知っておくだけで、婚活の見え方がちょっと変わってきます。"))
    nodes.append(sp())

    if url_eyecatch:
        nodes.append(image_node(url_eyecatch, "笑顔が、次のデートへの扉を開く。"))
        nodes.append(sp())

    # セクション1
    nodes.extend(section("男性が「いいな」と思う理由"))
    nodes.append(sp())
    nodes.append(p("結婚相談所で長年、男性会員さんたちを見てきてわかったことがあります。"))
    nodes.append(sp())
    nodes.append(p("男性がプロフィールを見てお申し込みをする理由、第1位は——写真の顔が好みかどうか。"))
    nodes.append(sp())
    nodes.append(p("これはもう、シンプルにそうなんです。「もちろんわかってます！」と思った方も多いかもしれません（笑）。"))
    nodes.append(sp())
    nodes.append(p("そして、お見合い当日。仮交際に進むかどうかを男性が決める理由も、やっぱりこの2つが大きい。"))
    nodes.append(sp())
    nodes.append(p_bold("①リアルな顔が、自分の好みかどうか"))
    nodes.append(p_bold("②自分に向かって、笑顔を向けてくれるかどうか"))
    nodes.append(sp())
    nodes.append(p("もちろん、それ以降の要素もあります。子どもが欲しいかどうか、料理が好きかどうか、価値観や生活スタイルが合うかどうか——男性によって違う、それぞれの希望条件です。これも大切な要素ではあるんです。"))
    nodes.append(sp())
    nodes.append(p('でも、①と②は、どの男性にも共通する“まず最初のフィルター”。そしてここに、婚活を楽にする大きなヒントが隠れているんですよね。'))
    nodes.append(sp())

    # セクション2
    nodes.extend(section("お見合いの席に着いた時点で、①はほぼクリア"))
    nodes.append(sp())
    nodes.append(p("ちょっと考えてみてください。"))
    nodes.append(sp())
    nodes.append(p("自分の好みの男性に申し込んで（あるいは申し込まれて）お見合いが成立したということは——よほど写真と実物が違わない限り、①の「顔が好み」はすでにクリアしているんです。"))
    nodes.append(sp())
    nodes.append(p("つまり、お見合いの席に着いた時点で、もう半分は乗り越えているようなもの。"))
    nodes.append(sp())
    nodes.append(p_bold("あとは②、笑顔だけ。"))
    nodes.append(sp())
    nodes.append(p("これを意識しておくだけで、お見合いの成功率はぐっと変わってきます。"))
    nodes.append(sp())

    # セクション3
    nodes.extend(section("でも、急には笑えない。それが現実"))
    nodes.append(sp())
    nodes.append(p("「笑顔でいよう」って、言葉で言うのは簡単なんですよね。"))
    nodes.append(sp())
    nodes.append(p("お見合いの場って、緊張するし、真剣に話をしようとすると、どうしても顔がキリッとしてしまう。"))
    nodes.append(sp())
    nodes.append(p("実は……かつての私もそうだったんです（汗）。"))
    nodes.append(sp())
    nodes.append(p("真面目な話をしているとき、「なんか怖い顔になってるよ」って人に言われて。「えっ、自分そんな顔してるの？」ってびっくりした記憶があります。それから意識するようにして、今もなるべく普段からにこにこするよう心がけています（笑）。"))
    nodes.append(sp())
    nodes.append(p("これ、意識しているつもりで、無意識に出てしまう反応パターンなんですよね。"))
    nodes.append(sp())
    nodes.append(p("右利きの人が急に左手でお箸を持とうとすると、ぎこちなくなるのと同じ。真剣になると自動的に「真顔モード」に入ってしまうのは、性格じゃなくて、長年の慣れた反応パターンなんです。"))
    nodes.append(sp())
    nodes.append(p("だからこそ、変えられます。繰り返しで身についたものは、繰り返しで更新できるんですよね。"))
    nodes.append(sp())

    # セクション4（ミニ診断）
    nodes.extend(section("今の自分の表情、ちょっと確認してみてください"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("誰かと向き合って真剣に話しているとき、ふと「あ、自分いま怖い顔してるかも」って気になることがある。"))
    nodes.append(sp())
    nodes.append(p("集中しているとき、気づいたら眉間にしわが寄っていることがある。"))
    nodes.append(sp())
    nodes.append(p("家でテレビを見ているとき、無表情のまま見ていることがある。"))
    nodes.append(sp())
    nodes.append(p("——どれかひとつでも「あるかも」と思った方。お見合いの場でも、きっと同じことが起きています。だって、表情は日常の積み重ねだから。"))
    nodes.append(sp())
    nodes.append(p("ちなみに、このブログを読んでいる今——あなたの表情はどうですか？😊"))
    nodes.append(sp())

    # セクション5
    nodes.extend(section("笑顔は、日常の中でつくるもの"))
    nodes.append(sp())
    nodes.append(p("だから私がお勧めしているのは、日常生活の中で笑顔を「通常モード」にしてしまうこと。"))
    nodes.append(sp())
    nodes.append(p("コンビニのレジで、「ありがとうございます」とニコッとする。"))
    nodes.append(sp())
    nodes.append(p("駅の改札で「おはようございます」と言ってくれる駅員さんに、にっこり返す。"))
    nodes.append(sp())
    nodes.append(p("道を譲ってもらったとき、ありがとうとにこっと伝える。"))
    nodes.append(sp())
    nodes.append(p("歩いているとき、口角をすこし上げてみる。（顔の筋トレだと思って！）"))
    nodes.append(sp())
    nodes.append(p("テレビやYouTubeを見ているときも、穏やかな表情で見る。頬の筋肉をすこし上げるだけでいいんですよね。"))
    nodes.append(sp())
    nodes.append(p("これを繰り返していくうちに、穏やかな表情＋笑顔が「自分のデフォルト」になっていきます。"))
    nodes.append(sp())
    nodes.append(p("そして、そういう人がお見合いの場に来ると——自然に笑顔が出るんです。「笑わなきゃ」って頑張らなくても。"))
    nodes.append(sp())

    if url_convenience:
        nodes.append(image_node(url_convenience, "日常のひとつひとつが、笑顔の練習になる。"))
        nodes.append(sp())

    # セクション6（鏡）
    nodes.extend(section("鏡を、そばに置く"))
    nodes.append(sp())
    nodes.append(p("営業職の方や受付の女性って、机の前にこっそり小さな鏡を置いていることがありますよね。"))
    nodes.append(sp())
    nodes.append(p("いつでも自分の表情をチェックできるように、と。"))
    nodes.append(sp())
    nodes.append(p("それ、本当に合理的な習慣だと思うんです。"))
    nodes.append(sp())
    nodes.append(p("パソコンのそばに、小さな手鏡を置いてみてください。作業の合間にふっと見て、「あ、今ちょっと怖い顔してたな」って気づけるだけでいい。"))
    nodes.append(sp())
    nodes.append(p("気づくことが、変わる第一歩ですから。"))
    nodes.append(sp())

    if url_mirror:
        nodes.append(image_node(url_mirror, "鏡はいちばんの婚活ツール。"))
        nodes.append(sp())

    # セクション7（科学的根拠）
    nodes.extend(section("なぜ笑顔がこんなに大切なのか"))
    nodes.append(sp())
    nodes.append(p("すこし深い話をしますね。"))
    nodes.append(sp())
    nodes.append(p("神経科学の分野に「顔面フィードバック仮説」というものがあります。表情が感情をつくる——つまり、笑顔を意識的に作ることで、脳に「穏やか」「楽しい」というシグナルが伝わるという考え方です。笑うから楽しくなる、という流れです。"))
    nodes.append(sp())
    nodes.append(p("また、コミュニケーション学では、人と人のやりとりの大部分は言葉ではなく表情・声のトーン・姿勢などの非言語情報で伝わると言われています。どんなに丁寧な言葉を選んでも、表情が硬いと、相手には「冷たい人」「緊張している人」として伝わってしまう。"))
    nodes.append(sp())
    nodes.append(p("そして社会心理学の「単純接触効果」の研究でも、温かみのある表情の人は繰り返し会うほど好感度が上がるとわかっています。お見合いのたった1時間でも、笑顔は相手の記憶に確かに残るんです。"))
    nodes.append(sp())

    # 希望への着地
    nodes.extend(section("笑顔が通常モードになった先に"))
    nodes.append(sp())
    nodes.append(p("日常の中で穏やかな表情と笑顔が自分のスタンダードになっていくと——お見合いでも、自然にそれが出るようになります。"))
    nodes.append(sp())
    nodes.append(p("「この人といると、なんか安心するな」"))
    nodes.append(p("「一緒にいて楽しいな」"))
    nodes.append(sp())
    nodes.append(p("そう感じてもらえるのは、顔が整っているからでも、話が上手いからでもなくて。"))
    nodes.append(sp())
    nodes.append(p("穏やかな表情で、相手の話にニコっと反応してくれるから。ただ、それだけなんですよね。"))
    nodes.append(sp())
    nodes.append(p("じんわり、でも確かに、相手の気持ちが動いていきます。お見合いが終わって「また会いたい」と思ってもらえる確率は、ぐっと変わってきます。"))
    nodes.append(sp())
    nodes.append(p("自分の好みの男性とお見合いにこぎつけたなら——あとは笑顔だけ。日常からすこしずつ、育てていきましょうね。"))
    nodes.append(sp())

    # 今日の一歩
    nodes.extend(section("今日の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、誰かと話すとき——1秒だけ、口角をいつもより1ミリ上げてみてください。それだけでいいんです。小さな習慣が、積み重なっていきます。"))
    nodes.append(sp())

    # CTA
    nodes.append(cta_node())

    return {"nodes": nodes}


def upload_image_binary(image_bytes, filename):
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "displayName": filename},
        timeout=30,
    )
    if not r.ok:
        print(f"  アップロードURL取得失敗: {r.status_code} {r.text[:200]}")
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
    if not url:
        print(f"  URL取得失敗: {ru.json()}")
        return None
    print(f"  → {url[:80]}...")
    return url


def generate_and_upload_image(prompt, filename):
    print(f"\n[gpt-image-1] 生成中: {filename}")
    resp = client.images.generate(
        model="gpt-image-1", prompt=prompt, size="1536x1024", quality="high", n=1,
    )
    img_data = resp.data[0]
    if not img_data.b64_json:
        print("  b64_json取得失敗")
        return None
    img_bytes = base64.b64decode(img_data.b64_json)
    save_path = os.path.join(os.path.dirname(__file__), f"../drafts/images/{filename}")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(img_bytes)
    print("  生成完了。Wixにアップロード中...")
    return upload_image_binary(img_bytes, filename)


def create_draft(rich_content):
    body = {
        "draftPost": {
            "title": TITLE,
            "memberId": MEMBER_ID,
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "richContent": rich_content,
        }
    }
    r = requests.post(
        f"{WIX_BASE}/blog/v3/draft-posts",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"下書き作成失敗: {r.status_code} {r.text[:300]}")
        return None
    return r.json().get("draftPost", {}).get("id")


def update_draft(post_id, cover_url):
    body = {
        "draftPost": {
            "coverMedia": {"image": {"src": {"url": cover_url}}},
            "excerpt": EXCERPT,
            "seoData": {"description": SEO_DESC},
            "relatedPostIds": RELATED_POST_IDS,
        },
        "fieldMask": "coverMedia,excerpt,seoData.description,relatedPostIds"
    }
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{post_id}",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"PATCH失敗: {r.status_code} {r.text[:300]}")
    return r.ok


def main():
    print("=== 笑顔×婚活 記事 投稿スクリプト ===\n")

    # 1. アイキャッチ生成
    print("[1] アイキャッチ画像を生成中...")
    url_eyecatch = generate_and_upload_image(IMAGE_PROMPTS[0]["prompt"], IMAGE_PROMPTS[0]["filename"])

    # 2. コンビニシーン生成
    print("\n[2] 本文画像（コンビニシーン）を生成中...")
    url_convenience = generate_and_upload_image(IMAGE_PROMPTS[1]["prompt"], IMAGE_PROMPTS[1]["filename"])

    # 3. 鏡シーン生成
    print("\n[3] 本文画像（鏡シーン）を生成中...")
    url_mirror = generate_and_upload_image(IMAGE_PROMPTS[2]["prompt"], IMAGE_PROMPTS[2]["filename"])

    # 4. richContent構築
    print("\n[4] richContent構築中...")
    rich_content = build_nodes(url_eyecatch, url_convenience, url_mirror)

    # 5. 下書き作成
    print("\n[5] Wix下書き作成中...")
    post_id = create_draft(rich_content)
    if not post_id:
        print("失敗。終了します。")
        return

    print(f"  → 下書きID: {post_id}")

    # 6. カバー画像・抜粋・関連記事を更新
    if url_eyecatch:
        print("\n[6] カバー画像・抜粋・関連記事を更新中...")
        ok = update_draft(post_id, url_eyecatch)
        print(f"  → {'成功' if ok else '失敗'}")

    print(f"\n✅ 完了！\n下書きID: {post_id}")
    print("Wixブログ管理画面で確認してください。")


if __name__ == "__main__":
    main()
