"""9/27（日）花園日曜市 出店告知ブログ2本（あすなる愛媛・NLP island）をWixに下書き保存する。
写真はテントの実写（前回NLP island記事で使用）に日付を焼き込んだもの。publish:false。
使い方: python3 post_hanazono_2026_09_27.py asunaru|nlp
"""
import os
import sys
import requests

from post_keikaku_josei_dansei_2026_09_common import (
    sp, p, section_heading, link_node_centered, real_photo_node, nid,
)

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_BASE = "https://www.wixapis.com"
D = os.path.join(os.path.dirname(__file__), "..", "drafts", "hanazono_2026-09")
TENT_PHOTO_ID = "a4e52d_387f411d43f841158d1cfdd55dbbd49a~mv2.jpeg"


def photo_node(media_id, w, h, caption="", size="CONTENT"):
    return {"type": "IMAGE", "id": nid(), "nodes": [], "imageData": {
        "image": {"src": {"id": media_id}, "width": w, "height": h},
        "caption": caption,
        "containerData": {"width": {"size": size}, "alignment": "CENTER"},
    }}


def event_info(extra_place=""):
    return [
        p("日時：9月27日（日）10時〜15時"), sp(),
        p("場所：愛媛県松山市・花園通り（伊予鉄道・松山市駅の正面〜城山公園まで）"), sp(),
        p("テント名：ワンコインカウンセリング"), sp(),
        p("料金：500円 / 20分"), sp(),
        p("予約：不要です。当日そのままテントへお越しください"),
    ]


def body_asunaru():
    n = [
        p("こんにちは！松山市駅から徒歩3分。"), sp(),
        p("あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"), sp(),
        p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"), sp(),
        p("秋分の日も過ぎて、朝晩はすっかり秋らしくなってきましたね。お散歩が気持ちいい季節です🍂"), sp(),
        p("今日は、うれしい告知のお知らせです！"), sp(),
        p("9月27日（日）、花園通りで開催される花園日曜市に、今月もあすなる愛媛の「ワンコインカウンセリング」のテントを出します。"),
        sp(), "PHOTO",
    ]
    n += section_heading("9月27日（日）花園日曜市 出店内容")
    n += [sp()] + event_info()
    n += section_heading("こんな方に来てほしいなぁ")
    n += [
        sp(), p("「婚活って、どこから始めたらいいんだろう」とワクワク半分で考えている方。"), sp(),
        p("「結婚相談所って、実際どんな感じなのかな」と気になっていた方。"), sp(),
        p("「誰かにちょっと話を聞いてほしいけれど、いきなり本格的な相談はハードルが高い」という方。"), sp(),
        p("そして、それだけじゃないんです。"), sp(),
        p("夫婦関係のこと、片思いのこと、マッチングアプリの婚活のこと、他の結婚相談所で活動中の方のちょっとした相談——どれも大歓迎です。"), sp(),
        p("私は公認心理師のカウンセラーでもあるので、恋愛や人間関係のことなら何でも一緒に考えます。「こんなこと相談していいのかな」と思うものほど、気軽に持ってきてくださいね（笑）。"),
    ]
    n += section_heading("20分で、気持ちがふっと軽くなる")
    n += [
        sp(), p("500円で20分。「ちょっと話してみる」だけで大丈夫です。"), sp(),
        p("話しているうちに、自分が本当はどうしたいのかが見えてきて、「なんだ、次はこうしてみればいいんだ」と表情が明るくなって帰っていかれる方がたくさんいらっしゃいます。"), sp(),
        p("そして今、あすなる愛媛では入会金11,000円OFFキャンペーンを10月18日まで実施中です。テントで「実は相談所も気になっていて」と声をかけてくださったら、そのままゆっくりご説明しますね。"), sp(),
        p("秋の花園通りのお散歩がてら、ぜひ気軽にのぞいてみてください。テントで笑顔でお待ちしています♪"),
        sp(), real_photo_node(), sp(),
        link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", CTA_ASUNARU),
        link_node_centered(CTA_ASUNARU, CTA_ASUNARU, underline=True),
    ]
    return n


