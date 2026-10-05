"""
ChatGPT作成の下書き「【男女共通】せっかく会えたのに、彼が昼寝。…」のレイアウト整え（2026-10-05）
本文の文章は変えず、あすなるブログの定型ルールに合わせる：
- 冒頭の画像2枚（アイキャッチ重複）を外し、本文の該当箇所へSMALL・中央で移動
- 見出し前を sp→DIVIDER→sp→HEADING に
- CTAの間に挟まっていた画像を外し、CTA直前にみっちゃん実写写真
- カテゴリ・タグ・関連記事・抜粋・SEO（説明文＋フォーカスキーワード）を設定
"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(__file__))
import post_keikaku_josei_dansei_2026_09_common as c

DRAFT_ID = "6f938ec5-c7e0-4c33-b3a9-cb6da95bb66c"
BASE = "https://www.wixapis.com"
H = c.wix_headers()
CTA_URL = "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-10-05-hirune-issho"

CATEGORY_IDS = [
    "5414dab5-ded7-4b15-a88a-d679d6fd3c71",  # 真剣交際
    "3f5f378d-a4f4-47e0-90a7-ab4daa27504e",  # 仮交際
]
TAG_LABELS = ["コミュニケーション", "パートナーシップ", "男性心理", "女性心理", "デート",
              "心理学", "NLP", "婚活マインド", "結婚生活", "松山市"]
EXCERPT = ("せっかく会えたのに、彼はソファで昼寝。「私といても楽しくない？」と気になった、私自身のお話です。"
           "聞いてみたら返ってきたのは「え？そんなこと思っとったん？」。"
           "“一緒にいる”の定義の違いと、不安を想像で終わらせない伝え方を、公認心理師・仲人の中嶋美知がお届けします。")
FOCUS_KEYWORD = "一緒にいる 定義 違い 交際 不安"


def text_of(n):
    return "".join(t.get("textData", {}).get("text", "") if t["type"] == "TEXT" else text_of(t) for t in n.get("nodes", []))


def is_blank(n):
    return n["type"] == "PARAGRAPH" and text_of(n).strip() == ""


def img(media_id):
    return c.image_node({"url": f"https://static.wixstatic.com/media/{media_id}"})


def main():
    d = requests.get(f"{BASE}/blog/v3/draft-posts/{DRAFT_ID}?fieldsets=CONTENT", headers=H).json()["draftPost"]
    old = d["richContent"]["nodes"]
    images = [n["imageData"]["image"]["src"]["id"] for n in old if n["type"] == "IMAGE"]
    sofa_img, talk_img = images[0], images[1]

    # 本文テキストだけ抜き出す（画像・空行・旧CTAを除く）
    body = [n for n in old if n["type"] in ("PARAGRAPH", "HEADING") and not is_blank(n)
            and "soudan" not in str(n)]

    new = []
    for n in body:
        t = text_of(n)
        if n["type"] == "HEADING":
            new += c.section_heading(t)
            continue
        new.append(n)
        if t.startswith("その間、彼はグーグー寝ていました"):
            new.append(img(sofa_img))
        if t.startswith("「少し休んだら、一緒にお茶にしない？」"):
            new.append(img(talk_img))
    new += [c.sp(), c.real_photo_node(), c.sp()] + c.cta_nodes(CTA_URL)

    # 関連記事：真剣交際カテゴリの最新3件
    q = {"query": {"filter": {"categoryIds": {"$hasSome": [CATEGORY_IDS[0]]}}, "sort": [{"fieldName": "firstPublishedDate", "order": "DESC"}], "paging": {"limit": 3}}}
    related = [x["id"] for x in requests.post(f"{BASE}/blog/v3/posts/query", headers=H, json=q).json()["posts"]]

    tags = {x["label"]: x["id"] for x in requests.get(f"{BASE}/blog/v3/tags?paging.limit=100", headers=H).json()["tags"]}
    tag_ids = [tags[l] for l in TAG_LABELS]

    r = requests.patch(f"{BASE}/blog/v3/draft-posts/{DRAFT_ID}", headers=H, json={
        "draftPost": {"richContent": {"nodes": new, "metadata": {"version": 1}},
                      "categoryIds": CATEGORY_IDS, "tagIds": tag_ids,
                      "relatedPostIds": related, "excerpt": EXCERPT},
        "fieldMask": "richContent,categoryIds,tagIds,relatedPostIds,excerpt"})
    print("本文・分類:", r.status_code, "" if r.ok else r.text[:300])
    c.set_seo(DRAFT_ID, {"title": d["title"], "excerpt": EXCERPT, "focus_keyword": FOCUS_KEYWORD})


if __name__ == "__main__":
    main()
