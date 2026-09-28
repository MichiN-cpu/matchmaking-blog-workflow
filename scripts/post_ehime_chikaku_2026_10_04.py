"""
【男女共通】愛媛で婚活、近くにいい人はいるの？――その答えを探す前に、考えてみてほしいこと
カテゴリ: 愛媛・松山の婚活／無料相談の前に読む
2026-09-28作成 → 日曜10/4公開予定（Wixには下書き保存のみ）。入会金11,000円OFFキャンペーン（〜10/18）後押し記事
IBJ地域別データは2026年1月現在（みっちゃん提供スクショ）

投稿ロジックは post_keikaku_josei_dansei_2026_09_common.py を流用し、
カテゴリと関連記事だけこの記事用に差し替える。
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import post_keikaku_josei_dansei_2026_09_common as common

common.CATEGORY_IDS = [
    "0b6a4462-3b75-4b9e-aaad-7da59b9fe819",  # 愛媛・松山の婚活（地域×オンライン）
    "641187e4-a409-4c2f-9639-ecc548f26f15",  # 無料相談の前に読む（不安解消・向き不向き）
]
common.RELATED_POST_IDS = [
    "f2c94997-3fc7-4a95-854d-7a28deae3f29",  # 【愛媛の婚活】公的支援「愛結び」と民間結婚相談所の違い
    "43b84e67-a49e-4d1c-b95f-cb1fc436a16b",  # 【男女共通】婚活が長引く人と早く決まる人、たった一つの違い。――同じ村を、何度も訪ねていませんか？
    "fcc76304-9e21-4419-816f-e0aa463afc31",  # 【男女共通】困った時、あなたは「縮む」人ですか、それとも「広げる」人ですか
]

BASE_STYLE = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
              "clear skin, real-world setting, professional lifestyle photography style, shallow depth of field, "
              "clean bright modern atmosphere, no text, no numbers, no letters, no warm yellowish tint, "
              "warm genuine smile, eyes bright with hope, NOT downcast, "
              "clean bright natural daylight, crisp clean colors, vivid but neutral tones, NOT pale, NOT gloomy, NOT sepia")

CFG = {
    "draft_path": os.path.join(os.path.dirname(__file__), "..", "drafts", "campaign_blogs_2026-09", "draft_2026-10-04_ehime-chikaku.md"),
    "slug": "2026-10-04_ehime-chikaku",
    "title": "【男女共通】愛媛で婚活、近くにいい人はいるの？――その答えを探す前に、考えてみてほしいこと",
    "excerpt": "「愛媛で婚活しても、近くにいい人っているのかな」。そんな不安を感じていませんか。実際の数字を正直にお伝えしながら、その前に一度考えてほしい「本当はどこで、どんなふうに生きたいか」というお話をします。公認心理師・仲人の中嶋美知が、愛媛・松山で婚活を考える方へお届けします。",
    "focus_keyword": "愛媛 婚活 出会い 結婚相談所 松山",
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-10-04-ehime-chikaku",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "cb09b820-3406-4609-b861-2aeb4956ec7c",  # 愛媛の婚活（2026-09-28新規作成）
        "5b192801-25d6-4067-98d5-c7405fc91d17",  # 松山市
        "61acc4f3-6c16-4653-995b-dd6d9136c1d3",  # IBJ
        "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
        "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
        "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
        "32413ff0-17fc-455e-93e1-3add76e9eb46",  # キャンペーン
    ],
    "eyecatch_prompt": (BASE_STYLE + ", a Japanese man and a Japanese woman in their 30s standing side by side on a bright "
        "seaside promenade in the Seto Inland Sea area, calm blue sea and small green islands in the background, "
        "both smiling and looking out at the view, not looking at camera, wide shot, "
        "plenty of empty space in the upper part of the frame"),
    "section_prompt": (BASE_STYLE + ", a Japanese woman in her 30s writing freely in a notebook at a bright desk by the window, "
        "a world map and a cup of tea on the desk, relaxed hopeful expression"),
    "hope_prompt": (BASE_STYLE + ", a Japanese couple in their 30s sitting together at a bright living room table, "
        "a large paper map spread out in front of them, pointing at it and laughing together, looking at each other not at camera"),
    "eyecatch_main_html": '愛媛で婚活、<br><span class="accent">近くにいい人</span>はいるの？',
    "eyecatch_subtitle": "――その答えを探す前に、考えてみてほしいこと",
    "eyecatch_main_size": 50,
    "insert_after": [
        ("思う存分、書き出してみてください。",
         "sec", "「本当はどこで生きたい？」を、自由に書き出してみる。"),
        ("ふたりでああでもない、こうでもないと話す時間は",
         "hope", "住む場所は、ふたりで話し合って決め直していい。"),
    ],
}

if __name__ == "__main__":
    common.run(CFG)
