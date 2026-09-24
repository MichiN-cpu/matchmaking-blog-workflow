"""
【男女共通】39歳と40歳のあいだにある、目に見えない壁。
カテゴリ: 30代婚活（男女・悩み別）／無料相談の前に読む
2026-09-24作成 → 日曜9/27公開予定（Wixには下書き保存のみ）

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
    "a795be5b-c16c-4fed-9d55-1623b103fa25",  # 【男性向け】「結婚はまだ先でいい」と思っていた男性たちが、後から気づいたこと
    "3f84d312-9c4f-40b7-8476-963876091b38",  # 【男性向け】ちょっと変わるだけで、ダントツになれる。——30代後半から婚活を始め、7ヶ月で成婚した男性
    "2b713571-80bd-4495-af99-fa1dc7ef280c",  # 「どうしよう」が「やってみよう」に変わる。——婚活の意思決定を軽くする
]

BASE_STYLE = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
              "clear skin, real-world setting, professional lifestyle photography style, shallow depth of field, "
              "clean bright modern atmosphere, no text, no numbers, no letters, no warm yellowish tint, "
              "warm genuine smile, eyes bright with hope, NOT downcast, NOT teary, NOT vacant, "
              "clean bright natural daylight, crisp clean colors, vivid but neutral tones, NOT pale, NOT gloomy, NOT sepia")

CFG = {
    "draft_path": os.path.join(os.path.dirname(__file__), "..", "drafts", "draft_2026-09-24_39sai-40sai-kabe.md"),
    "slug": "2026-09-27_39sai-40sai-kabe",
    "title": "【男女共通】39歳と40歳のあいだにある、目に見えない壁。――婚活は「いつまでにしたいか」より「相手の画面にいるか」",
    "excerpt": "「40歳までに結婚できればいい」と思っていませんか。でもお相手は年齢で検索して探しています。40歳になった日、「30代希望」の方の画面からあなたは消えてしまう。公認心理師・仲人の中嶋美知が、39歳と40歳の境目で起きていることと、今できることをお伝えします。",
    "focus_keyword": "婚活 39歳 40歳 結婚相談所 愛媛",
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-09-27-39sai-40sai",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
        "61acc4f3-6c16-4653-995b-dd6d9136c1d3",  # IBJ
        "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
        "1571190e-c478-41bd-89b7-aa88c9747b98",  # 決断できない
        "32413ff0-17fc-455e-93e1-3add76e9eb46",  # キャンペーン
        "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
    ],
    "eyecatch_prompt": (BASE_STYLE + ", a Japanese man and a Japanese woman in their late 30s, neat smart casual outfits, "
        "walking side by side on a bright city street in the morning, both smiling naturally, "
        "looking ahead with hopeful expressions, wide shot, plenty of empty space in the upper part of the frame"),
    "section_prompt": (BASE_STYLE + ", simple still life: a smartphone lying face down on a clean white desk next to "
        "a small desk calendar with blank pages and a cup of coffee, soft natural shadows, minimal and clean"),
    "hope_prompt": (BASE_STYLE + ", a Japanese man and woman in their late 30s sitting across a small table in a bright "
        "modern cafe, looking at each other not at camera, both smiling naturally, coffee cups on the table"),
    "eyecatch_main_html": '39歳と40歳のあいだの、<br><span class="accent">見えない壁</span>。',
    "eyecatch_subtitle": "――婚活は「相手の画面にいるか」",
    "eyecatch_main_size": 48,
    "insert_after": [
        ("39歳と40歳。59歳と60歳。たった1歳の違いなのに",
         "sec", "40歳の誕生日から、検索結果の見え方が変わります。"),
        ("「40歳までに結婚できればいい」という目安は、そのまま大切にしてください。",
         "hope", "今の立ち位置を知って踏み出す一歩は、焦りとは違う一歩。"),
    ],
}

if __name__ == "__main__":
    common.run(CFG)
