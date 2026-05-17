"""
同居をお願いする前に——アラカン婚活男性への正直な話 Wix下書き投稿スクリプト
カテゴリ: シニアの婚活
2026-05-17
"""
import os, time, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_IDS = ["a65acc05-b781-4ec9-95d7-66c9daefc19f"]  # シニアの婚活
TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "3a8d9ef3-9a26-4099-8ac8-546957aa1043",  # シニア
    "3c983f3c-50b7-4193-9d37-64a066c45d1c",  # ５０代
]
RELATED_POST_IDS = [
    "e8c323f3-ec33-49f5-83ce-fb994d2a014b",
    "9ef3a363-e67a-44e8-a56e-b1492596dfe6",
    "7c374371-ece7-4888-8bb1-abddd6e62cd7",
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

def link_node(text, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": text,
            "decorations": [{"type": "LINK", "linkData": {
                "link": {"url": url, "target": "BLANK"}
            }}]
        }}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}

def image_node(url, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": url}}, "caption": caption}}

def upload_image_binary(image_bytes, filename):
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "displayName": filename},
        timeout=30,
    )
    if not r.ok:
        print(f"アップロードURL取得失敗: {r.status_code} {r.text[:200]}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        print(f"uploadURL取得失敗: {data}")
        return None
    sep = "&" if "?" in upload_url else "?"
    upload_url_with_fn = f"{upload_url}{sep}filename={filename}"
    headers = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        headers["Authorization"] = upload_token
    ru = requests.put(upload_url_with_fn, data=image_bytes, headers=headers, timeout=60)
    if not ru.ok:
        print(f"バイナリアップロード失敗: {ru.status_code} {ru.text[:200]}")
        return None
    result = ru.json()
    file_obj = result.get("file", {})
    file_url = file_obj.get("url", "")
    file_id  = file_obj.get("id", "")
    if not file_url:
        print(f"アップロード結果にURLなし: {result}")
        return None
    print(f"アップロード完了: {file_url[:60]}...")
    return {"url": file_url, "id": file_id}

def generate_and_import_image(prompt, filename):
    print(f"画像生成中: {filename}...")
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024",
        quality="medium",
        n=1,
    )
    img_data = resp.data[0]
    print("生成完了。Wixにアップロード中...")
    if img_data.b64_json:
        image_bytes = base64.b64decode(img_data.b64_json)
        return upload_image_binary(image_bytes, filename)
    if img_data.url:
        r = requests.post(
            f"{WIX_BASE}/site-media/v1/files/import",
            headers=wix_headers(),
            json={"url": img_data.url, "displayName": filename, "mimeType": "image/png"},
            timeout=30,
        )
        if not r.ok:
            print(f"インポート失敗: {r.status_code} {r.text[:200]}")
            return None
        data = r.json()
        file_id = (data.get("file") or {}).get("id") or data.get("fileId")
        if not file_id:
            return None
        for i in range(20):
            time.sleep(3)
            chk = requests.get(f"{WIX_BASE}/site-media/v1/files/{file_id}",
                               headers=wix_headers(), timeout=15)
            if chk.ok:
                fd = chk.json().get("file", {})
                if fd.get("state") in ("READY", "OK"):
                    url = fd.get("url", "")
                    print(f"インポート完了: {url[:60]}...")
                    return {"url": url}
    return None

