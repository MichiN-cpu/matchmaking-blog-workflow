"""
漫画#2「見た目を変えたら、人生が変わった話」ブログ記事投稿
2026-05-25
"""
import os, time, uuid, base64, re, requests
from openai import OpenAI
from pathlib import Path

WIX_API_KEY  = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID  = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE     = "https://www.wixapis.com"
MEMBER_ID    = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_IDS = ["641187e4-a409-4c2f-9639-ecc548f26f15"]
TAG_IDS      = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
    "c2b8cde4-4435-435b-8b65-e02c2ba9e761",  # プロフィール
    "021e7932-59b1-43ae-9c76-4b00cd73b587",  # 好印象
    "6d01ad45-7102-4cf8-a156-98c908a968fe",  # 魅力
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
]
RELATED_POST_IDS = [
    "e1155633-e7b8-4179-8a0d-1283da56565c",  # 婚活の写真にかっこよさはいりません
    "d82eba55-ad05-41f3-b558-a17ab1646c52",  # 優しいのに選ばれない男性の減点行動
    "6ae51a61-7db6-4510-b865-f026ec1700fa",  # お見合いで仕事の苦労話をしていませんか
]

def wix_headers():
    return {"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID, "Content-Type": "application/json"}

def nid():
    return str(uuid.uuid4())[:8]

def sp():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": " ", "decorations": []}}
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
            "decorations": [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]
        }}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}

def image_node(url):
    m = re.search(r"/media/([^?#\s]+)", url)
    wix_uri = f"wix:image://v1/{m.group(1)}/img.png" if m else url
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": wix_uri}}, "caption": ""}}

def cta_node():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": "⬇️あなたに合った婚活を。無料相談はこちらから！⬇️",
            "decorations": [{"type": "LINK", "linkData": {"link": {"url": "https://www.asunaru.jp/soudan", "target": "BLANK"}}}]
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
        print("  uploadUrl取得失敗")
        return None
    sep = "&" if "?" in upload_url else "?"
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
        print("  URLが取得できませんでした")
        return None
    m = re.search(r"/media/([^?#\s]+)", url)
    media_id = m.group(1) if m else fid
    print(f"  → {url[:70]}...")
    return {"url": url, "id": media_id}

