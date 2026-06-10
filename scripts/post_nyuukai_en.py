"""
入会して1ヶ月で旅立っていく男性たちの、不思議で必然な理由 — Wix下書き投稿スクリプト
カテゴリ: 無料相談の前に読む / 結婚相談所の始め方
2026-06-10
"""
import os, re, time, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む
    "0122d61b-14c6-42d9-a950-d4b527ea39d1",  # 結婚相談所の始め方
]

TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "7b67d846-ad80-46b5-8e46-f8302f486c0b",  # 波動
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "4e730deb-5ff8-414c-a0ea-7fcde43eb113",  # 新規ご入会
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
]

RELATED_POST_IDS = [
    "488657cb-6e61-4104-b88d-d146349fd377",  # 言えなかった本音の疑問
    "f3e9966d-dda6-44cd-8f08-58187f3349c9",  # 見た目を変えたら（男性向け）
    "19d45af3-381f-45b0-8f38-a9449c47addf",  # こんな私でも大丈夫？
]

TITLE   = "入会して1ヶ月で旅立っていく男性たちの、不思議で必然な理由"
EXCERPT = "入会してすぐ退会される男性がいます。実はご縁がつながったんです。なぜそうなるのか。密教の「身口意」×コミットメント効果×脳のRAS×グラノベッター理論で、結婚相談所に入会する「だけで」ご縁が動き始める不思議で必然な理由をお伝えします。"
SEO_DESC = "入会してすぐ退会？実はご縁がつながったんです。密教の「身口意」×心理学×物理学×社会学で読み解く、結婚相談所に入会することで起きる内側と外側の変化。なぜ入会の決断がご縁を引き寄せるのか、心理カウンセラー仲人が解説します。"

