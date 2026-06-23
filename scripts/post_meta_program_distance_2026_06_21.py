"""
「かまってほしい」と「ひとりにして」は、どちらも愛の形。
カテゴリ: 仮交際（3f5f378d-a4f4-47e0-90a7-ab4daa27504e）
公開予定: 下書き保存のみ
"""
import os, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["3f5f378d-a4f4-47e0-90a7-ab4daa27504e"]

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    "d4d160ee-f3a6-44b6-9a82-66945f40f3b8",  # LINE
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
]

RELATED_POST_IDS = [
    "36915afc-e0aa-4b34-898b-106f66f11f33",  # 仮交際中、彼からLINEが来ない
    "89efea38-cc60-4f52-a7d4-0c2b7fb0e515",  # 仮交際中、LINEを送らない男性へ
    "78d9e1c5-9567-4c4c-a7d8-9b318a131ee9",  # 「どこ行こうか」から、ふたりは始まる
]

TITLE = (
    '「かまってほしい」と「ひとりにして」は、どちらも愛の形。'
    '——距離感の違いを知ると、婚活の"違和感"が消えていく。'
)
EXCERPT = (
    "LINEが少ないと不安になる人。多すぎると苦しくなる人。"
    "実はそれ、愛情の問題じゃなく「距離感のタイプ」の違いかもしれません。"
    "NLPのメタプログラムで読み解く、ふたりの心地よい距離のつくり方を、"
    "心理カウンセラー仲人の中嶋美知がお伝えします。"
)
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian couple in their 30s, "
            "beautiful Japanese woman with elegant refined features and model-like appearance, clear skin, "
            "handsome Japanese man, couple sitting on a park bench with a comfortable small gap between them, "
            "both smiling peacefully, woman looking at the man, man gazing at the sky relaxed, "
            "green park setting with soft sunlight through trees, "
            "shallow depth of field, clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-21_metaprogram_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman with elegant refined features, model-like appearance, clear skin, "
            "woman sitting alone at a stylish cafe by the window, reading a book, "
            "peaceful content expression, cup of coffee on the table, "
            "morning light streaming through window, bright airy cafe interior, "
            "shallow depth of field, clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-21_metaprogram_solo.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian couple in their 30s, "
            "beautiful Japanese woman with elegant refined features, model-like appearance, clear skin, "
            "handsome Japanese man in smart casual, couple having a warm conversation at a cozy restaurant, "
            "leaning slightly toward each other, genuine smiles, eye contact, "
            "intimate dinner setting with soft ambient light, "
            "shallow depth of field, clean bright modern atmosphere, no text"
        ),
        "filename": "2026-06-21_metaprogram_conversation.png",
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
        print(f"  upload URL failed: {r.status_code} {r.text[:200]}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        print(f"  uploadUrl missing: {data}")
        return None
    sep  = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print(f"  upload failed: {ru.status_code} {ru.text[:200]}")
        return None
    file_obj = ru.json().get("file", {})
    url = file_obj.get("url", "")
    if not url:
        print(f"  URL missing: {ru.json()}")
        return None
    print(f"  -> {url[:80]}...")
    return url


def generate_and_upload_image(prompt, filename):
    print(f"\n[gpt-image-1] generating: {filename}")
    resp = client.images.generate(
        model="gpt-image-1", prompt=prompt, size="1536x1024", quality="high", n=1,
    )
    img_data = resp.data[0]
    if not img_data.b64_json:
        print("  b64_json missing")
        return None
    img_bytes = base64.b64decode(img_data.b64_json)
    save_path = os.path.join(os.path.dirname(__file__), f"../drafts/images/{filename}")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(img_bytes)
    print("  done. uploading to Wix...")
    return upload_image_binary(img_bytes, filename)


def build_nodes(url_eyecatch, url_solo, url_conversation):
    nodes = []

    # A01 A02: greeting
    nodes.append(p('こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊'))
    nodes.append(sp())
    nodes.append(p('毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。'))
    nodes.append(sp())

    # intro
    nodes.append(p('LINEの返信が遅い。'))
    nodes.append(sp())
    nodes.append(p('LINEの返事が短い。'))
    nodes.append(sp())
    nodes.append(p('それだけで、「この人、私に興味ないのかな」って思ったこと、ありませんか。'))
    nodes.append(sp())
    nodes.append(p('逆に、LINEがたくさん来すぎて、返すのがしんどい。せっかくいい人なのに、なんだか息苦しくなってきた——そんな経験がある方も、きっといらっしゃると思います。'))
    nodes.append(sp())
    nodes.append(p('実はこれ、どちらかが悪いわけじゃないんです。'))
    nodes.append(sp())
    nodes.append(p('ただ、人との"心地よい距離感"が、ふたりの間でずれている。'))
    nodes.append(sp())
    nodes.append(p('それだけのことなんですよね。'))
    nodes.append(sp())

    if url_eyecatch:
        nodes.append(image_node(url_eyecatch, 'ふたりの「心地よい距離」は違って当たり前'))
        nodes.append(sp())

    # section 1: meta program
    nodes.extend(section('NLPの「メタプログラム」って知っていますか？'))
    nodes.append(sp())
    nodes.append(p('NLP（神経言語プログラミング）には、「メタプログラム」という考え方があります。'))
    nodes.append(sp())
    nodes.append(p('これは、人が無意識に持っている"思考や行動のクセ"のようなもので、自分では気づいていないけれど、日常のあらゆる判断や感じ方に影響しているんです。'))
    nodes.append(sp())
    nodes.append(p('その中に「他者との関わり方」に関するカテゴリーがあります。'))
    nodes.append(sp())
    nodes.append(p('簡単に言うと、人にはそれぞれ"人と一緒にいるときに一番自分らしくいられるバランス"があるということ。'))
    nodes.append(sp())
    nodes.append(p('これは良い悪いの話じゃなくて、持って生まれた性質のようなものなんですよね。'))
    nodes.append(sp())

    # section 2: which type
    nodes.extend(section('あなたは、どちら寄りですか？'))
    nodes.append(sp())
    nodes.append(p('ものすごく極端な両端の話をすると——'))
    nodes.append(sp())
    nodes.append(p('ひとつは「個人型」と呼ばれる傾向。自分ひとりの世界で過ごすことにモチベーションが高まって、居心地の良さを感じるタイプです。'))
    nodes.append(sp())
    nodes.append(p('もうひとつは、常に誰かが一緒にいることでワクワクして、楽しくて、幸せだなぁと感じる傾向。'))
    nodes.append(sp())
    nodes.append(p('そしてね、多くの人はその中間のどこかにいるんです。'))
    nodes.append(sp())

    if url_solo:
        nodes.append(image_node(url_solo, 'ひとりの時間で自分を整える——それも大切な愛の形'))
        nodes.append(sp())

    nodes.append(p('人とのつながりの時間がある程度あって、自分ひとりの時間もあると幸せを感じる人。'))
    nodes.append(sp())
    nodes.append(p('基本的にはひとりだけど、1日のうちの10分とか数時間ちょこちょこ話すことで満足する人。'))
    nodes.append(sp())
    nodes.append(p('ほぼ誰かがそばにいて、何も話さなくても近くにいるだけで気持ちが安定して、自律神経も整う人。'))
    nodes.append(sp())
    nodes.append(p('ほんとうに、人によってまったく違うんです。'))
    nodes.append(sp())

    # section 3: false consensus
    nodes.extend(section('「自分と同じ」だと思っちゃう、これが落とし穴'))
    nodes.append(sp())
    nodes.append(p('ここが一番大事なポイントなんですが——人は、自分が感じている感覚をみんなも同じだと、ついつい思ってしまうんです。'))
    nodes.append(sp())
    nodes.append(p('だって、他の人の感覚ってわからないじゃないですか。'))
    nodes.append(sp())
    nodes.append(p('だから、自分の感覚では寂しいのに「どうしてあの人は連絡くれないんだろう」「どうしてしょっちゅう会ってくれないんだろう」って思う。'))
    nodes.append(sp())
    nodes.append(p('一方で、自分の感覚ではしょっちゅう一緒にいるのがしんどい人は、「なんでこの人はいつもLINEや電話してきて、自分の時間を邪魔するんだろう」ってネガティブな気分になっていく。'))
    nodes.append(sp())
    nodes.append(p('心理学では「偽の合意効果（False Consensus Effect）」と呼ばれる認知バイアスがあって、人は自分の価値観や行動パターンが"普通"だと無意識に信じる傾向があるんです。'))
    nodes.append(sp())
    nodes.append(p_bold('つまり、「私が寂しいんだから、あの人も寂しいはず」「僕がひとりで平気なんだから、あの人も平気なはず」——そう思い込んでしまう。'))
    nodes.append(sp())
    nodes.append(p('でも、ふたりの"心地よい距離"は本当に違うんです。'))
    nodes.append(sp())
    nodes.append(p('これは愛情の量の問題じゃない。距離感のタイプが違うだけ。'))
    nodes.append(sp())

    # section 4: not just LINE
    nodes.extend(section('LINEの頻度の話だけじゃない'))
    nodes.append(sp())
    nodes.append(p('この距離感の違いって、LINEだけの話じゃないんですよね。'))
    nodes.append(sp())
    nodes.append(p('一緒にいる時間の長さ、休日の過ごし方、住む場所の選び方——ぜんぶつながってきます。'))
    nodes.append(sp())
    nodes.append(p('たとえば単身赴任。全然平気な人もいれば、寂しくてしょうがないから「転勤がない仕事のお相手と結婚したい」という方もいらっしゃいますよね。'))
    nodes.append(sp())
    nodes.append(p('どちらが正しいわけでもない。ただ、違う。'))
    nodes.append(sp())
    nodes.append(p('神経科学の観点で言えば、人によって「共調整（Co-regulation）」——誰かがそばにいることで神経系が落ち着くタイプと、「自己調整（Self-regulation）」——ひとりの静かな時間で神経系を整えるタイプがいると考えられています。'))
    nodes.append(sp())
    nodes.append(p('どちらも脳と自律神経のしくみとして正常なんです。'))
    nodes.append(sp())

    # section 5: communication
    nodes.extend(section('「私はね」「僕はね」から始まる、すり合わせ'))
    nodes.append(sp())
    nodes.append(p('じゃあ、距離感が違うふたりはうまくいかないのか？'))
    nodes.append(sp())
    nodes.append(p('そんなことはありません。'))
    nodes.append(sp())
    nodes.append(p('大事なのは、「私はこれくらいの距離感が心地いいんだよね」って伝えること。'))
    nodes.append(sp())
    nodes.append(p('そして相手の「僕はこう感じるんだ」も聴くこと。'))
    nodes.append(sp())
    nodes.append(p('そうやって話してみると、「あ、嫌われてたんじゃなかったんだ」「面倒だと思ってたわけじゃないんだ」って、誤解がすーっと溶けていくんです。'))
    nodes.append(sp())

    if url_conversation:
        nodes.append(image_node(url_conversation, '「私はね」「僕はね」——その一言が、誤解を溶かしていく'))
        nodes.append(sp())

    nodes.append(p('実は私の友人ご夫婦は、お二人ともNLPを学んでいらっしゃるんですが、「今からひとりにしてほしい」ということをお互いに言えるし、「この時間は一緒に過ごそう」というすり合わせもしている。'))
    nodes.append(sp())
    nodes.append(p('一緒に過ごす時間は近くのカフェに行くとか、環境もちゃんと切り分けているんですよね。'))
    nodes.append(sp())
    nodes.append(p('コミュニケーション学で言えば、これは「メタ・コミュニケーション」——コミュニケーションの取り方自体について話し合うこと。'))
    nodes.append(sp())
    nodes.append(p_bold('「何を話すか」じゃなくて「どう関わるか」をふたりで決められる関係って、すごく強いんです。'))
    nodes.append(sp())

    # section 6: beyond dating
    nodes.extend(section('これは婚活だけの話じゃない'))
    nodes.append(sp())
    nodes.append(p('この"距離感の違い"を知っておくと、交際中だけじゃなくて結婚生活でもずっと役立ちます。'))
    nodes.append(sp())
    nodes.append(p('お子さんが生まれたとき、その子の距離感のタイプが自分と違うこともあるんですよね。'))
    nodes.append(sp())
    nodes.append(p('「うちの子、全然甘えてこない」と心配するお母さんもいれば、「ずっとべったりで自分の時間がない」と疲れてしまうお母さんもいる。'))
    nodes.append(sp())
    nodes.append(p('でも知っていれば、「この子はそういうタイプなんだな」とわかる。'))
    nodes.append(sp())
    nodes.append(p('それだけで子育ての悩みも減るし、パートナーとの関係も、お子さんとの関係も、ずっと心地よくなっていきます。'))
    nodes.append(sp())

    # hope landing
    nodes.append(p('婚活は、ふたりの未来のしくみを一緒につくっていく作業です。'))
    nodes.append(sp())
    nodes.append(p('「この人のこと好きなのに、なんか違和感がある」——それは嫌いになったんじゃなくて、距離感がずれているだけかもしれません。'))
    nodes.append(sp())
    nodes.append(p('ぴんとこなくても大丈夫。相談してみてください。'))
    nodes.append(sp())
    nodes.append(p('こういった無意識の行動傾向の違いで、交際がうまくいかないように感じているだけ——そんなケースを、私はたくさん見てきました。'))
    nodes.append(sp())
    nodes.append(p('お互いにとって心地よい、自分らしくいられる環境づくりを、最初から一緒につくっていきましょう。'))
    nodes.append(sp())

    # CTA
    nodes.append(cta_node())

    return {"nodes": nodes}


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
        print(f"draft creation failed: {r.status_code} {r.text[:300]}")
        return None
    return r.json().get("draftPost", {}).get("id")


def update_excerpt_related(post_id):
    body = {
        "draftPost": {
            "excerpt": EXCERPT,
            "relatedPostIds": RELATED_POST_IDS,
        },
        "fieldMask": "excerpt,relatedPostIds"
    }
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{post_id}",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"excerpt/related PATCH failed: {r.status_code} {r.text[:300]}")
    return r.ok


def update_seo(post_id):
    body = {
        "draftPost": {
            "seoData": {
                "tags": [{
                    "type": "meta",
                    "props": {"name": "description", "content": SEO_DESC},
                    "children": ""
                }]
            }
        },
        "fieldMask": "seoData"
    }
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{post_id}",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"seoData PATCH failed: {r.status_code} {r.text[:300]}")
    return r.ok


def main():
    print("=== metaprogram distance article ===\n")

    urls = []
    for img in IMAGE_PROMPTS:
        url = generate_and_upload_image(img["prompt"], img["filename"])
        urls.append(url)

    url_eyecatch     = urls[0]
    url_solo         = urls[1]
    url_conversation = urls[2]

    print("\n[building richContent...]")
    rich_content = build_nodes(url_eyecatch, url_solo, url_conversation)

    print("\n[creating Wix draft...]")
    post_id = create_draft(rich_content)
    if not post_id:
        print("failed.")
        return

    print(f"  -> draft ID: {post_id}")

    print("\n[updating excerpt & related posts...]")
    ok = update_excerpt_related(post_id)
    print(f"  -> {'ok' if ok else 'failed'}")

    print("\n[updating SEO description...]")
    ok = update_seo(post_id)
    print(f"  -> {'ok' if ok else 'failed'}")

    print(f"\ndone!\ndraft ID: {post_id}")
    print("check Wix blog dashboard.")
    print("check that images display correctly.")


if __name__ == "__main__":
    main()