def build_nodes(img1=None, img2=None, img3=None):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # イントロ
    nodes.append(p("今日は、少し正直な話をさせてください。"))
    nodes.append(sp())
    nodes.append(p("アラカン——還暦近くのご年齢で婚活されている男性の中に、ご両親のどちらかと同居されている方がいらっしゃいます。"))
    nodes.append(p("プロフィールには「相談の上で」と書いてあるけれど、本音は「いずれ一緒に住んでほしい」と思っていることが多いんですよね。"))
    nodes.append(sp())
    nodes.append(p("その気持ち、もちろんわかります。大切な親御さんですから。"))
    nodes.append(sp())
    nodes.append(p("でも今日は、そこに正直に向き合っていただきたくて、書いています。"))
    nodes.append(sp())

    # Section 1
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("逆の立場で、一度考えてみてください"))
    nodes.append(sp())
    nodes.append(p("もしあなたが、女性側の親御さんと一緒に暮らさないといけないと言われたら——どうでしょう？"))
    nodes.append(sp())
    nodes.append(p("面識もほとんどない、生活スタイルも価値観も異なる、でも毎日顔を合わせてバランスをとりながら過ごす。"))
    nodes.append(p("そしてその方の介護も、いずれやってくる。"))
    nodes.append(sp())
    nodes.append(p("……想像するだけで、少し重くなりませんか。"))
    nodes.append(sp())
    nodes.append(p("女性たちも、まったく同じ気持ちです。"))
    nodes.append(sp())

    if img1:
        nodes.append(image_node(img1["url"], "逆の立場で考えてみるイメージ"))
        nodes.append(sp())

    # Section 2
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("「相談の上で」は、女性には「同居あり」に見えています"))
    nodes.append(sp())
    nodes.append(p("これが現実なんですよね。"))
    nodes.append(sp())
    nodes.append(p("「相談の上で」と書いてあっても、女性は読み解いています。"))
    nodes.append(p("「いずれ同居を望んでいる方なんだな」と。"))
    nodes.append(sp())
    nodes.append(p("そしてそこで、静かに心が動きます。"))
    nodes.append(p("「一緒に暮らすことになったら、どんな毎日になるだろう」と。"))
    nodes.append(sp())
    nodes.append(p("女性はおしゃべりです（笑）。"))
    nodes.append(p("友人や先輩からの話がリアルに蓄積されています。"))
    nodes.append(p("姑と同居で苦労した話、夫が間に挟まれて頼りなく見えた話、1人になれる時間がなくて限界になった話——そういう話が、女性たちの間では当たり前のように共有されています。"))
    nodes.append(sp())
    nodes.append(p("だから、想像力のハードルが低い。"))
    nodes.append(p("「そうなったとき、自分はどうなるか」がリアルに見えてしまうんです。"))
    nodes.append(sp())
    nodes.append(p("そしてこう思います。"))
    nodes.append(p("「いい人だなと思っても、同居があるなら……。傷つけ合うリスクを取るより、これまで通り1人のほうがマシかもしれない。」と。"))
    nodes.append(sp())

    # Section 3
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("若い頃の同居とは、まったく違います"))
    nodes.append(sp())
    nodes.append(p("若くして結婚して、子どもが生まれて、一緒に孫を育てて——そういう積み重ねの中での同居は、愛着も理解もあります。"))
    nodes.append(p("我慢もできるし、遠慮がなくなってくることもある。"))
    nodes.append(sp())
    nodes.append(p("でも、アラカンでの婚活は違います。"))
    nodes.append(sp())
    nodes.append(p("お互いにすでに長年の生活スタイルがある。"))
    nodes.append(p("夫婦でそれをすり合わせるだけでも、かなりのエネルギーが必要です。"))
    nodes.append(p("そこにさらにもう一人——まったくの初対面に近い方が加わって、その方の意図や気持ちを汲みながら、バランスをとりながら暮らしていく。"))
    nodes.append(sp())
    nodes.append(p("心理学でいう「自律性の欲求」という概念があります。"))
    nodes.append(p("人間は自分のペースで、自分の空間で過ごせる時間がないと、じわじわとストレスが積み上がっていきます（デシとライアン、1985年）。"))
    nodes.append(p("同居という環境は、その自律性を大きく制限する可能性があるんです。"))
    nodes.append(sp())
    nodes.append(p("介護が加わると、もっとです。"))
    nodes.append(sp())

    if img2:
        nodes.append(image_node(img2["url"], "同居のストレスを表すイメージ"))
        nodes.append(sp())

    # Section 4
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("だからこそ、早めの行動が必要です"))
    nodes.append(sp())
    nodes.append(p("「同居をお願いしたら、成婚は難しくなる」と覚悟した上でお願いするなら、それはお気持ちの問題ですから、私には何も言えません。"))
    nodes.append(sp())
    nodes.append(p("でも、少しでも成婚の可能性を広げたいと思っていらっしゃるなら、今すぐできることがあります。"))
    nodes.append(sp())
    nodes.append(p("まず、親御さんがまだお元気なうちに、動いてください。"))
    nodes.append(sp())
    nodes.append(p("「まだ大丈夫」と思っている間が、一番準備しやすいときです。"))
    nodes.append(sp())
    nodes.append(p("具体的には——ケアマネージャーさんに一度相談する、在宅介護サービスの情報を調べる、将来的に施設を利用する選択肢を確認しておく。"))
    nodes.append(p("そういったことを、今からやっておくということです。"))
    nodes.append(sp())

    # Section 5
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("「準備しています」という一言が、女性の心を動かします"))
    nodes.append(sp())
    nodes.append(p("お見合いの場やデートで、万が一「ご両親のことはどのようにお考えですか」と聞かれたとき。"))
    nodes.append(sp())
    nodes.append(p("「まだ考えていないです」という男性と、「ケアマネさんとも相談していて、こういう方向で考えています」という男性——どちらが頼もしく見えるでしょうか。"))
    nodes.append(sp())
    nodes.append(p("家族社会学の観点から言えば、結婚は「2人のシステム」に外部環境をどう取り込むかの設計でもあります。"))
    nodes.append(p("その設計を、すでに始めているかどうかが、女性の安心感に直結します。"))
    nodes.append(sp())
    nodes.append(p("「奥さんに苦労させたくない」「幸せにしたい」「笑顔いっぱいにしてあげたい」という思いがあるなら、その思いを行動で見せてほしいんです。"))
    nodes.append(sp())
    nodes.append(p("婚活の場に出てくる「前に」、もしくは「今すぐに」。"))
    nodes.append(sp())

    if img3:
        nodes.append(image_node(img3["url"], "準備している男性のイメージ"))
        nodes.append(sp())

    # Section 6
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("厳しいことを言ったのは、応援しているからです"))
    nodes.append(sp())
    nodes.append(p("奇跡を待っていても、ナイチンゲールのような天使が現れることはなかなかありません（笑）。"))
    nodes.append(sp())
    nodes.append(p("現実に向き合って、準備して、行動する——その姿勢が、あなたをもっとも魅力的な男性に見せてくれます。"))
    nodes.append(sp())
    nodes.append(p("何か聞かれたときに「こういう対策を考えています」「もう準備しています」と自信を持って答えられる男性は、それだけで女性の信頼をつかみます。"))
    nodes.append(sp())
    nodes.append(p("心から応援しているから、正直にお伝えしました。"))
    nodes.append(sp())

    # CTA（中央寄せ）
    nodes.append(link_node("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"))

    return nodes

