"""
「こんな私でも大丈夫？」下書きに画像3枚を追加するスクリプト
既存下書きID: 19d45af3-381f-45b0-8f38-a9449c47addf
"""
import os, re, time, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
DRAFT_ID    = "19d45af3-381f-45b0-8f38-a9449c47addf"

client = OpenAI(api_key=OPENAI_KEY)

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
            "A Japanese woman in her late 20s or early 30s sitting at a bright cafe table, "
            "looking thoughtfully at a notebook with a gentle, hopeful expression. "
            "Morning light through a window, soft white and cream tones. "
            "She looks like she is considering something new and positive."
        ),
        "filename": "2026-05-30_konname_img1.png",
        "caption": "",
    },
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A confident Japanese woman standing in a modern city street, smiling naturally, "
            "wearing a smart casual outfit. She looks self-assured and at ease. "
            "Bright daylight, clean urban background softly blurred."
        ),
        "filename": "2026-05-30_konname_img2.png",
        "caption": "",
    },
    {
        "prompt": (
            f"{BASE_STYLE}. "
            "A happy Japanese couple walking together in a bright park, laughing and enjoying each other's company. "
            "Warm afternoon light, greenery in background softly blurred. "
            "Relaxed and joyful atmosphere, sense of partnership and ease."
        ),
        "filename": "2026-05-30_konname_img3.png",
        "caption": "",
    },
]

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

def image_node(file_info, caption=""):
    url = file_info["url"]
    return {
        "type": "IMAGE",
        "id": nid(),
        "nodes": [],
        "imageData": {
            "image": {"src": {"url": url}},
            "caption": caption,
        }
    }

def generate_and_upload(prompt_text, filename):
    print(f"  gpt-image-1 生成中: {filename}")
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=prompt_text,
        size="1536x1024",
        quality="medium",
        n=1,
    )
    image_bytes = base64.b64decode(resp.data[0].b64_json)
    print(f"  生成完了。Wixにアップロード中...")

    # アップロードURL取得
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

    # バイナリPUT
    sep = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(
        f"{upload_url}{sep}filename={filename}",
        data=image_bytes,
        headers=hdrs,
        timeout=60,
    )
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
    media_id = m.group(1) if m else fid
    print(f"  アップロード完了: {url[:70]}...")
    return {"url": url, "id": media_id}

def build_nodes(imgs):
    img1, img2, img3 = imgs[0], imgs[1], imgs[2]
    n = []

    # 冒頭挨拶
    n.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    n.append(sp())
    n.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    n.append(sp())
    n.append(p("「婚活したいけど、自分みたいな人間が行って大丈夫かな」"))
    n.append(sp())
    n.append(p("そういう不安、ものすごくよくわかります。今日はそのリアルな疑問に、正直に答えます。"))
    n.append(sp())

    # 画像1: 入会前の不安を感じる女性
    if img1:
        n.append(image_node(img1))
        n.append(sp())

    # セクション1
    n.extend(heading_block("入会前の「私って大丈夫？」"))
    n.append(q("Q. 恋愛経験がほとんどないのですが、大丈夫ですか？"))
    n.append(sp())
    n.append(p("むしろ大歓迎です！！恋愛経験が少ない方ほど素直に吸収してくれて、グングン成長する姿を何度も見てきました。大切なのは経験の数じゃなくて「相手のことを大切にしたい」という気持ち。一緒にゼロから作っていきましょう。"))
    n.append(sp())
    n.append(q("Q. 婚活が初めてで何もわかりません。何から始めればいいですか？"))
    n.append(sp())
    n.append(p("「何もわからない」状態で来てくれるのが、実は一番ありがたいんですよ（笑）。まっさらな状態が最高のスタートラインです。準備なんて何もいりません、手ぶらで来てください！"))
    n.append(sp())
    n.append(q("Q. 以前、別の結婚相談所でうまくいきませんでした。また失敗するのが怖いです。"))
    n.append(sp())
    n.append(p("前の相談所でうまくいかなかった経験、それがあすなる愛媛でうまくいくための大切な材料になるんです。どこで行き詰まったか・何が合わなかったか——一緒に丁寧に振り返ることが、次の婚活をまったく別ものに変えます。"))
    n.append(sp())
    n.append(q("Q. 自分に自信がないのですが、入会しても意味ありますか？"))
    n.append(sp())
    n.append(p("自信がない状態で来てくれてちょうどいいんです！「自信がついてから婚活しよう」と思っていると、一生始められないですよ（笑）。婚活を進める中でどんどん自信がついていく方を何人も見てきました。動きながら変わっていくのが、婚活の醍醐味のひとつです。"))
    n.append(sp())
    n.append(q("Q. 離婚歴があります。再婚活でも入会できますか？"))
    n.append(sp())
    n.append(p("もちろん！再婚希望の方も大歓迎です。一度の経験があるからこそ「次はこんな関係を築きたい」というビジョンがはっきりしていて、かえってスムーズにいくケースも多いです。お子さんのこと・お金のこと・親への挨拶など、再婚ならではのデリケートな部分も一緒に丁寧に考えていきます。"))

    n.append(sp())

    # 画像2: 自信ある女性
    if img2:
        n.append(image_node(img2))
        n.append(sp())

    # セクション2
    n.extend(heading_block("「スペックが低い」「別に困ってない」という方へ"))
    n.append(q("Q. スペック（収入・外見）が低いと、活動しても意味ないですか？"))
    n.append(sp())
    n.append(p("スペックが全てだったら結婚相談所って成立しないんですよ（笑）。「一緒にいて心地よい人」「誠実に向き合ってくれる人」が選ばれる場面を何度も見てきました。「スペックが低い」と思っている方ほど、人の話をよく聞けて相手を大切にできる方が多い。それって一番大事な「結婚向きの素質」です。"))
    n.append(sp())
    n.append(q("Q. 「結婚相談所に入るほど困ってない」と思ってます。"))
    n.append(sp())
    n.append(p("この言葉、実はめちゃくちゃ多いんですよ（笑）。でも「困ってから動く」より「動いてから変わる」のほうが婚活はうまくいきます。「困ってないけど、このままでいいのかな」と思ったとき——それが一番いいタイミングかもしれないです。"))
    n.append(sp())
    n.append(q("Q. カウンセラーに「結婚できない理由」を分析されるのが怖いです。"))
    n.append(sp())
    n.append(p("怖いですよね（笑）。でも私は「ダメ出し」をするつもりはまったくないです。「なんでうまくいかないの？」を一緒に発見するのは、責めるためじゃなくて「じゃあここを変えたら変わるよ！」という希望を見つけるためです。分析より共感が先、それが私のスタイルです。"))

    n.append(sp())

    # セクション3
    n.extend(heading_block("活動中のこと"))
    n.append(q("Q. 仕事が忙しくて月に1〜2回しか動けません。それでも活動できますか？"))
    n.append(sp())
    n.append(p("できます！忙しい方ほど限られた機会を大切に使う意識が高くて、結果的にうまくいくケースが多いです。活動ペースは一緒に考えますので、まずご相談ください。"))
    n.append(sp())
    n.append(q("Q. お見合い相手は自分で選べますか？それとも紹介してもらうんですか？"))
    n.append(sp())
    n.append(p("両方できます！IBJのシステムで自分で検索してお申込みすることも、私からご提案することも。その時々の状況に合わせて組み合わせながら進めていきます。"))
    n.append(sp())
    n.append(q("Q. 交際中、どんなアドバイスをもらえますか？"))
    n.append(sp())
    n.append(p("LINEの返し方、デートプランの立て方、気持ちの伝え方——交際中に出てくる「どうしよう！」に具体的にお答えします。「相手が今どんな気持ちでいるか」を、心理カウンセラーの視点から一緒に読み解きながらサポートします。一人で悩まなくていい、それがあすなる愛媛の良さです。"))
    n.append(sp())
    n.append(q("Q. 成婚までに平均どのくらいかかりますか？"))
    n.append(sp())
    n.append(p("早い方で半年、平均的には1〜2年くらいのイメージです。大切なのはスピードより「この人でよかった！」と心から思える出会い。焦らず、でも止まらず、一緒に進んでいきましょう。"))
    n.append(sp())

    # 画像3: 幸せなカップル（希望の着地）
    if img3:
        n.append(image_node(img3))
        n.append(sp())

    # CTA
    n.append(p("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan"))

    return n

