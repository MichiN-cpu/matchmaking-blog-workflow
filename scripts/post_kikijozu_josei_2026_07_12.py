"""
【女性向け】「聞き上手」をやめたら、うまくいく。誠実な女性ほど陥る"聞き役"の罠
カテゴリ: お見合い(5089ac63-e2ce-4de1-b472-3512a77401af) / 仮交際(3f5f378d-a4f4-47e0-90a7-ab4daa27504e)
下書き保存のみ(公開日時未定)
"""
import os, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "5089ac63-e2ce-4de1-b472-3512a77401af",  # お見合い
    "3f5f378d-a4f4-47e0-90a7-ab4daa27504e",  # 仮交際
]

TAG_IDS = [
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "1c7a4d95-e95b-492a-93e2-da1c8a63ab9b",  # デート
]

RELATED_POST_IDS = [
    "ffcc121d-6384-4392-ac96-e7c75f424cf2",  # 「気がきく女子」をお休みしてみない？ポンコツ女子のすすめ
    "490faf91-c89f-489e-82ef-3d757165afea",  # 笑顔が、婚活を変える
    "64073f78-40d4-4695-ad8c-053ae2ff910e",  # 向かい合って話すだけがデートじゃない
]

TITLE   = "「聞き上手」をやめたら、うまくいく。誠実な女性ほど陥る\"聞き役\"の罠"
EXCERPT = "聞き上手な女性ほど、お見合いやデートで陥りやすい罠があります。相槌上手なあなたを見て、男性は「これでいい」と誤解し、喋り続ける悪循環に。コミュニケーション学・心理学の視点から、流れを変えるコツをお伝えします。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
            "beautiful Japanese woman with elegant refined features, model-like appearance, clear skin, "
            "soft pink elegant dress, hair down with gentle blow-dried wave, sitting across from a Japanese "
            "man in a neat dark suit with dress shirt at a quiet cafe table, facing each other, looking at "
            "each other not at camera, the man speaking animatedly with an expressive hand gesture, the "
            "woman listening with a warm polite smile, clean bright modern atmosphere, shallow depth of "
            "field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-12_kikijozu_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman in her 30s, elegant refined features, model-like appearance, clear "
            "skin, soft neutral elegant blouse, sitting at a bright cafe table, speaking with a confident "
            "open expression and a gentle hand gesture, engaged and relaxed posture, clean bright modern "
            "atmosphere, shallow depth of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-12_kikijozu_speak.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft daylight, East Asian appearance, black hair, "
            "beautiful Japanese woman with elegant refined features, model-like appearance, clear skin, "
            "sitting together with a Japanese man in smart casual clothing at an outdoor cafe table, both "
            "laughing and talking animatedly at the same time, warm genuine connection, clean bright modern "
            "atmosphere, shallow depth of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-12_kikijozu_laugh.png",
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


