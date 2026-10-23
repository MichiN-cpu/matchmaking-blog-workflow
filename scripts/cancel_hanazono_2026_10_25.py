"""10/25（日）花園日曜市が雨予報で中止→公開済みの告知ブログ2本を「中止のお知らせ」に書き換えて再公開する。
使い方: python3 cancel_hanazono_2026_10_25.py asunaru|nlp
"""
import sys
import requests

from post_keikaku_josei_dansei_2026_09_common import sp, nid
from post_hanazono_2026_10_25 import SITES, headers, WIX_BASE

DRAFT_IDS = {
    "asunaru": "944d9ed2-615e-46df-b0e7-b73c112d4313",
    "nlp": "37cb9991-919e-4fb0-beb4-9f1ff256644f",
}
TITLES = {
    "asunaru": "【中止】10月25日（日）花園日曜市のワンコイン婚活カウンセリングはお休みです",
    "nlp": "【中止】10月25日（日）松山花園日曜市のワンコインカウンセリングはお休みです",
}
EXCERPT = "10月25日（日）の花園日曜市は、雨予報のため中止になりました。楽しみにしてくださっていた皆さま、ありがとうございます。次回は11月22日（日）の出店を予定しています。"


def bold(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": [{"type": "BOLD", "fontWeightValue": 700}]}}
    ], "paragraphData": {}}


def notice():
    return [
        bold("【お知らせ】10月25日（日）の花園日曜市は、雨予報のため中止になりました☔"), sp(),
        bold("楽しみにしてくださっていた皆さま、本当にありがとうございます。"), sp(),
        bold("次回は11月22日（日）の出店を予定しています。決まり次第、ブログとインスタでお知らせしますね。"), sp(),
        bold("それまでの間に話してみたいことがあれば、この記事のいちばん下から無料相談もお気軽にどうぞ。"), sp(),
        {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {"lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"}},
        sp(),
    ]


def run(key):
    cfg, did = SITES[key], DRAFT_IDS[key]
    h = headers(cfg["site_id"])
    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{did}?fieldsets=RICH_CONTENT", headers=h, timeout=30)
    r.raise_for_status()
    d = r.json()["draftPost"]
    nodes = d["richContent"]["nodes"]
    if "中止" in str(nodes[:3]):
        print(key, "すでに中止のお知らせ入り。スキップ"); return
    seo = d.get("seoData") or {}
    seo["tags"] = [{"type": "title", "children": TITLES[key]},
                   {"type": "meta", "props": {"name": "description", "content": EXCERPT}}]
    body = {"draftPost": {
        "title": TITLES[key], "excerpt": EXCERPT,
        "richContent": {"nodes": notice() + nodes, "metadata": d["richContent"].get("metadata", {"version": 1})},
        "seoData": seo,
    }, "fieldMask": "title,excerpt,richContent,seoData"}
    r = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{did}", headers=h, json=body, timeout=30)
    print(key, "書き換え:", "完了" if r.ok else f"失敗 {r.status_code} {r.text[:300]}")
    if not r.ok:
        return
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts/{did}/publish", headers=h, json={}, timeout=30)
    print(key, "再公開:", "完了" if r.ok else f"失敗 {r.status_code} {r.text[:300]}")
    if r.ok:
        print("  ", r.json().get("postId"))


if __name__ == "__main__":
    run(sys.argv[1])
