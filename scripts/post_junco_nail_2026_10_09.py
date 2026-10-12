"""
【女性向け】ネイルサロンの椅子から見えた、仲良し夫婦の共通点。
特別記事（junco*さん×ネイル付き特別コース）。Wixには下書き保存のみ（publish:false）。
実写3枚を本文に使用、カバーは実写（ネイル写真）＋eyecatch_composerで文字焼き込み。
"""
import os, sys, re, requests
sys.path.insert(0, os.path.dirname(__file__))
import post_keikaku_josei_dansei_2026_09_common as c
from PIL import Image

D = os.path.join(os.path.dirname(__file__), "..", "drafts", "junco_2026-10")
DRAFT = os.path.join(D, "draft_2026-10-09_junco-nail-fufu.md")
CTA_URL = "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-10-junco-nail-fufu"
LP_URL = "https://michin-cpu.github.io/asunaru-shindan/campaign/nyukaikin-off-2026-09/?utm_source=blog&utm_medium=article&utm_campaign=2026-09-nyukaikin-off-junco"
PHOTOS = {
    "1": "/Users/nakashimamichi/Desktop/juncoネイル１.jpg",
    "2": "/Users/nakashimamichi/Desktop/juncoネイル２.jpg",
    "3": "/Users/nakashimamichi/Desktop/juncoネイル10月.jpg",
}
CAPTIONS = {"1": "junco*さんのサロンにて。", "2": "施術後の手を見せて、ぱっ。", "3": "tRipnail e'te'の施術例より。"}
TITLE = "【女性向け】ネイルサロンの椅子から見えた、仲良し夫婦の共通点。――婚活中の今から、まねできることがありました"
EXCERPT = "ネイルサロンの椅子に座ると、不思議と夫婦の話が弾みます。ネイリストのjunco*さんが「仲良し夫婦が多い」と話してくれた、結婚が続く夫婦の小さな習慣を7つ。婚活中の今から、まねできるヒントとあわせてご紹介します。"
FOCUS = "婚活 仲良し夫婦 共通点"
CATEGORY_IDS = ["641187e4-a409-4c2f-9639-ecc548f26f15", "998b685d-1453-4ebd-8bd2-0218e315186e"]
RELATED = [
    "f226c440-936c-4ab0-9961-fcd06d19672a",  # 未来の夫婦は、もう今のあなたの中にいます
    "d64cb253-7097-4949-8117-805356a6d359",  # 「なんか嫌だな」を、スルーしないでいてください
    "77e61211-46b1-433b-951f-afd39bfd4168",  # その将来不安、一人で抱えなくていいのかもしれません
]
TAG_IDS = [
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "e27232c2-174e-47f8-afee-3132dcbb7516",  # 結婚生活
    "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
    "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
    "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
    "5b192801-25d6-4067-98d5-c7405fc91d17",  # 松山市
    "32413ff0-17fc-455e-93e1-3add76e9eb46",  # キャンペーン
    "8e779610-2acc-448e-b6b0-ad65dbb418d1",  # 無料相談
]


def photo_node(file_obj, caption):
    return {"type": "IMAGE", "id": c.nid(), "nodes": [], "imageData": {
        "image": {"src": {"url": file_obj["url"]}}, "caption": caption,
        "containerData": {"width": {"size": "SMALL"}, "alignment": "CENTER"}}}


def link_para(text, url):
    return {"type": "PARAGRAPH", "id": c.nid(), "nodes": [{"type": "TEXT", "id": c.nid(), "nodes": [], "textData": {
        "text": text, "decorations": [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}, {"type": "UNDERLINE"}]}}],
        "paragraphData": {}}


def build(files):
    text = open(DRAFT, encoding="utf-8").read()
    body = text.split("## 本文\n\n", 1)[1].split("\n\n---\n\n## 差し込み画像")[0]
    nodes = []
    for i, b in enumerate(body.split("\n\n")):
        if i > 0:
            nodes.append(c.sp())
        b = b.strip()
        m = re.match(r"\[写真:(\d)\]", b)
        if b.startswith("### "):
            nodes.extend(c.section_heading(b[4:].strip()))
        elif m:
            nodes.append(photo_node(files[m.group(1)], CAPTIONS[m.group(1)]))
        elif b.startswith("[リンク:"):
            url, label = b[len("[リンク:"):-1].split("|", 1)
            nodes.append(link_para(label, url))
        elif b == "[LP]":
            nodes.append(c.link_node_centered("▶ ネイル付き特別コース・入会金11,000円OFFキャンペーンの詳細はこちら", LP_URL))
            nodes.append(c.sp())
            nodes.append(c.link_node_centered(LP_URL, LP_URL, underline=True))
        elif b == "[ここに実写カウンセリング写真を挿入]":
            nodes.append(c.real_photo_node())
        elif b.startswith("⬇️"):
            nodes.extend(c.cta_nodes(CTA_URL))
        else:
            nodes.append(c.p(b))
    return nodes


if __name__ == "__main__":
    files = {}
    for k, path in PHOTOS.items():
        fo = c.upload_image_file(path, f"junco_nail_{k}.jpg", mime="image/jpeg")
        assert fo, k
        files[k] = fo
    body = {"draftPost": {"title": TITLE, "richContent": {"nodes": build(files), "metadata": {"version": 1}},
            "categoryIds": CATEGORY_IDS, "tagIds": TAG_IDS, "relatedPostIds": RELATED, "excerpt": EXCERPT,
            "memberId": c.MEMBER_ID}, "publish": False}
    r = requests.post(f"{c.WIX_BASE}/blog/v3/draft-posts", headers=c.wix_headers(), json=body, timeout=30)
    print(r.status_code, r.text[:400])
    r.raise_for_status()
    did = r.json()["draftPost"]["id"]
    c.set_seo(did, {"title": TITLE, "excerpt": EXCERPT, "focus_keyword": FOCUS})
    cov = c.upload_image_file(os.path.join(D, "cover_composed.png"), "junco_nail_cover_composed.png")
    mp = {"draftPost": {"media": {"custom": True, "wixMedia": {"image": {"id": cov.get("id", ""), "url": cov["url"],
          "height": cov.get("height", 1024), "width": cov.get("width", 1536), "filename": "cover.png"}}, "displayed": True}},
          "fieldMask": "media"}
    rm = requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(), json=mp, timeout=30)
    print("cover", rm.status_code)
    print("DRAFT_ID =", did)
    print(f"https://manage.wix.com/dashboard/{c.WIX_SITE_ID}/blog/post/{did}")
