import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from post_keikaku_josei_dansei_2026_09_common import run

BASE_STYLE = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
              "clear skin, real-world setting, professional lifestyle photography style, shallow depth of field, "
              "clean bright modern atmosphere, no text, no warm yellowish tint, "
              "warm genuine smile, eyes bright with hope, NOT downcast, NOT teary, NOT vacant, "
              "clean bright natural daylight, crisp clean colors, vivid but neutral tones, NOT pale, NOT gloomy, NOT sepia")

CFG = {
    "draft_path": os.path.join(os.path.dirname(__file__), "..", "drafts", "draft_2026-09-21_keikaku_dansei.md"),
    "slug": "2026-09-24_keikaku_dansei",
    "title": "【男性向け】計画どおりに進んでいるのに、なぜか胸のあたりがザワつく旅の途中。――彼女の「ここ寄りたい」の裏にある本音",
    "excerpt": "準備は万全なのに、彼女の「ここ寄りたい」で予定が崩れてイライラする。そのモヤモヤ、実は誰のせいでもありません。公認心理師・仲人の中嶋美知が、計画を大切にする男性が彼女と心地よく過ごすための「余白の入れ方」を三つのコツで解説します。",
    "focus_keyword": "デート 計画 彼女 予定変更 男性 婚活 愛媛",
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-09-24-keikaku-dansei",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "1c7a4d95-e95b-492a-93e2-da1c8a63ab9b",  # デート
        "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
        "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
        "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
        "a1cddd3a-c52b-47f4-b1bf-3c8ce905ebc5",  # コミュニケーション心理学
    ],
    "eyecatch_prompt": (BASE_STYLE + ", a Japanese man in his 30s, neat casual smart outfit, sitting in the "
        "driver's seat of a car, glancing at a smiling woman beside him who points at a cafe outside, "
        "both smiling naturally, soft natural daylight, wide shot"),
    "section_prompt": (BASE_STYLE + ", a Japanese man in his 30s, neat casual outfit, looking at a printed "
        "travel itinerary on a table with a calm focused expression and slight smile, bright modern cafe"),
    "hope_prompt": (BASE_STYLE + ", a Japanese man and woman in their 30s facing each other across a small table "
        "in a bright cafe, looking at each other not at camera, both smiling naturally, coffee cups on the table"),
    "eyecatch_main_html": '計画どおりなのに、<br>なぜか胸が<span class="accent">ザワつく</span>旅。',
    "eyecatch_subtitle": "――彼女の「ここ寄りたい」の裏にある本音",
    "eyecatch_main_size": 44,
    "insert_after": [
        ("あなたが計画を立てているとき、男性性のスイッチが入っています。だから旅行も、時間という数字、距離という数字、プランというかたちにフォーカスが向く。一方で、彼女は今、女性性のスイッチが入っているのかもしれません。景色、香り、「なんだかいいな」という感覚が、何より大事になっている状態です。",
         "sec", "計画は、時間もエネルギーも使う立派な愛情表現。"),
        ("あなたが立てた計画があったからこそ、たどり着けた場所なんです。計画は、寄り道を邪魔するものではなく、寄り道を安心して楽しむための\"土台\"。そう思えたら、彼女の「ここ寄りたい」は、あなたの準備を無にするものではなく、あなたの準備の先にある、ふたりの喜びに変わっていきます。これは結婚後、人生のプランを立てるときも同じなんですよね。",
         "hope", "計画という土台があったから、たどり着けた場所で。"),
    ],
}

if __name__ == "__main__":
    run(CFG)
