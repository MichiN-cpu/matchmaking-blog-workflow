"""
【女性向け】「最初は優しかったのに」をくり返さないために。――探すのは「私の好きな〇〇」でいられる人
カテゴリ: 30代婚活（男女・悩み別）／無料相談の前に読む
2026-09-28作成 → 水曜9/30公開予定（Wixには下書き保存のみ）。入会金11,000円OFFキャンペーン（〜10/18）後押し記事

投稿ロジックは post_keikaku_josei_dansei_2026_09_common.py を流用し、
カテゴリと関連記事だけこの記事用に差し替える。
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import post_keikaku_josei_dansei_2026_09_common as common

common.CATEGORY_IDS = [
    "ce3b3deb-a05e-4093-a1a3-aa657693da8d",  # 30代婚活（男女・悩み別）
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む（不安解消・向き不向き）
]
common.RELATED_POST_IDS = [
    "b39f279c-2e72-4439-9181-6c5195e271e3",  # 【女性向け】本当は、素敵な人はちゃんといます。
    "ffcc121d-6384-4392-ac96-e7c75f424cf2",  # 【女性向け】「気がきく女子」をお休みしてみない？ ポンコツ女子のすすめ
    "2cf3dbc8-6b9d-471a-bc78-8fe3c75f4ff4",  # 【女性向け】「聞き上手」をやめたら、うまくいく。
]

BASE_STYLE = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
              "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, bright eyes, "
              "real-world setting, professional lifestyle photography style, shallow depth of field, "
              "clean bright modern atmosphere, no text, no numbers, no letters, no warm yellowish tint, "
              "clean bright natural daylight, crisp clean colors, vivid but neutral tones, NOT pale, NOT gloomy, NOT sepia")

CFG = {
    "draft_path": os.path.join(os.path.dirname(__file__), "..", "drafts", "campaign_blogs_2026-09", "draft_2026-09-30_ouji-sama-sagashi.md"),
    "slug": "2026-09-30_ouji-sama-sagashi",
    "title": "【女性向け】「最初は優しかったのに」をくり返さないために。――探すのは「私の好きな〇〇」でいられる人",
    "excerpt": "素敵な人を探して、やっと出会えたのに、なぜかうまくいかない。「最初は優しかったのに」と感じたことはありませんか。どちらが悪いわけでもなく、始まり方にヒントがあります。公認心理師・仲人の中嶋美知が、愛媛で婚活中の女性に、本当に探してほしい相手の見つけ方をお伝えします。",
    "focus_keyword": "婚活 女性 理想の相手 結婚相談所 愛媛",
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-09-30-ouji-sama-sagashi",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
        "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
        "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
        "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
        "a3a015e3-7f09-4a9f-b5c4-2c59a74bac7c",  # 自己肯定感
        "32413ff0-17fc-455e-93e1-3add76e9eb46",  # キャンペーン
    ],
    "eyecatch_prompt": (BASE_STYLE + ", a Japanese woman in her early 30s in a bright flower shop, arranging flowers, "
        "absorbed in what she loves, laughing naturally with a genuine relaxed smile, not looking at camera, "
        "wide shot, plenty of empty space in the upper part of the frame"),
    "section_prompt": (BASE_STYLE + ", a Japanese woman in her 30s sitting by the window of a bright modern cafe, "
        "holding a cup, slightly thoughtful gentle expression, not sad, looking out the window"),
    "hope_prompt": (BASE_STYLE + ", a Japanese man and woman in their 30s walking side by side in a bright green park, "
        "the man has just handed her a small coffee, she is laughing happily and naturally, relaxed and equal atmosphere, "
        "looking at each other not at camera"),
    "eyecatch_main_html": '「最初は優しかったのに」を<br><span class="accent">くり返さない</span>ために。',
    "eyecatch_subtitle": "――探すのは「私の好きな〇〇」でいられる人",
    "eyecatch_main_size": 46,
    "insert_after": [
        ("「最初はそんな人だと思わなかった」「優しかったのに」",
         "sec", "がんばって合わせるほど、なぜか遠くなる。そんな経験、ありませんか。"),
        ("その笑顔で、男性は「自分はこの人を幸せにできる」",
         "hope", "素直な「うれしい」が、ふたりの関係を育てていきます。"),
    ],
}

if __name__ == "__main__":
    common.run(CFG)
