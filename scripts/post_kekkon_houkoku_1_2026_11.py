"""
【特別編】結婚報告① 氏神様で神前挙式（2026-11-23(月・祝) 9:00 想定）。Wixには下書き保存のみ（publish:false）。
みっちゃん口述→ジェイ下書き→みっちゃん加除修正（11/8）。写真はすべて本人提供の実写（AI生成なし）。
共通ロジックは post_omiai_josei_2026_10_14.py / tag_ids は post_norichan_2026_11.py。
使い方: python3 post_kekkon_houkoku_1_2026_11.py     検証のみ: --verify <DRAFT_ID>
"""
import os, re, sys, requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_omiai_josei_2026_10_14 as base
import post_norichan_2026_11 as nori
c = base.c

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "drafts", "kekkon-houkoku_2026-11")
MD = os.path.join(D, "kekkon1_ujigami.md")
SLUG = "2026-11-23_kekkon-houkoku_1"
SEO_SLUG = "ujigami-shinzen-shiki"
CTA_URL = "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-11-23-kekkon-houkoku-1"

CAT_JIKO = "133a60f7-a603-431d-8ca9-8ec82c2294c5"    # 自己紹介
CAT_SAIKON = "bc14935b-78aa-4ee4-85bf-35ac04874fb3"  # 再婚の婚活
CAT_SENIOR = "a65acc05-b781-4ec9-95d7-66c9daefc19f"  # シニアの婚活

EXCERPT = ("57歳で婚活を始めた仲人・中嶋美知が、59歳の秋、生まれ育った町の氏神様で神前挙式を挙げました。"
           "ひっそりのつもりが、友人たちのサプライズで笑顔あふれる一日に。人と土地とのつながりに見守られて、新しい暮らしが始まります。")
FOCUS = "50代 再婚 神前式"
TAGS = ["婚活", "再婚", "シニア婚活", "結婚報告", "神前式", "氏神様", "57歳仲人婚活始めました", "パートナーシップ"]
COVER = "cover_composed.png"
RELATED = ["771006c5-5963-457e-b7c9-cdf514e0a0ac",   # 57歳仲人、婚活始めました。（第１話）
           "1e4d8345-f803-4522-b7d8-37cf8dbbb1dc",   # 同（第2話）
           "02c1c45f-9569-4010-9371-93e93447abb5"]   # 一緒に暮らせない結婚なんて…

# 本文中の文字列 → リンク（表示は名前だけ、URLは本文から外す）
LINKS = {
    "モクレンフォトスタジオさん(https://mokuren-photo.com/)": ("モクレンフォトスタジオさん", "https://mokuren-photo.com/"),
    "山田先生(https://www.instagram.com/kitsuke__ymd?utm_source=ig_web_button_share_sheet&xtok=ZDNlZDc0MzIxNw==)":
        ("山田先生", "https://www.instagram.com/kitsuke__ymd/"),
}

# この行の直後に写真を入れる（本人提供の実写）
PHOTOS = [
    ("59歳と61歳、嬉し恥ずかしのアラ還夫婦です（笑）", "p_ferry.jpg"),
    ("そんなふうに、ひとつ、またひとつと、ご縁がつながっていきました。", "p_bouquet1.jpg"),
    ("お花も、風船も、たくさんいただいちゃって🌸🎈", "p_flowers.jpg"),
    ("お花も、風船も、たくさんいただいちゃって🌸🎈", "p_balloons.jpg"),
    ("よく知った空、よく知った海、よく知った港、よく知った夕日。", "p_sunset.jpg"),
    ("そのありがたさを、この年齢になって、身をもって味わわせてもらいました。", "p_bouquet2.jpg"),
]


def p_links(line):
    for raw, (label, url) in LINKS.items():
        if raw in line:
            pre, post = line.split(raw, 1)
            texts = []
            if pre:
                texts.append({"type": "TEXT", "id": c.nid(), "nodes": [], "textData": {"text": pre, "decorations": []}})
            texts.append({"type": "TEXT", "id": c.nid(), "nodes": [], "textData": {"text": label, "decorations": [
                {"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}, {"type": "UNDERLINE"}]}})
            if post:
                texts.append({"type": "TEXT", "id": c.nid(), "nodes": [], "textData": {"text": post, "decorations": []}})
            return {"type": "PARAGRAPH", "id": c.nid(), "nodes": texts, "paragraphData": {}}
    assert "http" not in line, f"未処理のURLがあります: {line[:30]}"
    return c.p(line)


def build(blocks, images):
    nodes = []
    for b in (x.strip() for x in blocks):
        if b.startswith("## "):
            nodes.extend(c.section_heading(b[3:].strip())); continue
        if nodes:
            nodes.append(c.sp())
        if b == "―――":
            nodes.extend([c.divider_node()]); continue
        if b == base.PHOTO_PLACEHOLDER:
            nodes.append(c.real_photo_node()); continue
        if b.startswith("⬇️"):
            nodes.extend(c.cta_nodes(CTA_URL)); continue
        for line in (l.strip() for l in b.split("\n")):
            if not line:
                continue
            nodes.append(p_links(line))
            for fo in images.get(line, []):
                nodes.extend([c.sp(), c.image_node(fo), c.sp()])
    return nodes


def run():
    title, blocks = base.load_draft(MD)
    all_lines = [l.strip() for b in blocks for l in b.split("\n")]
    images = {}
    for i, (after, fn) in enumerate(PHOTOS, 1):
        assert all_lines.count(after) == 1, f"挿入位置が一意でない: {after[:20]}"
        fo = c.upload_image_file(os.path.join(D, fn), f"{SLUG}_{i}_{fn}", mime="image/jpeg")
        assert fo, f"upload failed: {fn}"
        images.setdefault(after, []).append(fo)
    nodes = build(blocks, images)
    body = {"draftPost": {"title": title, "richContent": {"nodes": nodes, "metadata": {"version": 1}},
            "categoryIds": [CAT_JIKO, CAT_SAIKON, CAT_SENIOR], "tagIds": nori.tag_ids(TAGS),
            "relatedPostIds": RELATED, "excerpt": EXCERPT, "memberId": c.MEMBER_ID}, "publish": False}
    r = requests.post(f"{c.WIX_BASE}/blog/v3/draft-posts", headers=c.wix_headers(), json=body, timeout=30)
    print("draft create:", r.status_code)
    if not r.ok:
        print(r.text[:500]); r.raise_for_status()
    did = r.json()["draftPost"]["id"]
    c.set_seo(did, {"title": title, "excerpt": EXCERPT, "focus_keyword": FOCUS})

    cov = c.upload_image_file(os.path.join(D, COVER), f"{SLUG}_cover.png")
    assert cov, "cover upload failed"
    mp = {"draftPost": {"media": {"custom": True, "wixMedia": {"image": {
          "id": cov.get("id", ""), "url": cov["url"], "height": cov.get("height", 1024),
          "width": cov.get("width", 1536), "filename": f"{SLUG}_cover.png"}}, "displayed": True}},
          "fieldMask": "media"}
    print("cover:", requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(), json=mp, timeout=30).status_code)
    r = requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(),
                       json={"draftPost": {"seoSlug": SEO_SLUG}, "fieldMask": "seoSlug"}, timeout=30)
    print("seoSlug:", r.status_code)
    base.verify(did, CTA_URL)
    print("DRAFT_ID =", did)
    print(f"https://manage.wix.com/dashboard/{c.WIX_SITE_ID}/blog/post/{did}")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        base.verify(sys.argv[2], CTA_URL)
    else:
        run()
