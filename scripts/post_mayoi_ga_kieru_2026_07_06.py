"""
【女性向け】迷いが消えていく人は、実は"最悪"を先に決めている。
カテゴリ: 真剣交際（5414dab5-ded7-4b15-a88a-d679d6fd3c71）
下書き保存のみ（公開日時未定）
"""
import os, uuid, base64, requests, time
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = ["5414dab5-ded7-4b15-a88a-d679d6fd3c71"]  # 真剣交際

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "0ddde006-b527-4852-8056-8cdb87174e82",  # 真剣交際
    "c249fe67-ef22-410a-a395-309db2116a0b",  # 結婚
    "25417c41-e15f-4447-8e02-1e9b7ff48aec",  # 受け身
]

RELATED_POST_IDS = [
    "c24ea7ec-7798-4cb9-a240-cf0ee30cd479",  # 仮交際→真剣交際のドキドキが怖いあなたへ
    "8b815244-5096-4f80-8dac-e0b0545a03f4",  # 夫婦の中に「3人の自分」がいる
    "b2fc6e44-29f2-40e4-be6c-4604c4ffeed4",  # 【女性向け】彼の親への初挨拶で失敗しない
]

TITLE   = '【女性向け】迷いが消えていく人は、実は"最悪"を先に決めている。'
EXCERPT = "「本当にこの人でいいのかな」その不安、性格のせいじゃないんです。気がかりを全部書き出して、自分主体の対処ルートを作っておくだけで、心の揺れは驚くほど静かになります。愛媛・松山の結婚相談所が伝える不安との付き合い方。"
SEO_DESC = EXCERPT

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman in her 30s, elegant refined features, clear skin, "
            "sitting alone at a wooden desk writing in a notebook, calm contemplative expression, "
            "warm afternoon light through a window, clean bright modern room, "
            "shallow depth of field, professional lifestyle photography, no text"
        ),
        "filename": "2026-07-06_mayoi_eyecatch.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, "
            "close-up of a neatly prepared emergency bag placed by the entrance of a modern Japanese apartment, "
            "symbolic of quiet readiness and calm, no people, no text, "
            "clean bright modern atmosphere, shallow depth of field, professional photography"
        ),
        "filename": "2026-07-06_mayoi_bousai.png",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural soft morning lighting, East Asian appearance, "
            "beautiful Japanese woman with elegant refined features, model-like appearance, clear skin, "
            "Japanese couple in their 30s, facing each other, having a relaxed meal together at home, "
            "warm gentle smiles, looking at each other not at camera, "
            "clean bright modern kitchen interior, shallow depth of field, "
            "professional lifestyle photography, no text"
        ),
        "filename": "2026-07-06_mayoi_hope.png",
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

    nodes.append(p("でね、今日は「本当にこの人でいいのかな」「結婚しちゃって大丈夫かな」っていう、あの独特の不安について話したいんです。"))
    nodes.append(sp())
    nodes.append(p("真剣交際が進んで、周りからも「おめでとう」って言われ始めて。なのに、夜になるとふと胸のあたりがザワザワする。これ、私自身も経験があるんです（笑）。あんなに自分で選んだ人なのに、なんでこんなに不安になるんだろうって、当時は本気で悩みました。"))
    nodes.append(sp())
    nodes.append(p("結論から言いますね。この不安、あなたの性格が弱いからでも、相手を選び間違えたサインでもありません。"))
    nodes.append(sp())

    if url1:
        nodes.append(image_node(url1, "不安は、書き出すことで輪郭がはっきりする。"))
        nodes.append(sp())

    nodes.extend(section("不安は「性格」じゃなくて「反応パターン」"))
    nodes.append(sp())
    nodes.append(p("人って、右利きの人が箸を左手に持ち替えるとすごく不自由に感じるように、慣れた反応の仕方が体に染みついているんですよね。"))
    nodes.append(sp())
    nodes.append(p_bold("大きな決断の前になると不安になる、というのも実はその人の「慣れた反応パターン」のひとつなんです。性格の欠陥じゃなくて、ただの癖。"))
    nodes.append(sp())
    nodes.append(p("癖なら、扱い方を知れば軽くできます。"))
    nodes.append(sp())
    nodes.append(p("こんなこと、心当たりはありませんか。"))
    nodes.append(sp())
    nodes.append(p("彼のちょっとした一言が引っかかって、何日も頭から離れない。友達の惚気話を聞くたびに、自分の選択と比べて不安になる。将来のことを考えようとすると、頭が真っ白になって考えるのをやめてしまう。"))
    nodes.append(sp())
    nodes.append(p("——どれか一つでも「あるある」と思った方は、このあとの話、きっと役に立ちます。"))
    nodes.append(sp())

    nodes.extend(section("まず、不安を\"正体不明\"のままにしない"))
    nodes.append(sp())
    nodes.append(p("こういう不安って、ぼんやりしたまま抱えているのが一番しんどいんです。正体が見えない霧の中を歩いているような感じ、わかりますか。"))
    nodes.append(sp())
    nodes.append(p_bold("だから最初にやってほしいのは、頭の中の気がかりを、ひとつ残らず紙に書き出すこと。"))
    nodes.append(sp())
    nodes.append(p("「なんとなく不安」で止めずに、「具体的に何が不安なのか」まで分解するんです。"))
    nodes.append(sp())
    nodes.append(p("住む場所のこと。出産後、自分のキャリアがどうなるか。彼の家族との関係。金銭感覚の違い。将来、彼の親の介護がどうなるか。——思いつく限り、全部です。"))
    nodes.append(sp())
    nodes.append(p("ここで大事な話をしますね。日本には今もまだ、女性が男性の人生設計に「担がれる」形で結婚するという風潮が根強く残っています。住む場所も、出産後の働き方も、気づけば相手の都合や相手の会社の転勤に合わせて決まっていく。"))
    nodes.append(sp())
    nodes.append(p("これ自体が悪いわけじゃないんです。でも、それを\"自分で選んだ\"んじゃなくて\"気づいたらそうなっていた\"という受け身の姿勢で迎えてしまうと、結婚後もずっと「自分の人生を人に委ねる」感覚が続いてしまうんですよね。"))
    nodes.append(sp())
    nodes.append(p("社会学の世界では、これを「個人化」という視点で説明することがあります。現代は本来、誰もが自分の人生を自分で設計する時代のはずなのに、結婚や家庭という枠に入った瞬間だけ、女性は無意識に主体性を手放しやすい構造が残っている、という指摘です。"))
    nodes.append(sp())
    nodes.append(p_bold("だからこそ、意識して自分の手に主導権を戻す作業が必要なんです。"))
    nodes.append(sp())

    nodes.extend(section("気がかり一つひとつに、「自分主体の対処ルート」を作る"))
    nodes.append(sp())
    nodes.append(p("書き出した気がかりを、今度は一つずつ見ていきます。「もしこうなったら、私はこうする」という、自分が主語の行動ルートを作るんです。"))
    nodes.append(sp())
    nodes.append(p("例えば「彼の転勤についていくかどうか」が気がかりなら、「もし転勤の話が出たら、まず自分のキャリアの選択肢を先に調べる。そのうえで、行くか行かないか、いつまでに決めるかを話し合う」というふうに。"))
    nodes.append(sp())
    nodes.append(p("ここでのポイントは、相手の出方を待つ文章にしないことです。「彼がこう言ったら、私はこうなる」ではなくて、「私はこうする」で終わらせる。主語を自分に戻す練習だと思ってください。"))
    nodes.append(sp())
    nodes.append(p("心理学では、これに近い効果を持つ手法として「筆記開示」というものが知られています。頭の中でぐるぐるしている不安を紙に書き出すだけで、コルチゾール(ストレスホルモン)の分泌が落ち着き、心身の負担が軽くなることが研究でわかっているんです。"))
    nodes.append(sp())
    nodes.append(p("書くという行為そのものに、不安を鎮める力があるんですね。"))
    nodes.append(sp())
    nodes.append(p("そして、この作業を通して「これは彼に伝えておいたほうがいいな」と思うものが出てきたら、そこはちゃんと言葉にして伝えてください。全部を一人で抱え込む必要はありません。二人で決めていいこともたくさんあります。"))
    nodes.append(sp())

    if url2:
        nodes.append(image_node(url2, "備えがあるだけで、日常の不安は静かになる。"))
        nodes.append(sp())

    nodes.extend(section("最後の一線だけは、誰にも言わなくていい"))
    nodes.append(sp())
    nodes.append(p("ここまで書き出して、彼に伝えるべきことは伝えた。それでもなお残る「これだけはどうしても譲れない」という一線——これについては、あえて誰にも言わないという選択をおすすめしています。"))
    nodes.append(sp())
    nodes.append(p_bold("相手が何と言おうと、相手の家族が何と言おうと、自分の家族が何と言おうと、「こうなったら、私はこうする」という覚悟だけは、自分の心の中にそっとしまっておくんです。"))
    nodes.append(sp())
    nodes.append(p("口に出さなくていい。誰かに承認してもらう必要もない。ただ、自分の中でだけ、決めておく。"))
    nodes.append(sp())
    nodes.append(p("これ、防災グッズの考え方に似ているなと思うんです。「災害が起きたら、この荷物を持って、あそこに逃げる」——そう決めているだけで、災害が起きるかどうかに関係なく、日々の心の落ち着きが全然違いますよね。"))
    nodes.append(sp())
    nodes.append(p("何も準備していない状態だと、漠然とした不安がずっと続く。でも「最悪こうなっても、私はこうする」という一つの答えを持っているだけで、気持ちがふっと軽くなるんです。"))
    nodes.append(sp())
    nodes.append(p("心理学的にも、これは「統制感(コントロール感)」と呼ばれるものに近い働きをします。何が起こるかは自分では選べなくても、「起きたときの自分の動き方」を自分で決めているという感覚が、日常の安心感を大きく支えてくれるんですよね。"))
    nodes.append(sp())

    nodes.extend(section("覚悟を持った人ほど、実は身軽に婚活を楽しめる"))
    nodes.append(sp())
    nodes.append(p("不思議なもので、「最悪の場合はこうする」という覚悟を自分の中に持っている人ほど、日々の婚活や交際そのものは肩の力が抜けて、楽しめるようになるんです。"))
    nodes.append(sp())
    nodes.append(p("だって、逃げ道も、譲れない一線も、もう自分の中で決まっているから。目の前の彼との時間に、安心して集中できる。彼のちょっとした言葉に一喜一憂することも減って、「今日、一緒にごはん食べられて嬉しいな」って、ただその瞬間を味わえるようになる。"))
    nodes.append(sp())
    nodes.append(p("不安を全部書き出して、対処ルートを作って、最後の覚悟だけ静かに心にしまう。この一連の作業を終えた人は、婚活という時間そのものが、じんわりと軽やかなものに変わっていきます。"))
    nodes.append(sp())

    if url3:
        nodes.append(image_node(url3, "覚悟を決めた人ほど、目の前の時間を安心して味わえる。"))
        nodes.append(sp())

    nodes.extend(section("今週の一歩"))
    nodes.append(sp())
    nodes.append(p("今日、紙とペンを用意して、頭の中にある気がかりを5個だけ書き出してみてください。全部じゃなくていいんです。まず5個。それだけで、霧が少し晴れます。"))
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


def create_tag(label):
    r = requests.post(
        f"{WIX_BASE}/blog/v3/tags",
        headers=wix_headers(),
        json={"label": label},
        timeout=30,
    )
    if not r.ok:
        print(f"タグ作成失敗 ({label}): {r.status_code} {r.text[:200]}")
        return None
    tag_id = r.json().get("tag", {}).get("id")
    print(f"  新規タグ作成: {label} → {tag_id}")
    return tag_id


def main():
    print("=== 迷いが消えていく人は実は最悪を先に決めている 投稿スクリプト ===\n")

    print("[タグ作成中...]")
    new_tag = create_tag("不安")
    if new_tag:
        TAG_IDS.append(new_tag)

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
