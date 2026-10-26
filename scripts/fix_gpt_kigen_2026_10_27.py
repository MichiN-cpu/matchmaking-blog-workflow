"""
ChatGPT作成の下書き「【女性向け】だいたい機嫌がいい人を選んだ。」の本文差し替え（2026-10-27）
- 本文はみっちゃん手入れ済みの修正案（デスクトップ「ブログ修正案_だいたい機嫌がいい人.txt」）に差し替え
- 画像3枚・参考リンク・CTAは元の下書きのノードをそのまま使う
- 抜けていたタグ・関連記事・SEO（フォーカスキーワード）を補完
"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(__file__))
import post_keikaku_josei_dansei_2026_09_common as c

DRAFT_ID = "e3109345-c32b-4835-9c05-b0b7da8d46d1"
SRC = os.path.expanduser("~/Desktop/ブログ修正案_だいたい機嫌がいい人.txt")
BASE = "https://www.wixapis.com"
H = c.wix_headers()
TAG_LABELS = ["婚活マインド", "女性心理", "自己肯定感", "心理学", "NLP", "お見合い",
              "パートナーシップ", "コミュニケーション", "素直婚", "松山市"]
FOCUS_KEYWORD = "婚活 相手選び"


def text_of(n):
    return "".join(t.get("textData", {}).get("text", "") if t["type"] == "TEXT" else text_of(t) for t in n.get("nodes", []))


def main():
    d = requests.get(f"{BASE}/blog/v3/draft-posts/{DRAFT_ID}?fieldsets=RICH_CONTENT", headers=H).json()["draftPost"]
    old = d["richContent"]["nodes"]
    images = [n for n in old if n["type"] == "IMAGE"]
    ref = next(n for n in old if text_of(n).startswith("参考："))
    cta = [n for n in old if "soudan" in str(n) or text_of(n).startswith("⬇️")]
    assert len(images) == 3 and len(cta) == 2

    lines = open(SRC, encoding="utf-8").read().splitlines()
    start = lines.index("こんにちは！松山市駅から徒歩3分。")
    new, img_i, pending_heading = [], 0, False
    for ln in lines[start:]:
        s = ln.strip()
        if s.startswith("⬇️") or s.startswith("https://www.asunaru.jp/soudan"):
            break
        if s.startswith("――――"):
            pending_heading = True
            continue
        if s.startswith("■ "):
            while new and text_of(new[-1]) == "" and new[-1]["type"] == "PARAGRAPH":
                new.pop()
            new += c.section_heading(s[2:])
            pending_heading = False
            continue
        if s.startswith("［画像"):
            if new and text_of(new[-1]) != "":
                new.append(c.sp())
            new.append(images[img_i]); img_i += 1
            new.append(c.sp())
            continue
        if s.startswith("参考："):
            new.append(ref); continue
        if s == "":
            if new and not (new[-1]["type"] == "PARAGRAPH" and text_of(new[-1]) == ""):
                new.append(c.sp())
            continue
        new.append(c.p(s))
    while new and text_of(new[-1]) == "":
        new.pop()
    new += [c.sp()] + cta
    assert img_i == 3

    q = {"query": {"filter": {"categoryIds": {"$hasSome": [d["categoryIds"][0]]}},
                   "sort": [{"fieldName": "firstPublishedDate", "order": "DESC"}], "paging": {"limit": 3}}}
    related = [x["id"] for x in requests.post(f"{BASE}/blog/v3/posts/query", headers=H, json=q).json()["posts"]]
    tags = {x["label"]: x["id"] for x in requests.get(f"{BASE}/blog/v3/tags?paging.limit=100", headers=H).json()["tags"]}
    tag_ids = [tags[l] for l in TAG_LABELS if l in tags]
    print("タグ未作成でスキップ:", [l for l in TAG_LABELS if l not in tags])

    r = requests.patch(f"{BASE}/blog/v3/draft-posts/{DRAFT_ID}", headers=H, json={
        "draftPost": {"richContent": {"nodes": new, "metadata": {"version": 1}},
                      "tagIds": tag_ids, "relatedPostIds": related},
        "fieldMask": "richContent,tagIds,relatedPostIds"})
    print("本文・分類:", r.status_code, "" if r.ok else r.text[:300])
    c.set_seo(DRAFT_ID, {"title": d["title"], "excerpt": d["excerpt"], "focus_keyword": FOCUS_KEYWORD})


if __name__ == "__main__":
    main()
