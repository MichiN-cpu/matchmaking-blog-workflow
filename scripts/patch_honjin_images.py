"""
「言えなかった本音の疑問、ぜんぶ受け取ります。」
下書きID: 488657cb-6e61-4104-b88d-d146349fd377
→ 画像3枚挿入 + タグ設定 + メタ説明
"""
import os, re, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
DRAFT_ID    = "488657cb-6e61-4104-b88d-d146349fd377"

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "e9832229-ecaf-435f-98ec-6d3470a13cd4",  # 結婚相談所
    "a8fd177f-b3ba-4a57-9f81-c26ba1ec0488",  # 婚活相談
    "8e779610-2acc-448e-b6b0-ad65dbb418d1",  # 無料相談
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
]

SEO_DESCRIPTION = "「モテない人が行くとこ？」「打算的では？」「負けみたいで嫌」——結婚相談所への言えなかった本音の疑問に、仲人が笑いながら正直に答えます。"

BASE_STYLE = (
    "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
    "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
    "real-world setting, professional lifestyle photography style, "
    "shallow depth of field, clean bright modern atmosphere, no text"
)

IMAGE_PROMPTS = [
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A Japanese woman in her late 20s sitting alone at a desk, looking thoughtfully at something "
            "with a slightly skeptical but curious expression, holding a pen, soft window light. "
            "Clean minimal desk setting, white and neutral tones."
        ),
        "filename": "2026-05-30_honjin_img1.png",
    },
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A close-up of two coffee cups on a bright white cafe table, soft morning light, "
            "cozy and warm atmosphere suggesting a comfortable conversation space. "
            "No people visible, clean and inviting."
        ),
        "filename": "2026-05-30_honjin_img2.png",
    },
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A happy Japanese couple in their late 20s to early 30s walking together outdoors, "
            "smiling and relaxed, bright natural light, green park background softly blurred. "
            "Joyful and natural atmosphere."
        ),
        "filename": "2026-05-30_honjin_img3.png",
    },
]

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

def q(text):
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

def generate_and_upload(prompt_text, filename):
    print(f"  gpt-image-1 生成中: {filename}")
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
    file_obj = ru.json().get("file", {})
    url = file_obj.get("url", "")
    if not url:
        print(f"  URL取得失敗")
        return None
    print(f"  完了: {url[:70]}...")
    return {"url": url}

