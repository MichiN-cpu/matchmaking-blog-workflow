"""
苦手でも、諦めなかった。30代医療職男性の成婚ストーリー — Wix下書き投稿スクリプト
カテゴリ: 成婚までのロードマップ / 30代婚活
2026-05-17
"""
import os, time, uuid, base64, tempfile, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_IDS = [
    "998b685d-1453-4ebd-8bd2-0218e315186e",  # 成婚までのロードマップ
    "ce3b3deb-a05e-4093-a1a3-aa657693da8d",  # 30代婚活
]
TAG_IDS = [
    "55498a0c-d02e-449d-b1b9-ecc659d5de60",  # 成婚
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "128a636a-6658-495e-ac2e-0f176a27b460",  # 出逢い
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "61acc4f3-6c16-4653-995b-dd6d9136c1d3",  # IBJ
]
RELATED_POST_IDS = [
    "d64cb253-7097-4949-8117-805356a6d359",  # 「なんか嫌だな」を、スルーしないでいてください
    "618586db-5475-4e65-b848-af2b5643c30c",  # 【成婚エピソード】自分を変える勇気が、彼を変えた。7ヶ月
    "59111839-05a2-4b2a-afeb-87acd564b09f",  # 軽く、軽く、軽く。成婚者19,112人のデータ
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
    # 静的URLを直接使用（wix:image://v1/ 形式は表示されない問題あり）
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": url}}, "caption": caption}}

def upload_image_binary(image_bytes, filename):
    """バイナリデータをWix Mediaに直接アップロードする"""
    # Step1: アップロードURLを取得
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
    upload_url = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        print(f"uploadURL取得失敗: {data}")
        return None

    # Step2: バイナリをアップロード（filenameをクエリパラメータで渡す）
    sep = "&" if "?" in upload_url else "?"
    upload_url_with_filename = f"{upload_url}{sep}filename={filename}"
    headers = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        headers["Authorization"] = upload_token
    ru = requests.put(upload_url_with_filename, data=image_bytes, headers=headers, timeout=60)
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
    print(f"バイナリアップロード完了: {file_url[:60]}...")
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

    # gpt-image-1はb64_jsonを返す
    if img_data.b64_json:
        image_bytes = base64.b64decode(img_data.b64_json)
        return upload_image_binary(image_bytes, filename)

    # URLが取得できた場合はimport APIを使用
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
            print(f"file_id取得失敗: {data}")
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
                print(f"待機中... ({fd.get('state')}, {i+1}/20)")
        print("タイムアウト")
    return None

def build_nodes(img1=None, img2=None, img3=None):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # イントロ
    nodes.append(p("今日は嬉しいご報告をしたいと思います。"))
    nodes.append(sp())
    nodes.append(p("今年、あすなる愛媛から素敵なご縁で成婚退会された、30代後半・医療職の男性会員さんのインタビューをご紹介します。"))
    nodes.append(p("「話すのが得意なほうじゃない」「マッチングアプリは自分に合わないかも」——そんな彼が、活動開始から11ヶ月で幸せをつかんだお話です。"))
    nodes.append(sp())

    # Section 1
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("きっかけは、友人の一言だった"))
    nodes.append(sp())
    nodes.append(p("「30代で結婚したいな」という気持ちは、ずっとあったそうです。"))
    nodes.append(p("でも「いつか」は、なかなか「いま」にはならないんですよね（笑）。"))
    nodes.append(sp())
    nodes.append(p("それが動き出したのは、結婚報告を受けた身近な友人から「相談所に入会してご縁をつかんだ」と聞いたときでした。"))
    nodes.append(sp())
    nodes.append(p("頭で考えていたことが、急にリアルに感じられる瞬間ってあります。"))
    nodes.append(p("「あ、本当にそういう出会い方があるんだ」って。"))
    nodes.append(p("それが行動への背中を押してくれたんですね。"))
    nodes.append(sp())

    # Section 2
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("マッチングアプリじゃなくて、相談所を選んだ理由"))
    nodes.append(sp())
    nodes.append(p("マッチングアプリも検討されたそうです。"))
    nodes.append(p("でも、「自分から話を広げたり、軽いやり取りを重ねたりするのが得意じゃない」という自己認識がありました。"))
    nodes.append(sp())
    nodes.append(p("これって、すごく正直な気づきだと思うんですよね。"))
    nodes.append(sp())
    nodes.append(p("マッチングアプリって、ある意味「会話スキルのゲーム」みたいな側面があります。"))
    nodes.append(p("テンポよく相手を楽しませる文章を書き続けないといけない。"))
    nodes.append(p("でも彼が求めていたのはそういう「うまい会話」じゃなかった。"))
    nodes.append(p("「きちんと結婚を考えている方と、ちゃんと向き合って出会いたい」ということだったんですよね。"))
    nodes.append(sp())
    nodes.append(p("そこで相談所という選択肢が、ストンと腑に落ちました。"))
    nodes.append(sp())

    # Section 3
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("活動を通じて、自分が変わっていった"))
    nodes.append(sp())
    nodes.append(p("入会当初は、自分の気持ちや考えを表現することに少し苦手意識があったと話してくれました。"))
    nodes.append(p("そこで心理カウンセリングを含めた面談を重ねていくうちに、周囲から「前より話すようになったね」と言われるようになったそうです。"))
    nodes.append(sp())
    nodes.append(p("これ、面白い現象なんですよね。"))
    nodes.append(sp())
    nodes.append(p("心理学でいう「行動が先、感情が後」という考え方があります。"))
    nodes.append(p("自信がついてから行動するのではなく、行動することで自信が育っていく。"))
    nodes.append(p("婚活って、そういう意味での「自己成長の場」でもあるんです。"))
    nodes.append(p("自己表現を止める心のブレーキを一緒に緩めていったのが、静かに、でも確実に、彼を変えていったんだと思います。"))
    nodes.append(sp())

    if img1:
        nodes.append(image_node(img1["url"], "心理カウンセリングを通じた自己成長のイメージ"))
        nodes.append(sp())

    # Section 4
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("落ち込んだ。でも止まらなかった。"))
    nodes.append(sp())
    nodes.append(p("正直なエピソードも話してくれました。"))
    nodes.append(sp())
    nodes.append(p("お見合いで「自分から話してばかりだった」という理由でお断りされたとき、「かなり落ち込んだ」と。"))
    nodes.append(p("「もう縁がなかったと思ってやめようかな」と思ったこともあったそうです。"))
    nodes.append(sp())
    nodes.append(p("その気持ち、すごくよくわかります。"))
    nodes.append(sp())
    nodes.append(p("でも彼は、「モヤモヤしながらも活動を完全には止めませんでした」と言っていました。"))
    nodes.append(sp())
    nodes.append(p("この「完全には止めなかった」って、実はすごく大事な言葉だと私は思うんです。"))
    nodes.append(p("落ち込んだとき、ぱたっと止まってしまうことがあります。"))
    nodes.append(p("それは自然なことです。"))
    nodes.append(p("でも、完全に止めずにいることが、次の出会いへの扉を開けたまま保っておくことにつながります。"))
    nodes.append(sp())
    nodes.append(p("行動科学的に言えば、惰性よりも意図的な継続のほうが難しい。"))
    nodes.append(p("でもそこにこそ、価値があります。"))
    nodes.append(sp())

    # Section 5
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("「また一緒に出かけたい」という気持ちの正体"))
    nodes.append(sp())
    nodes.append(p("一緒にご成婚退会された彼女との初対面で、「優しそうで、しっかりされている」「こちらの話をきちんと聞いてくださる方で、とても安心した」と感じたそうです。"))
    nodes.append(p("その後は、食事、いちご狩り、水族館……と少しずつデートを重ねていきました。"))
    nodes.append(sp())
    nodes.append(p("「結婚を決めた瞬間」を聞くと、「一瞬に決まったというより、一緒に過ごす時間の積み重ねでした」とのこと。"))
    nodes.append(sp())
    nodes.append(p("これ、心理学でいう「単純接触効果（ザイアンス効果）」に近い話かもしれません。"))
    nodes.append(p("人は同じ相手と接触する回数が増えるほど、自然と好意が深まっていきます。"))
    nodes.append(p("「また一緒に出かけたい」という感覚は、オキシトシンやドーパミンが静かに積み重なっていくサインでもあります。"))
    nodes.append(sp())
    nodes.append(p("ビビッとくる瞬間で決まるものだと思いがちですよね。"))
    nodes.append(p("でも多くの場合、「この人といると安心できる」「また会いたいと思える」という小さな積み重ねのほうが、ずっと信頼できる判断材料なんだと思います。"))
    nodes.append(sp())

    # Section 6
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("住所を間違えたデートが、一番の思い出になった"))
    nodes.append(sp())
    nodes.append(p("特に印象深かったエピソードを聞くと、タオル美術館のイルミネーションデートの話を聞かせてくれました。"))
    nodes.append(sp())
    nodes.append(p("住所を入力するときにミスをして、全然違う場所に向かってしまったそうです（笑）。"))
    nodes.append(sp())
    nodes.append(p("でもそのとき彼女から「そういうのも楽しかった」と言ってもらえました。"))
    nodes.append(sp())
    nodes.append(p("「その言葉がすごく嬉しかった」と、彼は話してくれました。"))
    nodes.append(sp())
    nodes.append(p("うまくいかないとき、予定通りじゃないとき。"))
    nodes.append(p("そこで相手がどういう反応をするか——そこに、その人の本当の姿が出る気がします。"))
    nodes.append(p("「そういうのも楽しかった」って言える人は、一緒にいてとても安心できる人なんですよね。"))
    nodes.append(sp())

    if img2:
        nodes.append(image_node(img2["url"], "イルミネーションをふたりで楽しむイメージ"))
        nodes.append(sp())

    # Section 7
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("条件って、変わっていいんだと気づいた"))
    nodes.append(sp())
    nodes.append(p("入会前は「将来的に関西に戻りたい。そのことを理解してくれる人」という条件があったそうです。"))
    nodes.append(p("でも活動を通じて、その考え方が変わっていったと言います。"))
    nodes.append(p("「完全に自分の希望通りでなくても、お互いに納得できる形を見つけることが大切」という気持ちになったと。"))
    nodes.append(sp())
    nodes.append(p("これって大事なことだなあ、と思います。"))
    nodes.append(sp())
    nodes.append(p("条件を持つことは悪いことじゃありません。"))
    nodes.append(p("でも、条件は「守るべき壁」ではなくて「話し合いの出発点」なんですよね。"))
    nodes.append(p("結婚ってそもそも、ひとりが全部思い通りになる場所じゃない。"))
    nodes.append(p("「どうお互いが納得できる形を作っていくか」を考えられる人が、本当に結婚に向いている人なんじゃないかと私は思っています。"))
    nodes.append(sp())

    # Section 8
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("おすすめデートスポットも教えてもらいました"))
    nodes.append(sp())
    nodes.append(p("父母ヶ浜が一番のおすすめだそうです。"))
    nodes.append(p("「天気の良い日はとても気持ちがいいし、夕暮れ時の景色もきれい」とのこと。"))
    nodes.append(p("四国水族館やタオル美術館のイルミネーションも、「景色を見たり食事をしたりしながら自然に会話ができる場所」として挙げてくれました。"))
    nodes.append(p("愛媛に住んでいると意外と見落としがちな場所が、実は婚活にぴったりなんですよね。"))
    nodes.append(sp())

    if img3:
        nodes.append(image_node(img3["url"], "父母ヶ浜の夕暮れイメージ"))
        nodes.append(sp())

    # Section 9
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(h("これから婚活を考えている方へ"))
    nodes.append(sp())
    nodes.append(p("彼からのメッセージです。"))
    nodes.append(sp())
    nodes.append(p("「結婚したい気持ちや、将来ひとりは寂しいなという気持ちが少しでもあるなら、まずは軽く相談してみてもいいと思います。迷っている方は、軽いお試しの感覚でも一歩踏み出してみてほしいです。」"))
    nodes.append(sp())
    nodes.append(p("私からも同じ気持ちです。"))
    nodes.append(sp())
    nodes.append(p("「苦手なことがあるから婚活は無理」じゃなくて、苦手なままで始めても大丈夫。"))
    nodes.append(p("活動を通じて変わっていけます。"))
    nodes.append(p("彼がそれを証明してくれています。"))
    nodes.append(sp())
    nodes.append(p("担当カウンセラーとして、入会当初の彼の控えめで誠実なお人柄から、心理カウンセリングを含む面談を通じてご自身の言葉で想いを伝えられるようになっていく姿を見ていました。"))
    nodes.append(p("本当に嬉しかったです。"))
    nodes.append(p("穏やかで温かなご家庭を築かれることを、心より願っています。"))
    nodes.append(sp())

    # CTA（中央寄せ）
    nodes.append(link_node("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"))

    return nodes