def body_nlp():
    n = [
        p("愛媛県松山市駅から徒歩3分の心理カウンセリングルーム、公認心理師でコミュニケーション心理学NLPトレーナーの中嶋です。"), sp(),
        p("秋分の日も過ぎて、朝晩の風がすっかり秋らしくなってきましたね🍂"), sp(),
        p("そんな9月27日（日）、松山市駅前の花園通りで開催される松山花園日曜市に、今月も「ワンコインカウンセリング」として出店いたします🌿"),
        sp(), "PHOTO",
    ]
    n += section_heading("9月27日（日）松山花園日曜市 出店内容")
    n += [sp()] + event_info() + [sp(), p("お買い物やお散歩の途中に、ふらっと立ち寄っていただけます🌸")]
    n += section_heading("話すことで、自分の心が見えてくる")
    n += [
        sp(), p("毎日の生活の中で、心の中に小さな疲れがたまっていくことがあります。"), sp(),
        p("職場で気をつかいすぎてしまう。家族やパートナーに言いたいことを飲み込んでしまう。なんとなく頭の中が落ち着かない。"), sp(),
        p("はっきりした悩みとして言葉にしにくいからこそ、誰かに少し話してみると、自分でも気づいていなかった気持ちがすっと見えてくることがあります。"), sp(),
        p("コミュニケーション心理学NLPでは、心の状態は頭の中の言葉・イメージ・身体の感覚とつながっていると考えます。だから、自分にかけている言葉を少し変えるだけで、気持ちも身体もふっと軽くなるんです。"), sp(),
        p("実は私自身、今朝のモーニングジャーナルで「どうせ考えるなら、前向きで明るいほうを考えよう」と改めて決めたところです。考え方の癖は、いくつになっても、今日からでも変えていけます😊"),
    ]
    n += section_heading("こんなことを話していただけます")
    n += [
        sp(), p("人間関係で気をつかいすぎて疲れる"), sp(),
        p("家族やパートナーとのコミュニケーションをもっと楽にしたい"), sp(),
        p("職場のストレスを少し整理したい"), sp(),
        p("自分の気持ちを言葉にしてみたい"), sp(),
        p("カウンセリングを一度体験してみたい"), sp(),
        p("相談内容がまとまっていなくても大丈夫です。「何から話したらいいかわからないんですが」から、一緒に整理していきましょう。20分の中で、ひとつだけテーマを決めて話してみるのもおすすめです⭐"),
    ]
    n += section_heading("最後に")
    n += [
        sp(), p("9月27日（日）10時〜15時、松山市駅前の花園通りでお待ちしています。テント名は「ワンコインカウンセリング」です。"), sp(),
        p("カウンセリングは、特別な人だけのものではありません。秋の心地よい一日に、自分の気持ちを整える時間として使っていただけたら嬉しいです🌿"),
        sp(), real_photo_node(), sp(),
        p("また、当カウンセリングルームでは、「このカウンセラーが自分に合うかな」を確かめていただける30分無料相談枠もご用意しています。"), sp(),
        link_node_centered("▶ 30分無料相談はこちら", CTA_NLP),
        link_node_centered(CTA_NLP, CTA_NLP, underline=True), sp(),
        p("あなたが安心して、自分の気持ちを話せるきっかけになりますように😊✨"),
    ]
    return n


CTA_ASUNARU = "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=referral&utm_campaign=hanazono_2026-09"
CTA_NLP = "https://www.nlp-island.jp/contact"