def build_nodes(imgs):
    img1, img2, img3 = imgs[0], imgs[1], imgs[2]
    n = []

    n.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    n.append(sp())
    n.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    n.append(sp())
    n.append(p("「気になってるんだけど、なんか言いにくくて」"))
    n.append(sp())
    n.append(p("「こんなこと聞いたら失礼かな」"))
    n.append(sp())
    n.append(p("そういう本音の質問、全部受け取ります（笑）。思ってることを正直に聞いてくれるほうが、私は嬉しいです。"))
    n.append(sp())

    if img1:
        n.append(image_node(img1)); n.append(sp())

    n.extend(heading_block("「結婚相談所って…そういうとこでしょ？」"))
    n.append(q("Q. 結婚相談所って、自然な出会いで選ばれなかった人が行くとこじゃないですか？"))
    n.append(sp())
    n.append(p("正直に言ってくれてありがとうございます（笑）。そのイメージ、すごくよくわかります。でも実際に来ている方を見ていると、「モテないから来た」じゃなくて「出会う場所がない・時間がない・職場や友人に異性がいない」という現実的な理由が圧倒的に多いんですよ。医師、教師、エンジニア、看護師……仕事一筋で来てしまった方ばかりです。「選ばれない」んじゃなくて「そもそも出会いの機会がない」、まったく別の話です。"))
    n.append(sp())
    n.append(q("Q. 結婚相談所で出会ったって、友達に言えない気がします。"))
    n.append(sp())
    n.append(p("わかります！でも最近、かなり変わってきていますよ。「マッチングアプリで出会った」が普通になったように、「結婚相談所で出会った」も全然珍しくなくなってきています。それに、幸せになってしまえばどこで出会ったかなんて関係ない。「この人と結婚できてよかった」が、全部を上回ります。"))
    n.append(sp())
    n.append(q("Q. 結婚相談所に入る人って、「早く結婚したい」と焦ってる人ばかりじゃないの？"))
    n.append(sp())
    n.append(p("焦っている方もいれば「ちゃんと考えて決めたい」という方もいます。むしろ「流れで付き合ってなんとなく結婚するのが嫌だ」という、結婚をしっかり考えているからこそ来る方が多い印象です。焦りより「丁寧に選びたい」という意識の方が多いですよ。"))
    n.append(sp())

    if img2:
        n.append(image_node(img2)); n.append(sp())

    n.extend(heading_block("「愛とか好きとか、どうなるの？」"))
    n.append(q("Q. 条件で相手を選ぶって、なんか打算的で嫌です。"))
    n.append(sp())
    n.append(p("すごく真剣に考えている方がおっしゃるんですよね。でも「条件」って本来、「この人とどんな生活を送りたいか」の言語化なんです。収入・居住地・家族観——それって打算じゃなくて、将来の生活を想像しているということ。フィーリングだけで決めて「こんなはずじゃなかった」となるより、ずっと誠実な選び方だと思っています。"))
    n.append(sp())
    n.append(q("Q. 好きでもない人と結婚するの？愛のない結婚になりそう。"))
    n.append(sp())
    n.append(p("「好きから始まらなくていい」という考え方、知っていますか？結婚相談所での出会いは、最初から「ドキドキの恋愛感情」より「この人は誠実だな、一緒にいると安心するな」というところから始まることが多い。でも結婚生活って、むしろそっちのほうが長続きするんですよ。最初のドキドキより、積み重ねた信頼のほうがずっと深い愛になります。"))
    n.append(sp())
    n.append(q("Q. 条件で選んだ相手が、本当に自分のことを好きなのかわからない。"))
    n.append(sp())
    n.append(p("これ、実はアプリや自然な出会いでも同じ不安があると思うんですよね（笑）。結婚相談所の場合は、お互い「結婚を前提に会っている」という真剣さが保証されています。「好きになれるか試す」場所じゃなくて「一緒に生きていける人を探す」場所。それが結婚相談所です。"))
    n.append(sp())
    n.append(q("Q. 結婚相談所で結婚した人って、本当に幸せなんですか？"))
    n.append(sp())
    n.append(p("正直に言います——幸せな方、たくさん見てきました。「この人じゃなかったら出会えなかった」「婚活して本当によかった」とおっしゃる方ばかりです。しっかり考えて選んだ分、覚悟が決まっている。出会い方より、選び方と向き合い方のほうが幸せに影響します。"))
    n.append(sp())

    n.extend(heading_block("「婚活=負け」じゃないよ、という話"))
    n.append(q('Q. 「婚活している」と認めると、なんか自分が"負け"みたいな気がします。'))
    n.append(sp())
    n.append(p("その感覚、めちゃくちゃわかります。でも婚活って「勝ち負け」じゃなくて「行動」なんですよ。欲しいものに向かって動くのは、かっこいいことだと思っています。負けじゃなくて、むしろ一番まともな判断です。"))
    n.append(sp())
    n.append(q("Q. 入会しても成婚できなかったら、お金だけ消えますよね？"))
    n.append(sp())
    n.append(p("そのリスクはゼロじゃないです、正直に言います。だからこそ「どう活動するか」が大事で、それをサポートするのが仲人の仕事です。費用対効果を最大にするために、私もガチで伴走します。"))
    n.append(sp())
    n.append(q("Q. 結婚相談所って、高い人だけが使えるもの？庶民には無理？"))
    n.append(sp())
    n.append(p("「思ったよりかかった」という声と「思ったより現実的だった」という声、半々です（笑）。少なくともあすなる愛媛は「払える範囲でちゃんとサポートを受けられること」を大切にしています。料金は無料相談でぜんぶお伝えしますので、まず聞きにいらしてください。"))
    n.append(sp())

    if img3:
        n.append(image_node(img3)); n.append(sp())

    n.append(p("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan"))

    return n

def main():
    print("=" * 50)
    print("「言えなかった本音の疑問」画像追加スクリプト")
    print("=" * 50)

    imgs = []
    for i, info in enumerate(IMAGE_PROMPTS, 1):
        print(f"\n[画像{i}/3]")
        result = generate_and_upload(info["prompt"], info["filename"])
        imgs.append(result)

    if any(img is None for img in imgs):
        print("\n⚠️ 一部の画像生成に失敗しました。")

    print("\nrichContent + タグ + メタ説明をPATCH中...")
    nodes = build_nodes(imgs)
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}",
        headers=wix_headers(),
        json={
            "draftPost": {
                "richContent": {"nodes": nodes, "metadata": {"version": 1}},
                "tagIds": TAG_IDS,
                "seoData": {"description": SEO_DESCRIPTION},
            },
            "fieldMask": "richContent,tagIds"
        },
        timeout=30,
    )
    if r.ok:
        print("PATCH完了 ✅")
    else:
        print(f"PATCH失敗: {r.status_code} {r.text[:300]}")
        return

    # カバー画像 displayed:true
    cover_url = "https://static.wixstatic.com/media/e6bbff_d6a9cf480ad640699ff6c3ac1ecc2293~mv2.png"
    m = re.search(r"/media/([^?#\s]+)", cover_url)
    cover_id = m.group(1) if m else ""
    rc = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}",
        headers=wix_headers(),
        json={"draftPost": {"media": {
            "custom": True, "displayed": True,
            "wixMedia": {"image": {"id": cover_id, "url": cover_url, "height": 1024, "width": 1536, "filename": "2026-04-29_qa3_eyecatch.png"}}
        }}, "fieldMask": "media"},
        timeout=30,
    )
    print("カバー画像更新" + (" ✅" if rc.ok else f" 失敗({rc.status_code})"))
    print(f"\n✅ 完了！下書きID: {DRAFT_ID}")

if __name__ == "__main__":
    main()
