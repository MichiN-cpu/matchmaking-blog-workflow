"""9/29（火）ハピラブLabo（ココカラダイガクさんと共催）の告知ブログを、あすなる愛媛のWixに下書き保存する。
画像は前回（2025-09-28）のチラシの日付帯だけ差し替えたもの。publish:false。
使い方: python3 post_hapilove_2026_09_29.py
"""
import os
import requests

from post_keikaku_josei_dansei_2026_09_common import (
    sp, p, section_heading, link_node_centered, real_photo_node, nid,
)

WIX_API_KEY = os.environ["WIX_API_KEY"]
WIX_BASE = "https://www.wixapis.com"
D = os.path.join(os.path.dirname(__file__), "..", "drafts", "hapilove_2026-09-29")
COVER = "hapilove_2026-09-29_square.png"

SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
MEMBER_ID = "69e25236-d316-4da8-92e4-f500aca1fe37"
CTA_ASUNARU = "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=referral&utm_campaign=hapilove_2026-09"
LINE_URL = "https://lin.ee/PEixgsD"

TITLE = "9月29日（火）午前は「ハピラブLabo」へ｜恋愛・婚活・結婚をもっとハッピーにするおしゃべり会"
EXCERPT = ("9月29日（火）10時〜12時、松山市駅から徒歩3分の花園町オフィスで「ハピラブLabo」を開催します。"
           "ココカラダイガクさんとの共催で、参加費は1,000円。恋愛・婚活・結婚のワクワクもお悩みも、みんなでおしゃべりしましょう。")
FOCUS_KEYWORD = "松山市 婚活 イベント"
CATEGORY_IDS = ["fc247847-d52b-438c-ab23-95bae771dc0a"]
TAG_IDS = ["15b9f04d-03e6-4649-a32b-dec43d522bee", "10dc8abd-4250-4356-a7ad-9f4465502257",
           "5b192801-25d6-4067-98d5-c7405fc91d17", "e00fdb14-3f82-4569-9c70-a7226cb7d058",
           "a8fd177f-b3ba-4a57-9f81-c26ba1ec0488"]
# 過去のハピラブLabo記事（どんなところ？／6月のお悩み解決／前回9/28の告知）
RELATED = ["c46c4153-8d85-4cfd-9e75-17b7588da3af", "5ded415e-9cc3-4f02-969f-e0fa5b36070c",
           "a8e0899a-d330-476b-ac54-bd3089e0b1ed"]


def photo_node(media_id, w, h, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [], "imageData": {
        "image": {"src": {"id": media_id}, "width": w, "height": h},
        "caption": caption,
        "containerData": {"width": {"size": "SMALL"}, "alignment": "CENTER"},
    }}


def link_node(text, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": [
            {"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]}}
    ], "paragraphData": {}}