SITES = {
    "asunaru": {
        "site_id": "d01daac5-b796-4bd3-b09b-6d9bbcc37573",
        "member_id": "69e25236-d316-4da8-92e4-f500aca1fe37",
        "title": "9月27日（日）花園日曜市に出店します！ワンコイン婚活カウンセリング、予約なしで気軽にどうぞ",
        "excerpt": "9月27日（日）10時〜15時、松山市駅前の花園通りで開かれる花園日曜市に「ワンコインカウンセリング」のテントを出します。500円・20分・予約不要。婚活や恋愛、人間関係のことを、プロの心理カウンセラーで仲人の中嶋美知に気軽に話してみませんか。",
        "focus_keyword": "松山市 花園日曜市 婚活 カウンセリング",
        "category_ids": ["fc247847-d52b-438c-ab23-95bae771dc0a"],
        "tag_ids": ["a8fd177f-b3ba-4a57-9f81-c26ba1ec0488", "4e0145e6-4a1a-4f18-aee3-859a6eb18b17"],
        "prev_post": "e8ae6d1a-58cb-48e7-9686-6a3e18ea6d03",
        "cover": "cover_asunaru.png",
        "caption": "花園通りのテントで、笑顔でお待ちしています",
        "body": body_asunaru,
    },
    "nlp": {
        "site_id": "c6047abe-2154-443e-af5d-c1aab099c33e",
        "member_id": "001c1c1d-7ed3-43b7-bb02-d301f9417857",
        "title": "9月27日（日）松山花園日曜市に出店します｜気持ちを少し話せるワンコインカウンセリング",
        "excerpt": "9月27日（日）10時〜15時、松山市駅前の花園通りで開かれる松山花園日曜市に「ワンコインカウンセリング」で出店します。500円・20分・予約不要。人間関係や日々のモヤモヤを、公認心理師・NLPトレーナーに気軽に話してみませんか。",
        "focus_keyword": "松山市駅 カウンセリング",
        "category_ids": [],
        "tag_ids": ["493d8dab-648d-4b7d-be2f-906734d17f86", "d77c0d01-32d7-4adc-ad0d-d4a2b6b0e818", "d2417ae7-58ef-43d4-a94f-a506d84d2b92", "b7e9a319-b9a5-414f-96e3-6dc4e925ddbc", "0db1488a-5578-45e9-9c81-ae789974d3ba", "84f0f74f-15ef-4209-9168-34a01532982d", "e7c85d3e-2c49-41ee-8b37-0e3df1cb12b1"],
        "related": ["e7c8675f-34a4-455d-9574-9140f9acdc36", "a829dbdc-42e5-4658-8984-497f89b8db2d", "bc01ae3e-3935-4d6d-8ea7-066cdd51080a"],
        "cover": "cover_nlp.png",
        "caption": "花園通りで、心が少し軽くなる相談の時間を🌿",
        "body": body_nlp,
    },
}


def headers(site_id):
    return {"Authorization": WIX_API_KEY, "wix-site-id": site_id, "Content-Type": "application/json"}


def upload(cfg, filename):
    h = headers(cfg["site_id"])
    r = requests.post(f"{WIX_BASE}/site-media/v1/files/generate-upload-url", headers=h,
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


def related_asunaru(cfg):
    r = requests.post(f"{WIX_BASE}/blog/v3/posts/query", headers=headers(cfg["site_id"]), json={
        "query": {"filter": {"categoryIds": {"$hasSome": cfg["category_ids"]}},
                  "sort": [{"fieldName": "firstPublishedDate", "order": "DESC"}], "paging": {"limit": 5}}}, timeout=30)
    ids = [x["id"] for x in r.json().get("posts", []) if x["id"] != cfg["prev_post"]]
    return [cfg["prev_post"]] + ids[:2]


def run(key):
    cfg = SITES[key]
    cover = upload(cfg, cfg["cover"])
    cover_node = photo_node(cover["id"], 1536, 1024, cfg["caption"])
    nodes = [cover_node if x == "PHOTO" else x for x in cfg["body"]()]
    related = cfg.get("related") or related_asunaru(cfg)
    body = {"draftPost": {
        "title": cfg["title"],
        "richContent": {"nodes": nodes, "metadata": {"version": 1}},
        "categoryIds": cfg["category_ids"], "tagIds": cfg["tag_ids"], "relatedPostIds": related,
        "excerpt": cfg["excerpt"], "memberId": cfg["member_id"],
        "media": {"wixMedia": {"image": {"id": cover["id"], "url": cover["url"], "width": 1536, "height": 1024}},
                  "displayed": True, "custom": True},
    }, "publish": False}
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=headers(cfg["site_id"]), json=body, timeout=30)
    if not r.ok:
        print("下書き作成失敗:", r.status_code, r.text[:500]); return
    did = r.json()["draftPost"]["id"]
    seo = {"draftPost": {"seoData": {
        "tags": [{"type": "title", "children": cfg["title"]},
                 {"type": "meta", "props": {"name": "description", "content": cfg["excerpt"]}}],
        "settings": {"preventAutoRedirect": False, "keywords": [{"term": cfg["focus_keyword"], "isMain": True}]}}},
        "fieldMask": "seoData"}
    rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{did}", headers=headers(cfg["site_id"]), json=seo, timeout=30)
    print("SEO:", "完了" if rp.ok else f"失敗 {rp.status_code} {rp.text[:200]}")
    print(f"下書きID {did}")
    print(f"編集URL https://manage.wix.com/dashboard/{cfg['site_id']}/blog/post/{did}")


if __name__ == "__main__":
    run(sys.argv[1])
