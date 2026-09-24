"""
モーニングジャーナル第11期 お誘いブログ（あすなる愛媛版／NLP island版）
2026-09-24作成。Wixには下書き保存のみ（publish:false）

使い方:
  python3 post_morning_journal_11th.py asunaru
  python3 post_morning_journal_11th.py nlpisland

投稿ロジックは post_keikaku_josei_dansei_2026_09_common.py を流用。
BASEの申込みリンク行と、あすなる版のみのCTA・実写写真を扱うため、本文の組み立てだけこのファイルで上書きする。
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import post_keikaku_josei_dansei_2026_09_common as common

BASE_SHOP_URL = "https://cocokara2525.base.shop/items/81637029"
DRAFTS = os.path.join(os.path.dirname(__file__), "..", "drafts")

BASE_STYLE = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
              "clear skin, real-world setting, professional lifestyle photography style, shallow depth of field, "
              "clean bright modern atmosphere, no text, no numbers, no letters, no warm yellowish tint, "
              "clean bright natural daylight, crisp clean colors, vivid but neutral tones, NOT pale, NOT gloomy, NOT sepia")


def build_nodes(draft_path, cta_url, with_cta):
    text = open(draft_path, encoding="utf-8").read()
    body = text.split("## 本文\n\n", 1)[1].split("\n\n---\n\n## 差し込み画像")[0]
    nodes = []
    for i, block in enumerate(body.split("\n\n")):
        block = block.strip()
        if i > 0:
            nodes.append(common.sp())
        if block.startswith("### "):
            nodes.extend(common.section_heading(block[4:].strip()))
        elif block == "[ここに実写カウンセリング写真を挿入]":
            nodes.append(common.real_photo_node())
        elif block.startswith("⬇️ モーニングジャーナル"):
            nodes.append(common.link_node_centered(block, BASE_SHOP_URL))
        elif block == BASE_SHOP_URL:
            nodes.append(common.link_node_centered(block, BASE_SHOP_URL, underline=True))
        elif block.startswith("⬇️あなたに合った婚活を"):
            if with_cta:
                nodes.extend(common.cta_nodes(cta_url))
        else:
            nodes.append(common.p(block))
    return nodes


CFGS = {
    "asunaru": {
        "site_id": "d01daac5-b796-4bd3-b09b-6d9bbcc37573",
        "with_cta": True,
        "category_ids": ["fc247847-d52b-438c-ab23-95bae771dc0a"],  # お知らせ
        "related_post_ids": [
            "d5023baa-851c-462d-aab9-46761ef0be0b",  # 【男女共通】第10期スタート！毎朝5時45分に、自分に帰ってくる15分のはなし。
            "43d9ae43-938c-47a0-b889-e5aa397b6e07",  # AI美知仲人コーチ、誕生しました
            "e8ae6d1a-58cb-48e7-9686-6a3e18ea6d03",  # 花園通りに出ます！ワンコイン婚活カウンセリング
        ],
        "tag_ids": [
            "b2bf9e74-a740-4f75-9377-189632b532b4",  # モーニングジャーナル
            "6e84b3d4-a336-4adc-94ff-7e326267a310",  # （第10期と同じタグ）
            "d5599216-6bdd-47df-9af3-07d1c15c1539",  # 願いを叶える
            "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
            "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
            "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
        ],
        "draft_path": os.path.join(DRAFTS, "draft_2026-09-24_morning-journal-11th_asunaru.md"),
        "slug": "2026-09-24_morning-journal-11th_asunaru",
        "title": "【男女共通】「私には無理だろうなぁ」と思っていた人が、気づけば1年続けていた朝の15分。――モーニングジャーナル第11期、10月5日スタート",
        "excerpt": "「すごいなぁ、でも私には無理」。そう思っていた方が、気づけば1年続けていた朝の15分があります。毎朝5時45分からZoomでつながって、ただ書くだけ。休んでも大丈夫。モーニングジャーナル第11期は10月5日スタートです。参加者さんの声と、続けられる理由をお伝えします。",
        "focus_keyword": "朝活 モーニングジャーナル 習慣 ジャーナリング 松山",
        "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-09-24-morning-journal-11",
        "insert_after": [
            ("実は、ここだけの話なのですが（笑）。", "sec", "朝の画面の向こうに、仲間がいる。"),
            ("そして、まだ誰からの連絡も、ニュースも入ってこない朝の15分は", "hope", "書き終えたあとの、すっきりした朝。"),
        ],
    },
    "nlpisland": {
        "site_id": "c6047abe-2154-443e-af5d-c1aab099c33e",
        "with_cta": False,
        "draft_path": os.path.join(DRAFTS, "draft_2026-09-24_morning-journal-11th_nlpisland.md"),
        "slug": "2026-09-24_morning-journal-11th_nlpisland",
        "title": "「私には無理」から始まった人ほど、なぜか続いている。――朝15分のモーニングジャーナル、第11期は10月5日スタート",
        "excerpt": "早起きも、毎日書くことも、「私には無理」と思っていた方が、気づけば1年続けていた。毎朝5時45分からZoomでつながって、15分書くだけの会です。休んでも大丈夫な場が、なぜ人を変えていくのか。参加者さんの声と心理学の視点からお伝えします。第11期は10月5日スタート。",
        "focus_keyword": "モーニングジャーナル 朝活 ジャーナリング 習慣化 セルフコンパッション",
        "cta_url": "",
        "insert_after": [
            ("実は、ここだけの話なのですが（笑）。", "sec", "朝の画面の向こうに、仲間がいる。"),
            ("参加者さんの「自分の位置が見える」という言葉は", "hope", "書き終えたあとの、すっきりした朝。"),
        ],
    },
}

COMMON_IMAGES = {
    "eyecatch_prompt": (BASE_STYLE + ", early morning before sunrise, a Japanese woman in her 40s in a cozy cardigan "
        "writing peacefully in an open notebook at a wooden desk by a large window, pale blue dawn sky outside, "
        "a cup of coffee beside the notebook, calm gentle smile, wide shot, plenty of empty space in the lower left"),
    "section_prompt": ("Photorealistic still life photograph, NO people, no hands, early morning, an open notebook with a pen "
        "on a wooden desk in front of a laptop whose screen is not visible (seen from the side), a steaming cup of coffee, "
        "soft dawn light from a window, calm and quiet, crisp neutral colors, no text, no letters, no warm yellowish tint"),
    "hope_prompt": (BASE_STYLE + ", a Japanese man in his 40s sitting by a window in morning sunlight, "
        "holding a closed notebook, relaxed and refreshed expression with a gentle smile, looking out the window, not at camera"),
    "eyecatch_main_html": '「私には無理」から、<br><span class="accent">朝の15分</span>が続いた理由。',
    "eyecatch_subtitle": "――モーニングジャーナル第11期 10月5日スタート",
    "eyecatch_main_size": 46,
}


def run(which):
    cfg = dict(CFGS[which], **COMMON_IMAGES)
    common.WIX_SITE_ID = cfg["site_id"]
    common.build_nodes_from_draft = lambda path, cta_url: build_nodes(path, cta_url, cfg["with_cta"])
    if which == "asunaru":
        common.CATEGORY_IDS = cfg["category_ids"]
        common.RELATED_POST_IDS = cfg["related_post_ids"]
    else:
        # office de・Sign（NLP island）サイト。投稿者・カテゴリはこのサイト用。タグ・関連記事は未設定
        common.MEMBER_ID = "001c1c1d-7ed3-43b7-bb02-d301f9417857"
        common.CATEGORY_IDS = [
            "5fc9b0f4-98ad-4903-acf4-3fbf17b084ee",  # お知らせ
            "544d3e43-4d4d-4c7e-8956-cbc9fe71c4e0",  # 中嶋美知のブログ
        ]
        common.RELATED_POST_IDS = []
        cfg["tag_ids"] = []
    return common.run(cfg)


if __name__ == "__main__":
    run(sys.argv[1])

# 実行記録（2026-09-24）
# - asunaru: 下書き 6560b7ab-0802-4a12-b18d-94560075591d。生成後、アイキャッチと本文1枚目が暗かったため
#   明るい版（drafts/images/2026-09-24_morning-journal-11th_eyecatch_v2.png／_section_v2.png）に差し替え
# - nlpisland: 下書き 7797578a-5031-42c6-8dbc-574b67a4488b。画像は新規生成せず上記v2＋asunaru_hope.pngを再利用
