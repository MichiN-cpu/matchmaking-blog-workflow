import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from post_keikaku_josei_dansei_2026_09_common import run

BASE_STYLE = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
              "clear skin, real-world setting, professional lifestyle photography style, shallow depth of field, "
              "clean bright modern atmosphere, no text, no warm yellowish tint, "
              "warm genuine smile, eyes bright with hope, NOT downcast, NOT teary, NOT vacant, "
              "clean bright natural daylight, crisp clean colors, vivid but neutral tones, NOT pale, NOT gloomy, NOT sepia")

CFG = {
    "draft_path": os.path.join(os.path.dirname(__file__), "..", "drafts", "draft_2026-09-21_keikaku_josei.md"),
    "slug": "2026-09-23_keikaku_josei",
    "title": "【女性向け】「あのカフェ、寄りたい」が言えなかった日。――彼の完璧なプランの中で、なぜか泣きたくなった理由",
    "excerpt": "彼が立ててくれたデートのプランに、「ここ寄りたい」が言えなかった経験はありませんか。それはワガママでも、彼の冷たさでもありません。公認心理師・仲人の中嶋美知が、自身の新婚旅行の失敗談から、計画派の彼と心地よく過ごすための三つのコツを解説します。",
    "focus_keyword": "デート 計画 合わない 女性 婚活 愛媛",
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-09-23-keikaku-josei",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "1c7a4d95-e95b-492a-93e2-da1c8a63ab9b",  # デート
        "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
        "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
        "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
        "a1cddd3a-c52b-47f4-b1bf-3c8ce905ebc5",  # コミュニケーション心理学
    ],
    "eyecatch_prompt": (BASE_STYLE + ", a beautiful Japanese woman in her 30s, elegant refined features, "
        "model-like appearance, sitting in the passenger seat of a car on a scenic coastal road, "
        "pointing happily out the window at a cafe, soft natural daylight, wide shot"),
    "section_prompt": (BASE_STYLE + ", a Japanese man in his 30s, neat casual outfit, holding a tablet and a "
        "neatly written travel itinerary, looking at it with a calm confident smile, bright modern living room"),
    "hope_prompt": (BASE_STYLE + ", a Japanese man and woman in their 30s facing each other across a small table "
        "in a bright cafe, looking at each other not at camera, both smiling naturally, coffee cups on the table"),
    "eyecatch_main_html": '「あのカフェ、寄りたい」<br>が言えなかった日。',
    "eyecatch_subtitle": "――彼の完璧なプランの中で、なぜか泣きたくなった理由",
    "eyecatch_main_size": 46,
    "insert_after": [
        ("彼がデートのプランを立てているとき、彼は男性性のスイッチが入っています。だから旅行も、時間という数字、距離という数字、計画というプランにフォーカスしていく。一方で、あなたの女性性が前に出ているときは、今この瞬間の景色、香り、「なんだかいいな」という感覚が、何より大事になります。",
         "sec", "彼のプランは、彼なりの愛情のかたち。"),
        ("計画どおりに進む旅も素敵です。でも、計画があったからこそ辿り着けた寄り道は、ふたりだけの、忘れられない思い出になります。これは結婚後の暮らしでも同じで、住まいや仕事、家族のことなど人生のプランも、「決めたとおりに進める」のではなく、「感じながら、すり合わせていく」ことで、もっと豊かなものになっていくんです。",
         "hope", "計画があったから、たどり着けた場所で。"),
    ],
}

if __name__ == "__main__":
    run(CFG)