def build_nodes(url1, url2, url3):
    nodes = []

    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    nodes.append(p("聞き上手な女性って、本当に多いんですよね。"))
    nodes.append(p("相槌のタイミングも絶妙で、表情も態度も「あなたの話、ちゃんと聞いてますよ」って伝わってくる。"))
    nodes.append(p("誠実で、思いやりがあって、素敵な資質だと思います。"))
    nodes.append(sp())
    nodes.append(p_bold("でも、その聞き上手さが、お見合いやデートの場では、実はちょっとした罠になることがあるんです。"))
    nodes.append(sp())

    if url1:
        nodes.append(image_node(url1, "彼はどんどん話し、彼女はにこにこ聞いている。"))
        nodes.append(sp())

    nodes.extend(section("なぜ男性はじゃんじゃん喋ってしまうのか"))
    nodes.append(sp())
    nodes.append(p("男性って、気に入った女性を目の前にすると、まるで孔雀のオスが美しい羽を広げるように、どんどん喋り続けてしまうことがあります。"))
    nodes.append(p("理由は主に2つ。"))
    nodes.append(p("ひとつは、自分を知ってもらいたい、無自覚に自分をアピールしたいという気持ち。"))
    nodes.append(p("もうひとつは、「会話を続けて女性を楽しませなきゃ」という誤解です。"))
    nodes.append(p("場を持たせなきゃ、と思えば思うほど、じゃんじゃん話し続けてしまうんですよね。"))
    nodes.append(sp())

    nodes.extend(section("聞き上手な女性が陥る罠"))
    nodes.append(sp())
    nodes.append(p("——ここで、聞き上手な女性の出番です。"))
    nodes.append(sp())
    nodes.append(p("相槌が上手で、表情も態度もすごく良いお話を聞いているように振る舞える。"))
    nodes.append(p("それ自体は素晴らしいことなんですが、その様子を見た男性は「これでオッケーなんだ」「うまくいっているんだ」と誤解してしまいます。"))
    nodes.append(p_bold("そして、さらに喋り続ける——という悪循環が生まれるんです。"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("気づいたら1時間、ずっと聞き役に回っていた。"))
    nodes.append(p("デートの帰り道、「今日、私何を話したっけ」と思う。"))
    nodes.append(p("楽しかったはずなのに、なんとなく疲れが残る。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section("会話は、話し手と聞き手の共同作業"))
    nodes.append(sp())
    nodes.append(p("コミュニケーション学の世界には、会話は話し手と聞き手の\"共同作業\"だという考え方があります。"))
    nodes.append(p("相手によって話がどんどん広がったり深まったりすることもあれば、まとまらずに終わることもある。"))
    nodes.append(p("それは、聞き手であるあなたが、思っている以上に会話の流れを作っているということでもあるんです。"))
    nodes.append(sp())
    nodes.append(p("社会学の視点で見ると、「女性は聞き上手であるべき」という無言の規範が、まだ社会の中に根強く残っています。"))
    nodes.append(p("社会学者ホックシールドが指摘した「感情労働」という概念にも近くて、女性のほうが自然と「聞く役割」「場を和ませる役割」を引き受けやすいんですよね。"))
    nodes.append(p("でもそれは、性格の問題ではなく、そう学習してきただけの話。"))
    nodes.append(p_bold("だったら、変えることもできます。"))
    nodes.append(sp())
    nodes.append(p("だから、ずっと聞いてるのが嫌だったら、流れを変えるのはあなたです。"))
    nodes.append(p("女性のリアクション次第で、男性は話を振ったり、聞き手に回ったりできるようになります。"))
    nodes.append(sp())

    nodes.extend(section("「私はね」でいいんです"))
    nodes.append(sp())
    nodes.append(p("その時に大事なのは、「嫌われるんじゃないか」「失礼なんじゃないか」という思いを、一度手放してみることです。"))
    nodes.append(sp())
    nodes.append(p("相手がずっと話してくれて楽だなぁ、ふんふん言っているだけで自分も楽しめている——という方は、それはそれでオッケーです。"))
    nodes.append(p("でも、もし話の流れを変えたい、自分の話も聞いてほしいと思うなら、ポイントはひとつ。"))
    nodes.append(p_bold("自分から積極的に話を拾って、自分の話にしていくことです。"))
    nodes.append(sp())
    nodes.append(p("「私はね」「私のこと聞いて」——それだけでいいんです。"))
    nodes.append(p("男性は基本的に、女性に喜んでほしいと思っています。"))
    nodes.append(p("だから、あなたが何をすれば楽しいのか、どうしてもらったら嬉しいのか伝えれば、まともな男性なら、ちゃんと聞いてくれます。"))
    nodes.append(sp())
    nodes.append(p("「私はね」「僕はね」って、多少割り込みながら盛り上がるくらいで、ちょうどいいんです。"))
    nodes.append(p("心理学でいう自己開示の返報性、つまり、あなたが自分のことを話すほど、相手も自然とあなたに歩み寄ってくるという現象もあります。"))
    nodes.append(sp())

    if url2:
        nodes.append(image_node(url2, "「私はね」その一言から、会話は変わります。"))
        nodes.append(sp())

    nodes.extend(section("結婚生活は、良い子ぶりっこでは続けられません"))
    nodes.append(sp())
    nodes.append(p_bold("結婚生活は、良い子ぶりっこでは続けられません。"))
    nodes.append(sp())
    nodes.append(p("実はこれ、私自身も一度失敗しています。"))
    nodes.append(p("聞き上手なイメージがついてしまったせいで、義理の父が週末になるたびに何時間も私に話し込むようになってしまって……。"))
    nodes.append(p("ある日、とうとう限界がきて、切れてしまったことがあるんです(汗)。"))
    nodes.append(sp())
    nodes.append(p("そうならないために、聞き上手な女性は、適当に聞いてオッケーです。"))
    nodes.append(p("聞かなくてもオッケーです。"))
    nodes.append(p("話を自分で撮っちゃって、好きなことをしゃべっても大丈夫なんです。"))
    nodes.append(sp())

    if url3:
        nodes.append(image_node(url3, "私はね、僕はね、で盛り上がるくらいがちょうどいい。"))
        nodes.append(sp())

    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("そういうことを何とも思わない、あなたの話も喜んで聞いてくれる男性と、幸せな結婚生活を送ってみませんか。"))
    nodes.append(sp())

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
        print(f"下書き作成失敗: {r.status_code} {r.text[:300]}")
        return None
    return r.json().get("draftPost", {}).get("id")


def update_cover(post_id, cover_url):
    file_id = cover_url.split("/media/")[-1] if "/media/" in cover_url else cover_url
    body = {
        "draftPost": {
            "media": {
                "wixMedia": {
                    "image": {
                        "id": file_id,
                        "url": cover_url,
                    }
                },
                "displayed": True,
                "custom": False,
            }
        },
        "fieldMask": "media"
    }
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{post_id}",
        headers=wix_headers(), json=body, timeout=30,
    )
    if not r.ok:
        print(f"カバー画像PATCH失敗: {r.status_code} {r.text[:300]}")
    return r.ok


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
        print(f"excerpt/relatedPosts PATCH失敗: {r.status_code} {r.text[:300]}")
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
        print(f"seoData PATCH失敗: {r.status_code} {r.text[:300]}")
    return r.ok


def main():
    print("=== 「聞き上手」をやめたら、うまくいく 投稿スクリプト ===\n")

    urls = []
    for img in IMAGE_PROMPTS:
        url = generate_and_upload_image(img["prompt"], img["filename"])
        urls.append(url)

    url1, url2, url3 = urls[0], urls[1], urls[2]

    print("\n[richContent構築中...]")
    rich_content = build_nodes(url1, url2, url3)

    print("\n[Wix下書き作成中...]")
    post_id = create_draft(rich_content)
    if not post_id:
        print("失敗。終了します。")
        return

    print(f"  → 下書きID: {post_id}")

    if url1:
        print("\n[カバー画像を設定中...]")
        ok = update_cover(post_id, url1)
        print(f"  → {'成功' if ok else '失敗'}")

    print("\n[excerpt・関連記事を更新中...]")
    ok = update_excerpt_related(post_id)
    print(f"  → {'成功' if ok else '失敗'}")

    print("\n[SEO descriptionを更新中...]")
    ok = update_seo(post_id)
    print(f"  → {'成功' if ok else '失敗'}")

    print(f"\n完了。下書きID: {post_id}")
    print("Wixブログ管理画面で確認してください。")
    print("画像が正しく表示されているか、必ず確認をお願いします。")


if __name__ == "__main__":
    main()
