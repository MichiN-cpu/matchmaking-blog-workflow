"""
【男性向け】「なんでできないんだろう」を卒業する。
婚活で最後まで進める男性と、途中で心が折れる男性を分けるたった1つの言葉
カテゴリ: 30代婚活(男女・悩み別)(ce3b3deb-a05e-4093-a1a3-aa657693da8d)
下書き保存のみ(公開日時未定)
"""
import os, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["ce3b3deb-a05e-4093-a1a3-aa657693da8d"]  # 30代婚活(男女・悩み別)

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
    "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
    "a3a015e3-7f09-4a9f-b5c4-2c59a74bac7c",  # 自己肯定感
]

RELATED_POST_IDS = [
    "a795be5b-c16c-4fed-9d55-1623b103fa25",  # 「結婚はまだ先でいい」と思っていた男性たちが、後から気づいたこと
    "fc81155c-09b4-4e31-9530-b0ff5f90e27f",  # 「苦手でも、諦めなかった。」30代医療職男性の成婚ストーリー
    "49bc08d5-9927-48c8-a37a-9124b0c43fce",  # 婚活がうまくいく人は行動より先に"あるもの"を変えている
]

TITLE   = "「なんでできないんだろう」を卒業する。婚活で最後まで進める男性と、途中で心が折れる男性を分けるたった1つの言葉"
EXCERPT = "婚活が最後までうまくいく男性と、途中で心が折れてしまう男性。その違いは、自分にかける「たった1つの言葉」でした。脳科学・心理学の視点から、結果を変えるセルフトークの力をお伝えします。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft daylight, East Asian appearance, "
            "Japanese man in his 30s, neat smart casual clothing, standing at a path that splits "
            "in two directions in a quiet park, thoughtful determined expression looking ahead, "
            "clean bright modern atmosphere, shallow depth of field, professional lifestyle "
            "photography, no text"
        ),
        "filename": "2026-07-11_selftalk_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "Japanese man in his 30s, neat business casual, sitting at a bright cafe table writing "
            "in a notebook with a calm confident expression, morning sunlight through a window, "
            "clean modern atmosphere, shallow depth of field, professional lifestyle photography, "
            "no text"
        ),
        "filename": "2026-07-11_selftalk_notebook.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft light, East Asian appearance, "
            "Japanese man in his 30s, neat smart casual clothing, walking forward confidently on a "
            "bright open street, gentle hopeful smile looking ahead, clean bright modern city "
            "atmosphere, shallow depth of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-11_selftalk_forward.png",
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

    nodes.append(p("婚活って、結局のところ相手があることなんですよね。"))
    nodes.append(p("だから、何もかも自分の思い通りの人とお見合いをして、思い通りの交際をして、思い通りにご成婚まで進む、なんてことは基本ありえません。"))
    nodes.append(p("現実的に考えれば、そうですよね。"))
    nodes.append(sp())
    nodes.append(p("それでも人は「こんなふうになりたいな」っていう理想を思い描いて、何かを始めるものです。"))
    nodes.append(p("それは婚活に限った話じゃなくて、学校生活でもサークル活動でも、就職活動でも、恋愛でも、趣味でも同じです。"))
    nodes.append(sp())
    nodes.append(p("そうすると、思い描いた未来予想図と、実際に一歩一歩歩んでいくプロセスとの間には、必ずギャップが生まれます。"))
    nodes.append(p("これは、どんな人であっても避けられません。"))
    nodes.append(p("どんなに賢い人も、どんなにお金持ちの人も、どんなにイケメンの人も、どんなに友達に恵まれている人であっても、全てが全て思い通りに進むということはないんです。"))
    nodes.append(p("道に迷ったり、遠回りしたり、間違った選択をしたりすることが、誰にでもあります。"))
    nodes.append(sp())
    nodes.append(p("じゃあ、その中で最終的に結果を手にする人と、そうでない人の違いは何なのか。"))
    nodes.append(p_bold("突き詰めれば、それは「自分にかける言葉」の違いなんじゃないかと、私は思っています。"))
    nodes.append(sp())

    if url1:
        nodes.append(image_node(url1, "分かれ道で、自分に何と声をかけるか。"))
        nodes.append(sp())

    nodes.extend(section("「なんでできないんだろう」が脳に与える指令"))
    nodes.append(sp())
    nodes.append(p("結果が出るまで歩めない人は、うまくいかない時にこんな言葉を自分にかけていることが多いんです。"))
    nodes.append(p("「なんでできないんだろう」って。"))
    nodes.append(sp())
    nodes.append(p("一方で、紆余曲折しながらも歩み続けられる人、最終的にゴールにたどり着く人の多くは、こんな問いを自分に投げかけています。"))
    nodes.append(p("「どうしたらできるんだろう」って。"))
    nodes.append(sp())
    nodes.append(p("この違い、実は脳の使い方として理にかなっています。"))
    nodes.append(p("脳の中には網様体賦活系(RAS)という、入ってくる情報の中から「今フォーカスしているもの」に関連する情報だけを優先的に拾い上げる仕組みがあります。"))
    nodes.append(sp())
    nodes.append(p("「なんでできないんだろう」と問いかけると、脳は\"できない理由\"を探すよう指令を受けたことになり、見た目、話し方、学歴、収入、趣味、思考のクセ、苦手意識、経験のなさ……できない理由なんて、探せば無限に見つかります。"))
    nodes.append(p("そうして自信をなくし、「もう無理だ」という結論に至ったり、「良い人がいないから」と自分以外に理由を見つけて終わってしまったりするんです。"))
    nodes.append(sp())
    nodes.append(p("これは心理学でいう確証バイアスにも重なります。"))
    nodes.append(p("人は自分が立てた問いや前提を裏付ける情報ばかりを集めてしまう傾向がある、というものです。"))
    nodes.append(sp())

    nodes.extend(section("「どうしたらできるんだろう」に変えると何が起こるか"))
    nodes.append(sp())
    nodes.append(p("一方、「どうしたらできるんだろう」と自分に問いかけると、思考の土台そのものが「できる前提」に変わります。"))
    nodes.append(p("頭の働きの方向性が、そもそも違うんですよね。"))
    nodes.append(sp())
    nodes.append(p("誰に聞いたらできるかな。どこに行けばできるかな。誰と一緒ならできるかな。"))
    nodes.append(p("何を手に入れたら、何を手放したらできるかな。いつならできるかな、いつはやめておいた方がいいかな。"))
    nodes.append(p("どんな手段や工夫を使えばバージョンアップできるかな。うまくいっている人はどうやっているんだろう——。"))
    nodes.append(sp())
    nodes.append(p("そんなふうに、「できる前提」のアンテナが広がっていくと、何かしらの答えが見つかり、何かしらバージョンアップして、経験を積み重ねながら結果まで進んでいけるようになります。"))
    nodes.append(sp())
    nodes.append(p("これは、心理学者キャロル・ドゥエックが提唱した「成長マインドセット」の考え方にも通じています。"))
    nodes.append(p("能力や状況を固定的なものと捉えるのではなく、「今はまだできていないだけ」と捉えて工夫を重ねられる人ほど、長期的に結果を出しやすいという研究です。"))
    nodes.append(p("スポーツ心理学の世界でも、トップアスリートほど自分にかける言葉(セルフトーク)を意識的にコントロールしていることが知られています。"))
    nodes.append(p_bold("婚活も、ある意味では自分自身のメンタルとの長期戦なんですよね。"))
    nodes.append(sp())

    if url2:
        nodes.append(image_node(url2, "「どうしたらできるんだろう」と書き出してみる。"))
        nodes.append(sp())

    nodes.extend(section("こんなこと、心当たりはありませんか"))
    nodes.append(sp())
    nodes.append(p("お見合いが決まらない時、「どうせ自分には」と思ってしまう。"))
    nodes.append(p("交際が停滞した時、「なんで自分だけうまくいかないんだろう」と考えてしまう。"))
    nodes.append(p("うまくいかない理由を、自分の見た目や条件のせいにしてしまう。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるかも」と思った方は、今日から自分にかける言葉を少しだけ変えてみてください。"))
    nodes.append(sp())

    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("もし今、「うまくいかないなぁ」「自分に自信がないなぁ」「どうせ自分にはダメだろう」という思考のクセ、セルフトークのクセがあるんだったら、今すぐそこを変えてみる。"))
    nodes.append(p("それだけで、結果を手にするスピードは大きく変わってくるはずです。"))
    nodes.append(sp())
    nodes.append(p_bold("これは婚活だけの話じゃありません。人生のあらゆる場面で、きっと得をする考え方です。"))
    nodes.append(sp())

    if url3:
        nodes.append(image_node(url3, "「どうしたらできるんだろう」で、一歩を踏み出す。"))
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
    print("=== 「なんでできないんだろう」を卒業する 投稿スクリプト ===\n")

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
