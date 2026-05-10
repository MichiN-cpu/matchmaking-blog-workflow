"""
お父さん同士が意気投合した話 — Wix下書き投稿スクリプト
カテゴリ: 真剣交際
2026-05-10
"""
import os, re, time, uuid, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_ID = "5414dab5-ded7-4b15-a88a-d679d6fd3c71"  # 真剣交際

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
    ], "paragraphData": {}}

def image_node(url, caption=""):
    m = re.search(r"/media/([^?#\s]+)", url)
    wix_uri = f"wix:image://v1/{m.group(1)}/img.png" if m else url
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": wix_uri}}, "caption": caption}}

def generate_and_import_image():
    prompt = (
        "Flat illustration style, no text, soft warm tones, minimalist, Japanese blog aesthetic. "
        "Two older Japanese men sitting together at a warm restaurant, smiling and laughing happily, "
        "raising glasses in a toast, celebrating their children's marriage. "
        "Soft cherry blossom elements in the background, heartwarming and joyful family scene."
    )
    print("DALL-E 3 画像生成中...")
    resp = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="standard",
        n=1,
    )
    dall_e_url = resp.data[0].url
    print(f"生成完了。Wixにインポート中...")

    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/import",
        headers=wix_headers(),
        json={"url": dall_e_url, "displayName": "2026-05-10_eyecatch.png", "mimeType": "image/png"},
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
                m = re.search(r"/media/([^?#\s]+)", url)
                print(f"インポート完了: {url[:60]}...")
                return {"url": url, "id": m.group(1) if m else file_id}
            print(f"待機中... ({fd.get('state')}, {i+1}/20)")
    print("タイムアウト")
    return None

def build_nodes(cover_img=None):
    nodes = []

    # 冒頭挨拶
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    # 本文
    nodes.append(p("今日はちょっと嬉しくて、どうしても書きたくなって、つぶやかせてください。"))
    nodes.append(sp())
    nodes.append(p("今月ご成婚退会される会員さんがいらっしゃいまして。昨日、そのご報告のお話を聞かせてもらったんですけど、顔合わせのエピソードがすごくて。"))
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p("彼女のお父さんと彼のお父さんが、めちゃくちゃ意気投合されたというんですよ！"))
    nodes.append(sp())
    nodes.append(p("はじめての顔合わせ、初対面なのに「2人で飲みましょう」って。お互いの娘さんと息子さんのことを、こんなにも嬉しそうに喜んで、迎え入れてくれていて。それだけで胸がいっぱいになるんですけど。"))
    nodes.append(sp())
    nodes.append(p("その話を教えてくれたのが、男性の会員さんのほうで。"))
    nodes.append(sp())
    nodes.append(p("照れながら、教えてくれたんですよね。"))
    nodes.append(sp())
    nodes.append(p("もう、かわいくて。たまらなかった（笑）。"))
    nodes.append(sp())
    nodes.append(divider_node())
    nodes.append(sp())
    nodes.append(p("婚活って、本人同士の縁だけじゃないんだなって、改めて思いました。2人が出会うことで、新しい家族が生まれる。お父さん同士が仲良くなる。その輪がひろがっていく。"))
    nodes.append(sp())
    nodes.append(p("それを近くで見させてもらえることが、この仕事をしていて一番幸せな瞬間のひとつです。"))
    nodes.append(sp())
    nodes.append(p("幸せのおすそ分け、ありがとうございます😊"))
    nodes.append(sp())

    # CTA
    nodes.append(link_node("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"))

    return nodes

def main():
    title = "お父さん同士が意気投合した話"

    # 画像生成・アップロード
    cover = generate_and_import_image()

    # richContent構築
    nodes = build_nodes(cover)
    rich_content = {"nodes": nodes, "metadata": {"version": 1}}

    # 下書き作成
    print("Wixに下書き作成中...")
    body = {
        "draftPost": {
            "title": title,
            "richContent": rich_content,
            "categoryIds": [CATEGORY_ID],
            "memberId": MEMBER_ID,
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

    # カバー画像・メタディスクリプション更新
    if cover and draft_id:
        print("カバー画像・メタ更新中...")
        patch_body = {
            "draftPost": {
                "coverMedia": {
                    "image": {"src": {"url": cover["url"]}}
                },
                "seoData": {
                    "description": "今月ご成婚退会される会員さんから、顔合わせのエピソードを聞きました。両家のお父さん同士が意気投合して「2人で飲みましょう」と。婚活って、本人同士だけでなく家族の縁でもあるんですよね。"
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
            print("カバー画像・メタ更新完了")
        else:
            print(f"カバー更新失敗: {rp.status_code} {rp.text[:200]}")

    print(f"\n✅ 完了！下書きID: {draft_id}")
    print(f"タイトル: {title}")
    print(f"カテゴリ: 真剣交際")

if __name__ == "__main__":
    main()