IMAGE_PROMPTS = [
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural daylight, East Asian appearance, no text. "
            "A Japanese man in his 30s wearing a crisp dark suit, standing tall with a calm and determined expression, "
            "looking forward with quiet confidence. Clean modern urban background, "
            "professional lifestyle photography style."
        ),
        "filename": "2026-06-10_nyuukai_en_eyecatch.png",
        "caption": "",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural daylight, East Asian appearance, no text. "
            "A Japanese man in his 30s at a stylish barber shop, getting his hair styled with care, "
            "smiling slightly with a sense of fresh confidence and new beginning. "
            "Clean bright modern interior, professional lifestyle photography style."
        ),
        "filename": "2026-06-10_nyuukai_en_grooming.png",
        "caption": "身だしなみを整えることが、内側の変化を呼び起こす",
    },
    {
        "prompt": (
            "Photorealistic, cinematic quality, natural daylight, East Asian appearance, no text. "
            "A Japanese man and woman meeting naturally outdoors on a sunny city street, "
            "both with warm natural smiles, a genuine connection forming between them. "
            "Black hair, the man in smart casual attire, the woman in a soft elegant dress. "
            "Bright cheerful atmosphere."
        ),
        "filename": "2026-06-10_nyuukai_en_encounter.png",
        "caption": "準備が整った人のもとに、ご縁はやってくる",
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
    # static.wixstatic.com URLをそのまま使う（wix:image://形式は表示されないため）
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


def build_nodes(img_eyecatch=None, img_grooming=None, img_encounter=None):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # イントロ
    nodes.append(p("今日は男性の皆さんへ、ちょっと不思議な話をしようと思います。"))
    nodes.append(sp())
    nodes.append(p("実はですね、当相談所に入会してくださったあと、ご自身でお申し込みをする間もなく、1ヶ月ほどで退会される男性の方がちらほりいらっしゃるんです。"))
    nodes.append(sp())
    nodes.append(p("「え、うまくいかなかったのかな…」と思いますよね。"))
    nodes.append(sp())
    nodes.append(p("違うんです（笑）。"))
    nodes.append(sp())
    nodes.append(p("ご友人からご紹介があったり、何年も前から知っている方から急にアプローチされたり。長年の知り合いだった方との距離が急に縮まったり。そういうご縁が、なぜか入会直後に動き出すケースがけっこうあって。"))
    nodes.append(sp())
    nodes.append(p("こちらとしては「ぜひ一緒に活動したかったなぁ」という正直な気持ちはあります（笑）。でも同時に、「ああ、またか。やっぱりそうなるよなぁ」という感覚もあって。"))
    nodes.append(sp())
    nodes.append(p("今日はその「なぜそうなるのか」を、私なりに考えてみたことをお伝えしたいと思います。"))
    nodes.append(sp())

    if img_eyecatch:
        nodes.append(image_node(img_eyecatch["url"], ""))
        nodes.append(sp())

    # セクション1
    nodes.extend(section("「入る」と決めた瞬間に、何かが動き始めている"))
    nodes.append(sp())
    nodes.append(p("結婚相談所への入会を決断するとき、その瞬間に何が起きているか、考えたことはありますか？"))
    nodes.append(sp())
    nodes.append(p("「まぁ、婚活始めてみるか」という軽い気持ちの方もいれば、「もう本気でやらないと」と覚悟を決めた方もいる。でもどんな形であれ、「結婚する」という方向に、自分のエネルギーと意図が向いたということですよね。"))
    nodes.append(sp())
    nodes.append(p("密教では「身口意（しんくい）」という言葉があります。体と言葉と心、この三つが揃ったとき、人は本当に変化すると言われています。入会の決断は、その「意（こころ）」の部分にあたる。"))
    nodes.append(sp())
    nodes.append(p("面白いのは、心理学の世界でもこれが証明されているんですよね。人は何かを「決めた」瞬間から、それと一致した行動をとりやすくなる。これを「コミットメント効果」といいます。「自分は結婚に向かって動いている人間だ」という自己定義が、行動と認識を自然と塗り替えていく。"))
    nodes.append(sp())
    nodes.append(p("さらに言うと、脳の中には「RAS（網様体賦活系）」という機能があります。意識を向けたものに関連する情報だけをフィルタリングして、意識上に浮かび上がらせる仕組みです。新しい車を買ったら急に街中でその車が目につくようになる、あの感覚です。"))
    nodes.append(sp())
    nodes.append(p("「結婚相手を探している」というアンテナが立った瞬間から、脳が「良縁に関係する情報」を選んで届けてくれるようになる。今まで気づかなかった誰かの存在が、急に目に入ってくるわけです。"))
    nodes.append(sp())

    # セクション2
    nodes.extend(section("写真撮影が「体」を変えていく"))
    nodes.append(sp())
    nodes.append(p("入会が決まると、まずプロフィール写真の撮影予約を入れます。"))
    nodes.append(sp())
    nodes.append(p("このとき、ただ撮ればいいだけじゃないんですよね。「女性が見てくれる写真」だと思うと、やっぱり気が引き締まって。髪を整える。ひげを整える。眉毛もきれいにする。撮影用のスーツを用意する。立ち姿、表情、どこかすっきりした、凛とした顔になっていく。"))
    nodes.append(sp())
    nodes.append(p("これが「身（からだ）」の変容です。"))
    nodes.append(sp())
    nodes.append(p("外側が変わると、内側も変わります。人はふさわしい格好をしているとき、ふさわしいふるまいをしようとする。これは「エンボディメント（身体化認知）」と呼ばれる心理現象で、服装や姿勢が思考や行動に影響を与えることが、多くの研究で確認されています。"))
    nodes.append(sp())
    nodes.append(p("すっきりした顔つき、背筋の伸びた立ち姿。それが日常になっていくと、周囲の人はちゃんとそれを感じ取っています。"))
    nodes.append(sp())

    if img_grooming:
        nodes.append(image_node(img_grooming["url"], img_grooming.get("caption", "")))
        nodes.append(sp())

    # セクション3
    nodes.extend(section("プロフィール文が「言葉」で未来を形づくる"))
    nodes.append(sp())
    nodes.append(p("次にプロフィール文を一緒に作ります。"))
    nodes.append(sp())
    nodes.append(p("過去を振り返り、今の仕事や趣味や生活を言葉にして、そしてパートナーとともにどんな未来を作りたいかを書いていく。"))
    nodes.append(sp())
    nodes.append(p("これが「口（ことば）」の部分です。"))
    nodes.append(sp())
    nodes.append(p("未来を言葉にするって、単なる自己紹介文じゃないんですよね。「私はこういう未来を生きる」という宣言になっている。言語化することで、脳はその状態をより鮮明にイメージできるようになって、「素晴らしいパートナーとともにいる自分」が、じわじわと内側に刻まれていく。"))
    nodes.append(sp())
    nodes.append(p("量子力学の世界には「観察者効果」という概念があります。観察すること自体が、対象の状態に影響を与えるという話です。もちろんそのまま人間関係に当てはめるわけにはいかないけれど、「意識を向けた方向に現実が動く」という感覚は、物理学の世界でも語られていることだったりします。"))
    nodes.append(sp())

    # セクション4
    nodes.extend(section("身口意が揃ったとき、「その人」は変わる"))
    nodes.append(sp())
    nodes.append(p("意が決まって、身が整って、口が未来を語り出す。この三つが揃ってくると、不思議なことが起きます。"))
    nodes.append(sp())
    nodes.append(p("頭の中でメンタルリハーサルが始まるんです。「どんなデートをしようか」「どんな話をしようか」。無意識のうちに、良い出会いに向けて自分を整え始めている。いつお見合いが来てもいいように。いつデートになってもいいように。"))
    nodes.append(sp())
    nodes.append(p("その状態の人って、なんというか、すっきりしているんです。自信がある、というより「腹が決まっている」感じ。変に力が入っていないけど、ちゃんと前を向いている。"))
    nodes.append(sp())
    nodes.append(p("社会学者のグラノベッターは「弱い絆の強さ」という理論の中で、日常的に強いつながりのある人よりも、少し距離のある知人・友人の方が、新しい情報や出会いをもたらしやすいと示しました。相談所に入ったことを周囲に話していなくても、たたずまいや言葉の変化として、なんとなく伝わっていく。そうして「なんかあの人、最近いいな」と思った誰かが、動き出すんじゃないかと思うんです。"))
    nodes.append(sp())

    if img_encounter:
        nodes.append(image_node(img_encounter["url"], img_encounter.get("caption", "")))
        nodes.append(sp())

    # セクション5
    nodes.extend(section("「不思議」じゃなくて、必然なのかもしれない"))
    nodes.append(sp())
    nodes.append(p("入会してすぐに良縁がつながる男性たちを見ていると、「不思議だなぁ」と思う一方で、「必然だよなぁ」とも感じます。"))
    nodes.append(sp())
    nodes.append(p("心が決まって、体が整って、言葉が未来を描く。その状態の人にご縁が寄ってくるのは、当然と言えば当然で。結婚相談所に入会するという行為は、単なる「手続き」じゃなくて、自分の内側と外側を、結婚という未来に向けて一斉に動かすきっかけなんですよね。"))
    nodes.append(sp())
    nodes.append(p("もちろん、相談所の中でお相手を一緒に探してくださることが私の本来の役目ではあります（笑）。でも、こんなふうに入会の決断そのものが人を変えていくのを見るたびに、「一歩踏み出すことの力」って本物だなぁと感じます。"))
    nodes.append(sp())
    nodes.append(p("今、悩んでいる方にお伝えするとしたら、「完璧な準備ができてから」じゃなくていい。決めること、それだけで何かが動き始めます。"))
    nodes.append(sp())

    # CTA（中央寄せ）
    nodes.append(cta_node())

    return nodes


def main():
    # Step 1: 画像3枚を生成・アップロード
    img_eyecatch = generate_and_import_image(IMAGE_PROMPTS[0]["prompt"], IMAGE_PROMPTS[0]["filename"])
    img_grooming  = generate_and_import_image(IMAGE_PROMPTS[1]["prompt"], IMAGE_PROMPTS[1]["filename"])
    if img_grooming:
        img_grooming["caption"] = IMAGE_PROMPTS[1]["caption"]
    img_encounter = generate_and_import_image(IMAGE_PROMPTS[2]["prompt"], IMAGE_PROMPTS[2]["filename"])
    if img_encounter:
        img_encounter["caption"] = IMAGE_PROMPTS[2]["caption"]

    # Step 2: richContent構築
    nodes = build_nodes(
        img_eyecatch=img_eyecatch,
        img_grooming=img_grooming,
        img_encounter=img_encounter,
    )

    # Step 3: 下書き作成（本文・タグ・カテゴリ・関連記事・抜粋）
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

    # Step 4: カバー画像をPATCH（fieldMask: "media" — coverMediaではなくmedia）
    if img_eyecatch and draft_id:
        print("[Wix] カバー画像をPATCH中...")
        patch_media = {
            "draftPost": {
                "media": {
                    "wixMedia": {
                        "image": {
                            "id": img_eyecatch["id"],
                            "url": img_eyecatch["url"],
                        }
                    },
                    "displayed": True,
                    "custom": False,
                }
            },
            "fieldMask": "media"
        }
        rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
                            headers=wix_headers(), json=patch_media, timeout=30)
        print("カバー画像PATCH完了" if rp.ok else f"カバー画像PATCH失敗: {rp.status_code} {rp.text[:200]}")

    # Step 5: SEOディスクリプションをPATCH（カバーと分けて送る）
    if draft_id:
        print("[Wix] SEOディスクリプションをPATCH中...")
        patch_seo = {
            "draftPost": {
                "seoData": {"description": SEO_DESC}
            },
            "fieldMask": "seoData.description"
        }
        rs = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
                            headers=wix_headers(), json=patch_seo, timeout=30)
        print("SEO PATCH完了" if rs.ok else f"SEO PATCH失敗: {rs.status_code} {rs.text[:200]}")

    print(f"\n✅ 完了！")
    print(f"下書きID: {draft_id}")
    print(f"タイトル: {TITLE}")
    print(f"\n⚠️  投稿後に確認してください:")
    print(f"  - 記事内の画像が正しく表示されているか")
    print(f"  - カバー画像が設定されているか")
    print(f"  - SEOフォーカスキーワードを手動で設定する（Wixエディター）")


if __name__ == "__main__":
    main()
