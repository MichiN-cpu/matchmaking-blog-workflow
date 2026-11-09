"""
お休みのお知らせ（11/17〜21・新婚旅行）。Wixには下書き保存のみ（publish:false）。
本文はデスクトップ「お休みのお知らせ_11月17日〜21日.txt」の【A】ブログ（みっちゃんOK済み 11/9）。
"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_omiai_josei_2026_10_14 as base
import post_norichan_2026_11 as nori
c = base.c
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "drafts", "oyasumi_2026-11")
SRC = os.path.expanduser("~/Desktop/お休みのお知らせ_11月17日〜21日.txt")
CAT_OSHIRASE = "fc247847-d52b-438c-ab23-95bae771dc0a"
EXCERPT = "11月17日（火）〜21日（土）は、新婚旅行のためお休みをいただきます。期間中のお問い合わせは11月22日（日）から順にお返事いたします。会員さまのサポートは通常どおりです。"
LINKS = {"https://www.asunaru.jp/soudan": "https://www.asunaru.jp/soudan",
         "https://line.me/R/ti/p/@505atdkw": "https://line.me/R/ti/p/@505atdkw",
         "de-sign@nlp-island.jp": "mailto:de-sign@nlp-island.jp",
         "089-948-9606": "tel:0899489606"}

def link_p(text, url):
    return {"type": "PARAGRAPH", "id": c.nid(), "paragraphData": {}, "nodes": [{"type": "TEXT", "id": c.nid(), "nodes": [],
            "textData": {"text": text, "decorations": [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}, {"type": "UNDERLINE"}]}}]}

def run():
    src = open(SRC, encoding="utf-8").read()
    a = src.split("■タイトル\n", 1)[1].split("━━━━", 1)[0]
    title, body = a.split("\n■本文\n", 1)
    title = title.strip()
    nodes = []
    for block in [b for b in body.strip().split("\n\n") if b.strip()]:
        if nodes: nodes.append(c.sp())
        for line in block.strip().split("\n"):
            line = line.strip()
            nodes.append(link_p(line, LINKS[line]) if line in LINKS else c.p(line))
    assert not any("http" in str(n) and n["nodes"][0]["textData"]["decorations"] == [] for n in nodes if n["type"] == "PARAGRAPH" and n["nodes"])
    body = {"draftPost": {"title": title, "richContent": {"nodes": nodes, "metadata": {"version": 1}},
            "categoryIds": [CAT_OSHIRASE], "tagIds": nori.tag_ids(["お知らせ", "結婚報告"]),
            "excerpt": EXCERPT, "memberId": c.MEMBER_ID}, "publish": False}
    r = requests.post(f"{c.WIX_BASE}/blog/v3/draft-posts", headers=c.wix_headers(), json=body, timeout=30)
    print("draft create:", r.status_code); r.raise_for_status()
    did = r.json()["draftPost"]["id"]
    c.set_seo(did, {"title": title, "excerpt": EXCERPT, "focus_keyword": "あすなる愛媛 お休み"})
    cov = c.upload_image_file(os.path.join(D, "cover_oyasumi.png"), "2026-11-17_oyasumi_cover.png")
    mp = {"draftPost": {"media": {"custom": True, "wixMedia": {"image": {"id": cov.get("id", ""), "url": cov["url"],
          "height": 1024, "width": 1536, "filename": "2026-11-17_oyasumi_cover.png"}}, "displayed": True}}, "fieldMask": "media"}
    print("cover:", requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(), json=mp, timeout=30).status_code)
    print("seoSlug:", requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(),
          json={"draftPost": {"seoSlug": "oyasumi-2026-11-17"}, "fieldMask": "seoSlug"}, timeout=30).status_code)
    print("DRAFT_ID =", did); print(f"https://manage.wix.com/dashboard/{c.WIX_SITE_ID}/blog/post/{did}")

if __name__ == "__main__":
    run()
