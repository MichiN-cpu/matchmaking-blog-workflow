"""
【男性向け】婚活、何から手をつければいいか分からなくてモヤモヤしているあなたへ。――成婚までの６ステップ
カテゴリ: 結婚相談所の始め方／成婚までのロードマップ
2026-09-28作成 → 木曜10/1公開予定（Wixには下書き保存のみ）。入会金11,000円OFFキャンペーン（〜10/18）後押し記事

投稿ロジックは post_keikaku_josei_dansei_2026_09_common.py を流用し、
カテゴリと関連記事だけこの記事用に差し替える。
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import post_keikaku_josei_dansei_2026_09_common as common

common.CATEGORY_IDS = [
    "0122d61b-14c6-42d9-a950-d4b527ea39d1",  # 結婚相談所の始め方（IBJ・流れ・費用）
    "998b685d-1453-4ebd-8bd2-0218e315186e",  # 成婚までのロードマップ
]
common.RELATED_POST_IDS = [
    "e1155633-e7b8-4179-8a0d-1283da56565c",  # 【男性向け】婚活の写真に、かっこよさはいりません。
    "388e71e9-6147-4322-a8d9-b66778b31577",  # 【男性向け】婚活で「また会いたい」と思われる男性が、自然にやっていること。
    "89efea38-cc60-4f52-a7d4-0c2b7fb0e515",  # 【男性向け】仮交際中、LINEを送らない男性へ。
]

BASE_STYLE = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
              "clear skin, real-world setting, professional lifestyle photography style, shallow depth of field, "
              "clean bright modern atmosphere, no text, no numbers, no letters, no warm yellowish tint, "
              "warm genuine smile, NOT downcast, "
              "clean bright natural daylight, crisp clean colors, vivid but neutral tones, NOT pale, NOT gloomy, NOT sepia")

CFG = {
    "draft_path": os.path.join(os.path.dirname(__file__), "..", "drafts", "campaign_blogs_2026-09", "draft_2026-10-01_seikon-6steps.md"),
    "slug": "2026-10-01_seikon-6steps",
    "title": "【男性向け】婚活、何から手をつければいいか分からなくてモヤモヤしているあなたへ。――成婚までの６ステップ",
    "excerpt": "結婚したい気持ちはあるのに、何から手をつければいいか分からない。そんなモヤモヤを抱えていませんか。実は、結婚までにやることはとてもシンプルです。公認心理師・仲人の中嶋美知が、愛媛で婚活を考える男性に、プロフィールづくりからプロポーズまでの6つのステップをお伝えします。",
    "focus_keyword": "婚活 男性 何から 結婚相談所 愛媛",
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-10-01-seikon-6steps",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
        "d372d6c7-06f8-47fe-a647-6229a0b94c80",  # お見合い
        "1ec5b4de-8edb-4c97-8199-2ef82776c050",  # 仮交際
        "0ddde006-b527-4852-8056-8cdb87174e82",  # 真剣交際
        "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
        "021e7932-59b1-43ae-9c76-4b00cd73b587",  # 好印象
        "32413ff0-17fc-455e-93e1-3add76e9eb46",  # キャンペーン
    ],
    "eyecatch_prompt": (BASE_STYLE + ", a Japanese man in his mid 30s, neat smart casual outfit, standing on a bright "
        "city street in the morning, looking ahead with a calm hopeful smile, not looking at camera, "
        "wide shot, plenty of empty space in the upper part of the frame"),
    "section_prompt": (BASE_STYLE + ", a Japanese man in his 30s in a neat navy suit being photographed in a bright "
        "white photo studio, smiling naturally, a photographer's softbox visible at the edge of the frame"),
    "hope_prompt": (BASE_STYLE + ", omiai scene in a bright hotel lounge, a Japanese man in a neat dark suit with a "
        "dress shirt and a beautiful Japanese woman in a soft pink elegant dress, hair down with gentle blow-dried "
        "wave, loose and flowing, not tied up, facing each other, looking at each other not at camera, "
        "both smiling naturally, coffee cups on the table"),
    "eyecatch_main_html": '婚活、何から手をつければ<br><span class="accent">いいか分からない</span>あなたへ。',
    "eyecatch_subtitle": "――成婚までの６ステップ",
    "eyecatch_main_size": 46,
    "insert_after": [
        ("ここにお金と時間をかけるのは",
         "sec", "清潔感と笑顔。プロの写真は、婚活でいちばん効果の高い投資です。"),
        ("「なんだか楽しかったな」「話しやすかったな」",
         "hope", "覚えているのは「何を話したか」より、「なんだか楽しかった」という空気感。"),
    ],
}

if __name__ == "__main__":
    common.run(CFG)