def main():
    title   = "「苦手でも、諦めなかった。」30代医療職男性の成婚ストーリー"
    excerpt = "「話すのが得意ではない」「マッチングアプリは合わないかも」——そんな30代後半・医療職の男性が、あすなる愛媛で活動開始から11ヶ月でご成婚。自己成長の過程、住所ミスのデートエピソード、条件観の変化など、リアルな成婚ストーリーをご紹介します。"
    meta_desc = "「話すのが得意でない」30代医療職の男性が、心理カウンセリングを通じて自己成長し活動開始から11ヶ月でご成婚。住所ミスのデートが一番の思い出に。あすなる愛媛の成婚ストーリー。"

    cover = generate_and_import_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A Japanese man in his 30s with neat dark clothing, standing at a crossroads with a gentle determined smile, "
        "holding a small glowing compass. Soft cherry blossom petals falling around him, warm golden afternoon light. "
        "Hopeful and persevering atmosphere, symbolizing not giving up in finding love.",
        "2026-05-17_seikon_30s_cover.png"
    )

    img1 = generate_and_import_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A Japanese man in his 30s sitting across from a warm female counselor at a cozy desk with plants, "
        "both looking engaged and relaxed in conversation. The man looks gradually opening up, smiling softly. "
        "Soft indoor lighting, warm colors. Self-growth and psychological counseling atmosphere.",
        "2026-05-17_self_growth_counseling.png"
    )

    img2 = generate_and_import_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "A Japanese couple in their 30s walking together under beautiful colorful illumination lights at night, "
        "both smiling and laughing naturally. Warm glowing lights reflecting around them. "
        "Romantic and cozy night date atmosphere, no text.",
        "2026-05-17_illumination_date.png"
    )

    img3 = generate_and_import_image(
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "Beautiful sunset at a mirror-like tidal flat beach in Shikoku Japan, "
        "golden sky reflected perfectly on the wet sand, silhouette of a couple walking hand in hand. "
        "Peaceful, romantic and hopeful atmosphere, warm orange and pink tones.",
        "2026-05-17_chichihama_sunset.png"
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
        print("カバー画像・メタ更新中...")
        patch_body = {
            "draftPost": {
                "coverMedia": {
                    "image": {"src": {"url": cover["url"]}}
                },
                "seoData": {
                    "description": meta_desc
                }
            },
            "fieldMask": "coverMedia,seoData.description"
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
