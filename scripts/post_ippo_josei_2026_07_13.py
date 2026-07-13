"""
【女性向け】"一人で踏み出すのが怖い"人ほど、実は婚活がうまくいく。
カテゴリ: 無料相談の前に読む(641187e4-a409-4c2f-9639-ecc548f26f15)
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
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む
]

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "8e779610-2acc-448e-b6b0-ad65dbb418d1",  # 無料相談
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "1571190e-c478-41bd-89b7-aa88c9747b98",  # 決断できない
]

RELATED_POST_IDS = [
    "19d45af3-381f-45b0-8f38-a9449c47addf",  # こんな私でも大丈夫？婚活を始める前の不安に答えます。
    "ef922c0a-d808-4a03-aef8-c9be3c9c66b5",  # 20年後の幸せな自分から、今日の婚活へのメッセージ
    "14ec5353-eba7-4b05-88fa-16d99fd521d1",  # 受け身をやめたら、半年でご成婚できた話。
]

TITLE   = "【女性向け】\"一人で踏み出すのが怖い\"人ほど、実は婚活がうまくいく。"
EXCERPT = "「動いたほうがいいのかも」と思いながら、一人で始めるのが怖くて足が止まっている。その怖さは弱さじゃなく、脳の自然な反応です。愛媛・松山の結婚相談所カウンセラーが、一歩を後押ししてくれる存在の大切さについて綴ります。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft morning lighting, East Asian appearance, black hair, "
            "beautiful Japanese woman in her 30s, elegant refined features, model-like appearance, clear skin, "
            "soft neutral elegant outfit, standing at a bright open doorway or large window, one hand gently "
            "resting on the frame, looking outward with a hopeful and slightly nervous smile, warm morning light "
            "streaming in, symbolizing a first step forward, clean bright modern atmosphere, shallow depth of "
            "field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-13_ippo_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft daylight, East Asian appearance, black hair, "
            "beautiful Japanese woman in her 30s, elegant refined features, model-like appearance, clear skin, "
            "sitting alone at a bright cafe table with a calm, content expression, two coffee cups on the table "
            "one across from her suggesting companionship, an open notebook and pen beside her, soft warm "
            "sunlight, clean bright modern atmosphere, shallow depth of field, professional lifestyle "
            "photography, no text"
        ),
        "filename": "2026-07-13_ippo_support.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft morning light, East Asian appearance, black hair, "
            "a Japanese couple in a bright modern kitchen on a weekend morning, both in casual comfortable "
            "clothing, laughing together while making coffee, warm genuine connection, candid natural moment, "
            "clean bright modern atmosphere, shallow depth of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-13_ippo_future.png",
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

    nodes.append(p("でね、今日は無料相談にいらしてくださった方とのお話から、感じたことを書きたいんです。"))
    nodes.append(sp())

    if url1:
        nodes.append(image_node(url1, "その一歩は、決して小さなものじゃありません。"))
        nodes.append(sp())

    nodes.append(p("先日、お友達と一緒に無料相談にお越しくださった方がいました。"))
    nodes.append(p("「このままでは少し心配」「そろそろ動いた方がいいのかもしれない」——そう感じて、実際に連絡をくださって、足を運んでくださった。"))
    nodes.append(p("その一歩、決して小さなものじゃないんですよね。"))
    nodes.append(p("私はそう思っています。"))
    nodes.append(sp())
    nodes.append(p("お話を伺いながら感じたのは、婚活をしたくないわけじゃないんだ、ということでした。"))
    nodes.append(p("一人で始めることや、よくわからない世界に踏み出すことに、不安を感じていらっしゃるだけなんです。"))
    nodes.append(sp())

    nodes.extend(section("不安は「性格」じゃなくて「反応パターン」"))
    nodes.append(sp())
    nodes.append(p("人には、今の状態を変えることを怖いと感じて、慣れた場所にとどまろうとする心の働きがあります。"))
    nodes.append(p("右利きの人が急に左手で箸を持つように言われたら、悪いことじゃなくても、最初はぎこちなくて落ち着かない気持ちになりますよね。"))
    nodes.append(p("それと同じです。"))
    nodes.append(sp())
    nodes.append(p("これ、自分を守るために必要な働きでもあるんです。"))
    nodes.append(p("でも、大切な場面で一歩を止めてしまうこともある。"))
    nodes.append(p("だから知っておいてほしいんです。"))
    nodes.append(p_bold("不安は、あなたの性格が弱いからじゃありません。ただの反応パターンです。"))
    nodes.append(sp())

    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("「そろそろ動いた方がいいのかな」と思いながら、半年、一年と時間だけが過ぎている。"))
    nodes.append(p("婚活サイトや相談所のページを開いては閉じる、を何度も繰り返している。"))
    nodes.append(p("周りに相談しようとしても、「一人で決めなきゃ」という気持ちが先に立って、結局誰にも言えないままでいる。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section("なぜ、今は「一人で決める」がこんなに重いのか"))
    nodes.append(sp())
    nodes.append(p("実はこれ、あなただけの問題じゃないんです。"))
    nodes.append(sp())
    nodes.append(p("脳の仕組みから言うと、扁桃体という部分は、よく知らないもの・経験したことのないものを、一時的に「危険」として判定しやすい性質を持っています。"))
    nodes.append(p("婚活という、多くの人にとって未知の世界に足を踏み入れようとするとき、体がブレーキをかけるのは、ごく自然な反応なんですよね。"))
    nodes.append(sp())

    if url2:
        nodes.append(image_node(url2, "隣に、伴走してくれる人がいるだけで。"))
        nodes.append(sp())

    nodes.append(p("社会学の世界では、現代の結婚を「親密性の変容」という視点で語ることがあります。"))
    nodes.append(p("かつては、親戚やご近所の世話焼きさんが間に入って、お相手を探すところから話を進めるところまで、一緒に背負ってくれていました。"))
    nodes.append(p("でも今は、出会いから決断まで、ほとんどすべてを一人で背負う時代になっています。"))
    nodes.append(p("だから「一人で決めなきゃ」というプレッシャーは、昔よりずっと重くなっている。"))
    nodes.append(p_bold("あなたの気持ちが弱いからではなく、時代の構造そのものが、決断を一人に背負わせやすくなっているんです。"))
    nodes.append(sp())
    nodes.append(p("心理学には「安全基地」という考え方があります。"))
    nodes.append(p("人は、安心して戻れる場所や、頼れる誰かがそばにいると感じられるときほど、新しい世界に踏み出す勇気を持てる、というものです。"))
    nodes.append(p("子どもが知らない場所を探検できるのは、後ろを振り返ればお母さんがいるとわかっているからなんですよね。"))
    nodes.append(p("婚活も同じで、隣に伴走してくれる人がいるだけで、一人で立ち向かうときとは踏み出しやすさが全然違うんです。"))
    nodes.append(sp())

    nodes.extend(section("一人で頑張らなくていい、その先にあるもの"))
    nodes.append(sp())
    nodes.append(p("これまで一人ではなかなか動き出せなかったのなら、これからは一人で頑張らなくてもいいんじゃないでしょうか。"))
    nodes.append(sp())
    nodes.append(p("婚活の進め方を一緒に考え、迷ったときには相談でき、落ち込んだときにも支えてくれる。"))
    nodes.append(p("そのために、私たち仲人というプロの伴走者がいます。"))
    nodes.append(p("当相談所では、ただお相手をご紹介するだけでなく、最初に「変わることへの怖さ」や「傷つくことへの不安」を少しずつ緩めながら、あなたのペースで進めていくことも大切にしています。"))
    nodes.append(sp())
    nodes.append(p("婚活そのものを急ぐ必要はありません。"))
    nodes.append(p("焦ってお相手を決める必要もありません。"))
    nodes.append(sp())
    nodes.append(p("けれど、スタートだけは、あまり先送りにしてほしくないなと思っています。"))
    nodes.append(p("「もう少し考えてから」と悩んでいるうちに、半年、一年と時間が過ぎてしまうことは、本当に珍しくないんです。"))
    nodes.append(p("今この瞬間は、これからの人生を変えるために使える、いちばん若い時間ですから。"))
    nodes.append(sp())
    nodes.append(p("費用のことも、正直に触れておきますね。"))
    nodes.append(p("決して小さな金額ではないので、迷われるお気持ちはよくわかります。"))
    nodes.append(p("ただ、これは単に「出会いを探すためのお金」ではなくて、これから先の人生を一緒に支え合える方と出会い、そのご縁を育てていくためのサポートへの費用なんです。"))
    nodes.append(sp())

    if url3:
        nodes.append(image_node(url3, "休みの日の朝、二人分のコーヒーを淹れる音が聞こえてくる。"))
        nodes.append(sp())

    nodes.append(p("5年後、10年後に、大切な人と笑い合いながら暮らしている未来と、「あのとき始めておけばよかった」と感じる未来。"))
    nodes.append(p("休みの日の朝、二人分のコーヒーを淹れる音がキッチンから聞こえてくる、そんな景色を思い浮かべながら、ご自身にとって価値があるかどうかを、一度考えてみてくださいね。"))
    nodes.append(sp())
    nodes.append(p("無理におすすめするつもりはありません。"))
    nodes.append(p_bold("ただ、あなたの中にある「変わりたい」という気持ちを、また不安の中に戻してしまうのは、少しもったいないなと感じています。"))
    nodes.append(sp())

    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、婚活について一人で抱えている不安を、紙に3行だけ書き出してみてください。"))
    nodes.append(p("誰かに見せなくていいんです。"))
    nodes.append(p("まず、自分の中から言葉として外に出してみる。"))
    nodes.append(p("それだけで、今週の一歩としては十分です。"))
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
    print('=== "一人で踏み出すのが怖い"人ほど、実は婚活がうまくいく 投稿スクリプト ===\n')

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