def main():
    print("=" * 50)
    print("「こんな私でも大丈夫？」画像追加スクリプト")
    print("=" * 50)

    # 画像3枚生成
    imgs = []
    for i, info in enumerate(IMAGE_PROMPTS, 1):
        print(f"\n[画像{i}/3]")
        result = generate_and_upload(info["prompt"], info["filename"])
        imgs.append(result)

    if any(img is None for img in imgs):
        print("\n⚠️ 一部の画像生成に失敗しました。処理を続行します。")

    # richContent再構築（画像込み）
    print("\nrichContent構築中...")
    nodes = build_nodes(imgs)
    rich_content = {"nodes": nodes, "metadata": {"version": 1}}

    # PATCH: richContentを更新
    print("Wix draft-posts PATCH中...")
    patch_body = {
        "draftPost": {
            "richContent": rich_content,
        },
        "fieldMask": "richContent"
    }
    r = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}",
        headers=wix_headers(),
        json=patch_body,
        timeout=30,
    )
    if r.ok:
        print("richContent更新完了 ✅")
    else:
        print(f"richContent更新失敗: {r.status_code} {r.text[:300]}")
        return

    # カバー画像のdisplayed:trueを確認
    # 既存のカバー画像URLを使ってdisplayedをtrueに設定
    cover_url = "https://static.wixstatic.com/media/e6bbff_d6a9cf480ad640699ff6c3ac1ecc2293~mv2.png"
    m = re.search(r"/media/([^?#\s]+)", cover_url)
    cover_id = m.group(1) if m else ""

    print("カバー画像 displayed:true に更新中...")
    cover_patch = {
        "draftPost": {
            "media": {
                "custom": True,
                "displayed": True,
                "wixMedia": {
                    "image": {
                        "id": cover_id,
                        "url": cover_url,
                        "height": 1024,
                        "width": 1792,
                        "filename": "2026-04-29_qa2_eyecatch.png",
                    }
                }
            }
        },
        "fieldMask": "media"
    }
    rc = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}",
        headers=wix_headers(),
        json=cover_patch,
        timeout=30,
    )
    if rc.ok:
        print("カバー画像更新完了 ✅")
    else:
        print(f"カバー画像更新失敗: {rc.status_code} {rc.text[:200]}")

    print(f"\n✅ 完了！")
    print(f"下書きID: {DRAFT_ID}")
    print(f"管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")
    print("\n📌 投稿後、Wixの下書きで画像が正しく表示されているか確認してください。")

if __name__ == "__main__":
    main()