def build_nodes(img1_url, img2_url):
    n = []
    n.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    n.append(sp())
    n.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    n.append(sp())
    n.append(p("今日は、うちに来てくださった男性会員さんの話から始めさせてください。"))
    n.append(sp())
    n.append(p("他の相談所で3ヶ月、お見合いが1件も組めなかったという30代の男性でした。"))
    n.append(sp())
    n.append(p("「自分に問題があるんだと思います」と、最初の相談でそう言ったんです。静かに、でも確信した顔で。"))
    n.append(sp())
    n.append(p("話を聞いていくうちに、スキルの問題ではないことがわかってきました。プロフィールに出ている「第一印象」が、彼の実際の魅力を伝えられていなかった。それだけだったんです。"))
    n.append(sp())
    n.append(p("今日はそんな話を漫画にしました。よかったら、まずこちらを見てみてください。"))
    n.append(sp())
    n.append(link_node("→ 漫画「見た目を変えたら、人生が変わった話」を読む", "https://www.asunaru.jp/manga"))
    n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("「外見を気にするのは、なんか浅い気がして」"))
    n.append(sp())
    n.append(p("こういう感覚、男性にはすごく多いんですよね。"))
    n.append(sp())
    n.append(p("真剣に結婚を考えているからこそ、「外見じゃなくて中身で選んでほしい」という気持ちがある。それ自体は、とても誠実な考え方だと思うんです。"))
    n.append(sp())
    n.append(p("でもね、ちょっとだけ聞いてみたいことがあって。"))
    n.append(sp())
    n.append(p("初めてお見合いの席についたとき、相手の女性はあなたの「中身」をどうやって知るんでしょうか？"))
    n.append(sp())
    n.append(p("最初の数分、人は目から入ってくる情報を手がかりに、相手がどんな人かを読もうとします。これは意識的な判断ではなく、脳が自動的にやっていること。心理学では「薄切り判断（thin-slicing）」と呼ばれていて、わずか数十秒の観察から、かなり正確に相手の印象が形成されることがわかっています。"))
    n.append(sp())
    n.append(p("「外見が全てではない」は本当のことです。でも、「外見で損をしている状態を放置したまま、中身を伝えようとしている」のは、もったいない話でもある。そう思いませんか。"))
    n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("こんなこと、思い当たりませんか。"))
    n.append(sp())
    n.append(p("連絡が取れているのに、なぜかお見合いが組みにくい。"))
    n.append(sp())
    n.append(p("プロフィール写真を見直したことが、ここ1年一度もない。"))
    n.append(sp())
    n.append(p("「自分の外見は普通」だと思っているけれど、「普通」の根拠を誰かに確認したことがない。"))
    n.append(sp())
    n.append(p("——どれか一つでも「あるかも」と感じた方は、このあとの話がきっと役に立ちます。"))
    n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("外見を整えると、なぜ「接し方」まで変わるのか。"))
    n.append(sp())
    n.append(p("漫画の中で、田中さん（仮名）がプロフィール写真を見て「これ、本当に自分ですか？」と固まる場面があります。"))
    n.append(sp())
    n.append(p("これ、笑い話じゃないんです。"))
    n.append(sp())
    n.append(p("服を変え、髪を整え、写真を撮り直した。それだけで「自分の見え方」が変わった。するとお見合いの席で、今まで無意識にかけていたブレーキが少し緩んだんです。"))
    n.append(sp())
    n.append(p("「どうせ印象が良くないかも」という感覚が薄れると、話すときの余裕が変わります。"))
    n.append(sp())
    n.append(p("シカゴ大学の心理学者アダム・ガリンスキーらの研究（Enclothed Cognition）では、着る服が思考や行動のスタイルに影響を与えることが示されています。白衣を着ると注意力が高まる、というあれです。「自分に合った服を着ている」という感覚は、その人の話し方、視線、姿勢にまで微妙に影響を与える。"))
    n.append(sp())
    n.append(p("外見を整えることは、表面を取り繕うことじゃない。「自分の見え方に責任を持つ」という、内側からの変化なんですよね。"))
    n.append(sp())
    n.append(image_node(img1_url)); n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("「どうせ自分は…」という感覚は、反応パターンです。"))
    n.append(sp())
    n.append(p("右手で字を書く人が、左手で書こうとするとぎこちなくなる。それは左手が下手なのではなく、右手が「いつもの動き」として体に染み込んでいるだけです。"))
    n.append(sp())
    n.append(p("「外見に自信がない」という感覚も、同じような話で。"))
    n.append(sp())
    n.append(p("幼い頃に笑われた、変だと言われた、そういう経験が積み重なって、「自分の見た目は人より劣っている」というパターンが染み込んでいるケースが、本当に多い。"))
    n.append(sp())
    n.append(p("でも、それは「事実」じゃなくて「慣れた反応」なんです。"))
    n.append(sp())
    n.append(p("不安は性格ではなく反応パターン——うちでは、外見を整えるサポートと並行して、このパターンに気づいて緩めていく作業も一緒にやります。そこまでやらないと、また次の場面で同じブレーキがかかってしまうから。"))
    n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("変わっていく先に、何があるのか。"))
    n.append(sp())
    n.append(p("田中さんは、成婚退会のときにこう言っていました。「外見を変えたら、接し方まで変わった気がします」と。"))
    n.append(sp())
    n.append(p("それはきっと、外見の話だけじゃなかったんだと思います。"))
    n.append(sp())
    n.append(p("自分の見え方を整えて、写真を撮り直して、お見合いに出た。その小さな行動の積み重ねが、「自分にも変われる」という実感に変わっていった。"))
    n.append(sp())
    n.append(p("そういう積み重ねの先に、何があるか。"))
    n.append(sp())
    n.append(p("一緒に食卓を囲む相手がいる朝。疲れて帰った夜に、「今日どうだった？」と聞いてくれる人がいる夜。そういう当たり前の景色が、少しずつ近づいてきます。"))
    n.append(sp())
    n.append(p("外見を整えることは、その入口のひとつ。地味だけど、確かな一歩です。"))
    n.append(sp())
    n.append(image_node(img2_url)); n.append(sp())

    n.append(divider_node()); n.append(sp())
    n.append(h("今日の一歩"))
    n.append(sp())
    n.append(p("自分のプロフィール写真を、今日もう一度見てみてください。"))
    n.append(sp())
    n.append(p("「この写真で、自分のことを好きになってもらえるだろうか？」"))
    n.append(sp())
    n.append(p("その問いに自信を持って「うん」と言えなかったとしたら、それが変え時のサインです。うちでは写真撮影のサポートも一緒に考えます。気軽に話しかけてみてください。"))
    n.append(sp())
    n.append(cta_node())
    return n