def main():
    title   = "「同居をお願いする前に、読んでいただけますか。」——アラカン婚活男性への、正直な話"
    excerpt = "親と同居中のアラカン男性が「相談の上で同居を」と書くと、女性には「ほぼ同居確定」と読まれています。成婚確率への影響と、今すぐできる準備について正直にお伝えします。"
    meta_desc = "親と同居のアラカン婚活男性へ。「相談の上で同居を」は女性にはほぼ同居確定に見えます。成婚確率が大きく下がる理由と、今すぐできる準備を心理カウンセラー仲人が正直にお伝えします。"

    cover = generate_and_import_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A Japanese man in his late 50s sitting alone at a kitchen table, looking thoughtfully at a notebook, "
        "with a warm cup of tea beside him. Soft morning light coming through a window. "
        "Reflective and serious but hopeful atmosphere. No other people in the scene.",
        "2026-05-17_arakan_doukyorei_cover.png"
    )

    img1 = generate_and_import_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A Japanese man in his late 50s sitting across from a Japanese woman at a cafe table, "
        "both looking thoughtful. Above them, a thought bubble showing the man imagining himself "
        "in the woman's shoes, looking stressed while caring for an elderly person. "
        "Empathy and perspective-taking concept. Warm soft colors.",
        "2026-05-17_arakan_perspective.png"
    )

    img2 = generate_and_import_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A split scene: left side shows a young couple happily living with grandparents and children, "
        "right side shows a middle-aged couple looking tense with an elderly parent between them. "
        "Contrasting the difference between multigenerational living when young vs. late marriage. "
        "Soft muted colors, no text.",
        "2026-05-17_arakan_doukyostress.png"
    )

    img3 = generate_and_import_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A Japanese man in his late 50s sitting at a desk, looking confident and prepared, "
        "with documents and a small notepad showing care planning notes. "
        "A warm smile on his face. Organized, responsible, and hopeful atmosphere. "
        "Symbolizing someone who has done his homework for future caregiving.",
        "2026-05-17_arakan_prepared.png"
    )

    nodes = build_nodes(img1, img2, img3)
    rich_content = {"nodes": nodes, "metadata": {"version": 1}}

    print("Wixに下書き作成中...")
    body = {
        "draftPost": {
            "title": title,
            "richContent": rich_content,
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "memberId": MEMBER_ID,
            "excerpt": excerpt,
            "relatedPostIds": RELATED_POST_IDS,
        }
    }
    r = requests.post(
        f"{WIX_BASE}/blog/v3/draft-posts",
        headers=wix_headers(),
        json=body,
        timeout=30,
    )
    if not r.ok:
        print(f"下書き作成失敗: {r.status_code} {r.text[:300]}")
        return
    draft = r.json().get("draftPost", {})
    draft_id = draft.get("id")
    print(f"下書き作成完了: {draft_id}")

    if cover and draft_id:
        cover_id = cover["id"] if cover.get("id") else cover["url"].split("/media/")[-1].split("?")[0]
        print("カバー画像・メタ更新中...")
        patch_body = {
            "draftPost": {
                "id": draft_id,
                "media": {
                    "wixMedia": {"image": {"id": cover_id, "url": cover["url"]}},
                    "displayed": True,
                    "custom": True
                },
                "seoData": {
                    "tags": [{"type": "meta", "props": {"name": "description", "content": meta_desc}, "custom": False, "disabled": False}]
                }
            }
        }
        rp = requests.patch(
            f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
            headers=wix_headers(),
            json=patch_body,
            timeout=30,
        )
        if rp.ok:
            print("カバー画像・メタ更新完了！")
        else:
            print(f"更新失敗: {rp.status_code} {rp.text[:200]}")

    print(f"\n✅ 完了！下書きID: {draft_id}")
    print("⚠️  Wixブログ管理画面で画像が正しく表示されているか必ず確認してください！")

if __name__ == "__main__":
    main()
