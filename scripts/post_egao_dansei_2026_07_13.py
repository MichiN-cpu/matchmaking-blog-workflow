"""
【男性向け】"話が面白いのに、なぜか伝わらない"男性へ。笑顔ひとつで、婚活は動き出します。
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
    "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "f2b2bc0c-b1c1-497a-aca8-dff56712cbc6",  # 成婚エピソード
]

RELATED_POST_IDS = [
    "490faf91-c89f-489e-82ef-3d757165afea",  # 笑顔が、婚活を変える。
    "58079daf-693b-48bd-b4e0-9bfcc0ae918d",  # 腕を開いて座れる男性が、婚活も家庭も制す。
    "6ae51a61-7db6-4510-b865-f026ec1700fa",  # お見合いで仕事の苦労話をしていませんか？
]

TITLE   = "【男性向け】\"話が面白いのに、なぜか伝わらない\"男性へ。笑顔ひとつで、婚活は動き出します。"
EXCERPT = "話が面白くて気配りもできるのに、なぜかデートが続かない。その原因は話の内容じゃなく「表情」かもしれません。愛媛・松山の結婚相談所カウンセラーが、非言語コミュニケーションとNLPの視点から解説します。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
            "a Japanese man in a neat dark suit with dress shirt sitting across from a Japanese woman in a "
            "soft pink elegant dress at a quiet cafe table, facing each other, looking at each other not at "
            "camera, the man speaking with a genuinely warm bright smile and an expressive open hand gesture, "
            "the woman smiling back at ease and relaxed, clean bright modern atmosphere, shallow depth of "
            "field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-13_egao_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft daylight, East Asian appearance, black hair, "
            "a Japanese man in smart casual business attire at a convenience store counter, receiving a small "
            "item from a store clerk's hand just out of frame, giving a genuine warm smile while saying thank "
            "you, candid everyday moment, clean bright modern atmosphere, shallow depth of field, professional "
            "lifestyle photography, no text"
        ),
        "filename": "2026-07-13_egao_practice.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft golden hour lighting, East Asian appearance, "
            "black hair, a Japanese man and woman walking together outdoors, both laughing genuinely at the "
            "same time, warm relaxed connection, casual smart clothing, clean bright atmosphere, shallow depth "
            "of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-13_egao_future.png",
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

    nodes.append(p("でね、今日は少し前にご成婚退会された男性会員さんの、印象的な変化のお話をしたいんです。"))
    nodes.append(sp())

    if url1:
        nodes.append(image_node(url1, "笑顔ひとつで、伝わり方はこんなに変わります。"))
        nodes.append(sp())

    nodes.append(p("とても知的で、話も面白くて、気配りもできる方でした。"))
    nodes.append(p("会話をしていて本当に楽しい方だったんですよね。"))
    nodes.append(p("でも、婚活を始めてしばらく経った頃、私はあることに気づいたんです。"))
    nodes.append(p("——笑顔が少ない。表情の動きが、思っている以上に少ないんです。"))
    nodes.append(sp())
    nodes.append(p("もしかしたらこれ、以前の婚活がうまくいかなかった理由の一つだったんじゃないか。"))
    nodes.append(p("私はそう思いました。"))
    nodes.append(sp())

    nodes.extend(section("「話の内容」より先に「伝わり方」が効いている"))
    nodes.append(sp())
    nodes.append(p("女性って、共感力が高かったり、相手の気持ちを思いやることに長けている方が多いんですよね。"))
    nodes.append(p("だからこそ、無意識に相手の言葉以外の情報——表情や声のトーン、身振り——にとても敏感なんです。"))
    nodes.append(sp())
    nodes.append(p("だから、楽しい内容の話をしていても、表情が真顔だったり、声のトーンに抑揚がなかったりすると、その非言語の情報を無意識にキャッチしてしまいます。"))
    nodes.append(p("頭では「楽しい話をしてもらっている」とわかっていても、潜在意識のほうが安心できない。"))
    nodes.append(p("楽しい話と、表情の乏しさ。"))
    nodes.append(p_bold("この不一致感を、なんとなく「この人への違和感」として勘違いしてしまうんですよね。"))
    nodes.append(sp())
    nodes.append(p("とても知的で、言語力も高くて、楽しい話をしているはずなのに、なぜか一緒に楽しめない。"))
    nodes.append(p("そんな女性が出てきてしまう。"))
    nodes.append(p("本人も気づいていない、なんとなくの違和感。それに気づいたのは、私が近くでずっと見ていたからだと思います。"))
    nodes.append(sp())

    nodes.extend(section("人には\"優位感覚\"がある"))
    nodes.append(sp())
    nodes.append(p("NLPの世界には「優位感覚」という考え方があります。"))
    nodes.append(p("人は五感すべてを使って相手を理解しようとしていますが、その中でも特によく使う、優位な感覚を持っているんです。"))
    nodes.append(sp())
    nodes.append(p("大きく分けると、視覚優位・聴覚優位・体感覚優位の3つ。"))
    nodes.append(p("視覚優位の方は、目に見える情報からの影響をとても強く受けます。"))
    nodes.append(p("話の内容そのものより、見た目・見た印象で理解し、決断していく方なんですね。"))
    nodes.append(sp())

    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("デートの後、楽しかったはずなのに、なぜか次に繋がらない。"))
    nodes.append(p("話の内容には自信があるのに、なぜか「面白みがない人」だと思われている気がする。"))
    nodes.append(p("もらう感想はいつも「話しやすい人」止まりで、「一緒にいてドキドキした」とは言われない。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.append(p("視覚優位の女性からすれば、楽しい話をしているはずなのに、その方が「楽しそうに見えない」。"))
    nodes.append(p("聴覚優位の方なら話の内容から楽しさを感じ取ってくれるかもしれませんが、視覚優位の方には、表情や身振りという「見えるもの」の影響力のほうが大きいんです。"))
    nodes.append(sp())

    nodes.extend(section("表情も声のトーンも、実は\"癖\""))
    nodes.append(sp())
    nodes.append(p("ここで大事なことをお伝えしたいんです。"))
    nodes.append(p_bold("笑顔が少ないのは、性格が冷たいからでも、愛情が薄いからでもありません。ただの表現の\"癖\"なんです。"))
    nodes.append(sp())
    nodes.append(p("人には、慣れた表現の仕方が体に染みついています。"))
    nodes.append(p("右利きの人が急に左手で箸を持つように言われたら、悪いことじゃなくても、最初はぎこちなく感じますよね。"))
    nodes.append(p("表情や声の抑揚も同じで、これまで使ってこなかった動かし方をするのは、最初は誰でも慣れないものなんです。"))
    nodes.append(p("性格の問題じゃなくて、ただの癖。癖なら、練習で変えられます。"))
    nodes.append(sp())

    if url2:
        nodes.append(image_node(url2, "小さな場面で、まずにこっと。"))
        nodes.append(sp())

    nodes.append(p("私はその男性会員さんに、正直にお伝えしました。"))
    nodes.append(p("もしかしたら笑顔が少ない、あるいは表情の表現が小さいために、あなたの気持ちが伝わっていないかもしれません。"))
    nodes.append(p("一緒にいて楽しい、一緒にいて嬉しい、デートができて幸せ——その思いが、もしかしたら全く伝わっていないどころか、真逆に「つまらなそう」と受け取られている可能性さえありますよ、と。"))
    nodes.append(sp())

    nodes.extend(section("行動レベルの練習と、根っこからの変化"))
    nodes.append(sp())
    nodes.append(p("とはいえ、「彼女に会ったときにニコニコしろ」と言われても、急には難しいですよね。"))
    nodes.append(p("だから私がお願いしたのは、日常の中に小さな練習を仕込むことでした。"))
    nodes.append(sp())
    nodes.append(p("職場での朝の挨拶や、名前を呼ばれて返事をするとき。"))
    nodes.append(p("何かを頼まれたり、尋ねられたりしたとき。"))
    nodes.append(p("コンビニで店員さんから商品を受け取って「ありがとう」と言うとき。"))
    nodes.append(p("そういう小さな場面のたびに、まず、にこっとしてから対応する。"))
    nodes.append(p("意識しなくても、ちょいちょい笑顔が出るような癖づけを、日々の中で積み重ねていく練習です。"))
    nodes.append(sp())
    nodes.append(p("それと合わせて、話の内容に合わせて身振りや表情を、自分では大げさに感じるくらい動かしてみること。"))
    nodes.append(p("声のトーンやリズムも、ゆっくりにしたり早くしたり、力強くしたり優しくしたりと、内容に合わせて抑揚をつけていくこと。"))
    nodes.append(p("この二つをお願いしました。"))
    nodes.append(sp())

    if url3:
        nodes.append(image_node(url3, "だんだんそれが自然になっていって。"))
        nodes.append(sp())

    nodes.append(p("だんだんそれが自然になっていって、デートのときも心から楽しんでいらっしゃったようです。"))
    nodes.append(p("お相手の女性も、安心して関係を深めていかれて、スムーズにご成婚に進まれました。"))
    nodes.append(sp())
    nodes.append(p("心理学の世界には、ミラーニューロンという神経細胞の働きが知られています。"))
    nodes.append(p("人は、相手の表情を見るだけで、自分の脳内にも同じような感情の動きが起こるようにできているんです。"))
    nodes.append(p("あなたが笑えば、相手の中にも小さな安心が生まれる。"))
    nodes.append(p_bold("表情は、伝えるための道具じゃなくて、相手の中に感情を起こす装置でもあるんですよね。"))
    nodes.append(sp())

    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、誰かに名前を呼ばれたときか、お店で店員さんに「ありがとう」と言うとき、一瞬でいいので、にこっと微笑んでみてください。"))
    nodes.append(p("それだけで十分です。"))
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
    print('=== "話が面白いのに、なぜか伝わらない"男性へ 投稿スクリプト ===\n')

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