def body(cover_node):
    n = [
        p("こんにちは！松山市駅から徒歩3分。"), sp(),
        p("あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"), sp(),
        p("今日は、急きょ決まったうれしいお知らせです！"), sp(),
        p("ココカラダイガクさんからのお声がけで、9月29日（火）の午前中に「ハピラブLabo（Happy Love研究所）」を開催することになりました💓"),
        sp(), cover_node,
    ]
    n += section_heading("9月29日（火）ハピラブLabo 開催内容")
    n += [
        sp(), p("日時：2026年9月29日（火）10時〜12時"), sp(),
        p("会場：花園町オフィス（松山市花園町4-11 吉田ビル3階東）"), sp(),
        p("参加費：1,000円（税込）"), sp(),
        p("共催：ココカラダイガク"), sp(),
        p("お申し込み：公式LINEかInstagramのDMに「ハピラブ参加」とメッセージをくださいね。メール（de-sign@nlp-island.jp）でも受け付けています。"),
    ]
    n += section_heading("ハピラブLaboってどんな場所？")
    n += [
        sp(), p("既に幸せな人も、これから幸せになる人も。恋愛・婚活・結婚のことを、みんなでおしゃべりする会です。"), sp(),
        p("ワクワクも、お悩みも、お惚気も、「誰かをサポートしたい」気持ちも、おふざけも真剣な話も、なんでもOK！"), sp(),
        p("これまでのハピラブLaboには、婚活中の方、ご成婚された方、お子さんのご結婚を願う親御さん、コミュニケーションのプロなど、いろいろな立場の方が集まってくださいました。"), sp(),
        p("自分とは違う経験を聞くと、「そんな考え方もあるんだ！」と視点がくるっと変わる瞬間があるんです。みんなで集まれば文殊の知恵で、いつも笑い声の絶えない時間になります😊"),
    ]
    n += section_heading("平日の午前中だからこそ、ゆったりと")
    n += [
        sp(), p("今回は火曜日の10時からの2時間です。"), sp(),
        p("お仕事がお休みの方、午前中に少し時間がとれる方、子育てがひと段落した方にも来ていただきやすい時間帯になりました。"), sp(),
        p("あなたの経験が、誰かの人生を変えちゃうかもしれません。そして、誰かのひと言が、あなたの明日をふっと明るくしてくれるかもしれません。"), sp(),
        p("そんなあたたかい循環が生まれる場所で、お会いできるのを楽しみにしています🎵"), sp(),
        p("なお、あすなる愛媛では入会金11,000円OFFキャンペーンを10月18日まで実施中です。「相談所のことも少し聞いてみたい」という方も、どうぞ気軽に声をかけてくださいね。"),
        sp(), link_node("▶ あすなる愛媛の結婚相談所 公式LINEはこちら", LINE_URL),
        sp(), real_photo_node(), sp(),
        link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", CTA_ASUNARU),
        link_node_centered(CTA_ASUNARU, CTA_ASUNARU, underline=True),
    ]
    return n


def headers():
    return {"Authorization": WIX_API_KEY, "wix-site-id": SITE_ID, "Content-Type": "application/json"}


def upload(filename):
    r = requests.post(f"{WIX_BASE}/site-media/v1/files/generate-upload-url", headers=headers(),
                      json={"mimeType": "image/png", "displayName": filename}, timeout=30)
    r.raise_for_status()
    data = r.json()
    url = data["uploadUrl"]
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if data.get("uploadToken"):
        hdrs["Authorization"] = data["uploadToken"]
    sep = "&" if "?" in url else "?"
    up = requests.put(f"{url}{sep}filename={filename}", data=open(os.path.join(D, filename), "rb").read(),
                      headers=hdrs, timeout=120)
    up.raise_for_status()
    f = up.json()["file"]
    print("  画像アップロード:", f["id"])
    return f


def run():
    cover = upload(COVER)
    cover_node = photo_node(cover["id"], 1080, 1080, "既に幸せな人も、これから幸せになる人も💓")
    b = {"draftPost": {
        "title": TITLE,
        "richContent": {"nodes": body(cover_node), "metadata": {"version": 1}},
        "categoryIds": CATEGORY_IDS, "tagIds": TAG_IDS, "relatedPostIds": RELATED,
        "excerpt": EXCERPT, "memberId": MEMBER_ID,
        "media": {"wixMedia": {"image": {"id": cover["id"], "url": cover["url"], "width": 1080, "height": 1080}},
                  "displayed": True, "custom": True},
    }, "publish": False}
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=headers(), json=b, timeout=30)
    if not r.ok:
        print("下書き作成失敗:", r.status_code, r.text[:500]); return
    did = r.json()["draftPost"]["id"]
    seo = {"draftPost": {"seoData": {
        "tags": [{"type": "title", "children": TITLE},
                 {"type": "meta", "props": {"name": "description", "content": EXCERPT}}],
        "settings": {"preventAutoRedirect": False, "keywords": [{"term": FOCUS_KEYWORD, "isMain": True}]}}},
        "fieldMask": "seoData"}
    rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{did}", headers=headers(), json=seo, timeout=30)
    print("SEO:", "完了" if rp.ok else f"失敗 {rp.status_code} {rp.text[:200]}")
    print(f"下書きID {did}")
    print(f"編集URL https://manage.wix.com/dashboard/{SITE_ID}/blog/post/{did}")


if __name__ == "__main__":
    run()
