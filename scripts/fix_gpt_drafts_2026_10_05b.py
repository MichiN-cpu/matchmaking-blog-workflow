"""
ChatGPT作成の下書き2本の仕上げ（2026-10-05）
レイアウト（区切り線・実写写真・CTA中央寄せ・画像SMALL）はChatGPT側で対応済みだったので、
残りの抜けだけ補う：CTAのUTM付与と表記統一／カテゴリ・タグ・関連記事・抜粋・SEO。
本文の文章は変えない（1文が2段落に割れていた箇所だけ1段落にまとめる）。
"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(__file__))
import post_keikaku_josei_dansei_2026_09_common as c

BASE = "https://www.wixapis.com"
H = c.wix_headers()
CAT = {
    "仮交際": "3f5f378d-a4f4-47e0-90a7-ab4daa27504e",
    "真剣交際": "5414dab5-ded7-4b15-a88a-d679d6fd3c71",
    "お見合い": "5089ac63-e2ce-4de1-b472-3512a77401af",
}

POSTS = [
    {
        "id": "a84e130b-8a6d-4bf1-b601-6ca462582047",
        "slug": "2026-10-05-ittekure-moyaru",
        "cats": ["仮交際", "真剣交際"],
        "tags": ["女性心理", "男性心理", "コミュニケーション", "パートナーシップ", "デート",
                 "心理学", "NLP", "婚活マインド", "松山市"],
        "excerpt": ("「どこか行きたいなら言ってくれたらいいよ」。優しいひと言のはずなのに、なぜかモヤッとしたことはありませんか。"
                    "その奥にある「私と何かしたいと思ってほしい」という願いと、察してほしいを小さなお願いに変える伝え方を、"
                    "公認心理師・仲人の中嶋美知がお届けします。"),
        "keyword": "交際 デート 提案がない 女性心理 モヤモヤ",
        "merge": ("そんな時は", "性格と決めつけるより"),
    },
    {
        "id": "bc500ed6-cdcf-40e1-9172-85c8e7fbffae",
        "slug": "2026-10-05-omiai-shokuji",
        "cats": ["お見合い", "仮交際"],
        "tags": ["お見合い", "男性心理", "女性心理", "コミュニケーション", "好印象",
                 "相手の見極め方", "心理学", "NLP", "婚活マインド", "松山市"],
        "excerpt": ("お見合いで「食事をしませんか？」「食べません」。そのあと男性だけが食事をして、女性は「ありえない」とお断りに。"
                    "同じテーブルで何がすれ違ったのか、自分の「当たり前」に気づくヒントと、次のお見合いで使えるひと言を、"
                    "公認心理師・仲人の中嶋美知がお届けします。"),
        "keyword": "お見合い 食事 マナー すれ違い 結婚相談所",
        "merge": None,
    },
]


def text_of(n):
    return "".join(t.get("textData", {}).get("text", "") if t["type"] == "TEXT" else text_of(t) for t in n.get("nodes", []))


def fix(cfg, tags):
    d = requests.get(f"{BASE}/blog/v3/draft-posts/{cfg['id']}?fieldsets=CONTENT", headers=H).json()["draftPost"]
    nodes = d["richContent"]["nodes"]

    # 旧CTA2行（UTMなし）を外して、UTM付きの定型CTAに差し替え
    while "soudan" in str(nodes[-1]):
        nodes.pop()
    cta_url = f"https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign={cfg['slug']}"
    nodes += c.cta_nodes(cta_url)

    # 2段落に割れた1文をまとめる
    if cfg["merge"]:
        a, b = cfg["merge"]
        i = next(i for i, n in enumerate(nodes) if text_of(n).strip() == a)
        assert text_of(nodes[i + 1]).startswith(b)
        nodes[i:i + 2] = [c.p(a + "、" + text_of(nodes[i + 1]))]

    cat_ids = [CAT[x] for x in cfg["cats"]]
    q = {"query": {"filter": {"categoryIds": {"$hasSome": [cat_ids[0]]}},
                   "sort": [{"fieldName": "firstPublishedDate", "order": "DESC"}], "paging": {"limit": 3}}}
    related = [x["id"] for x in requests.post(f"{BASE}/blog/v3/posts/query", headers=H, json=q).json()["posts"]]

    r = requests.patch(f"{BASE}/blog/v3/draft-posts/{cfg['id']}", headers=H, json={
        "draftPost": {"richContent": {"nodes": nodes, "metadata": d["richContent"].get("metadata", {"version": 1})},
                      "categoryIds": cat_ids, "tagIds": [tags[t] for t in cfg["tags"]],
                      "relatedPostIds": related, "excerpt": cfg["excerpt"]},
        "fieldMask": "richContent,categoryIds,tagIds,relatedPostIds,excerpt"})
    print(d["title"][:30], "本文・分類:", r.status_code, "" if r.ok else r.text[:300])
    c.set_seo(cfg["id"], {"title": d["title"], "excerpt": cfg["excerpt"], "focus_keyword": cfg["keyword"]})


if __name__ == "__main__":
    tags = {x["label"]: x["id"] for x in requests.get(f"{BASE}/blog/v3/tags?paging.limit=100", headers=H).json()["tags"]}
    for cfg in POSTS:
        fix(cfg, tags)