def main():
    print("=== 漫画#2 ブログ投稿開始 ===")

    # 1. カバー画像アップロード
    print("\n[1] カバー画像アップロード中...")
    cover_bytes = open("drafts/images/2026-05-25_manga2_mikata_eyecatch.png", "rb").read()
    cover_url = upload_image_binary(cover_bytes, "2026-05-25_manga2_mikata_eyecatch.png")
    if not cover_url:
        print("カバー画像アップロード失敗。終了。")
        return

    # 2. ボディ画像アップロード
    print("\n[2] ショッピング画像アップロード中...")
    img1_bytes = open("drafts/images/2026-05-25_manga2_mikata_shopping.png", "rb").read()
    img1_url = upload_image_binary(img1_bytes, "2026-05-25_manga2_mikata_shopping.png")

    print("\n[3] カップル画像アップロード中...")
    img2_bytes = open("drafts/images/2026-05-25_manga2_mikata_couple.png", "rb").read()
    img2_url = upload_image_binary(img2_bytes, "2026-05-25_manga2_mikata_couple.png")

    if not img1_url or not img2_url:
        print("ボディ画像アップロード失敗。終了。")
        return

    # 3. 下書き作成
    print("\n[4] 下書き作成中...")
    nodes = build_nodes(img1_url["url"], img2_url["url"])
    draft_payload = {
        "draftPost": {
            "title": "【男性向け】見た目を変えたら、婚活も、自分への見方も変わった話。",
            "richContent": {"nodes": nodes},
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "memberId": MEMBER_ID,
            "media": {
                "wixMedia": {
                    "image": {
                        "id": cover_url["id"],
                        "url": cover_url["url"],
                        "height": 1024,
                        "width": 1536,
                        "filename": "2026-05-25_manga2_mikata_eyecatch.png"
                    }
                },
                "displayed": True,
                "custom": True
            }
        }
    }
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(), json=draft_payload)
    if not r.ok:
        print(f"下書き作成失敗: {r.status_code} {r.text[:300]}")
        return
    draft_id = r.json()["draftPost"]["id"]
    print(f"  下書きID: {draft_id}")

    # 4. excerpt・relatedPostIds更新
    print("\n[5] excerpt・関連記事更新中...")
    excerpt = "「どうせ自分は外見が…」そう思って婚活に踏み出せていませんか？見た目を変えることは、ただの表面的な話ではありません。外見を整えると、自信が戻り、接し方まで変わります。愛媛・松山の結婚相談所あすなる愛媛がお伝えします。"
    patch = requests.patch(
        f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}",
        headers=wix_headers(),
        json={"draftPost": {"excerpt": excerpt, "relatedPostIds": RELATED_POST_IDS}, "fieldMask": "excerpt,relatedPostIds"}
    )
    if patch.ok:
        print("  更新完了")
    else:
        print(f"  更新失敗: {patch.status_code} {patch.text[:200]}")

    print(f"\n=== 完了 ===")
    print(f"下書きID: {draft_id}")
    print("Wixブログ下書きフォルダを確認してください。")

if __name__ == "__main__":
    main()
