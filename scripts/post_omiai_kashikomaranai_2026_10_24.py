"""
【男女共通】なんだか疲れたお見合い。――面談ではあんなに楽しそうなのに、お見合いになると消えてしまうものがあります
2026-10-24作成（公開日はみっちゃんがWixで決める）。Wixには下書き保存のみ（publish:false）。
共通ロジックは post_omiai_josei_2026_10_14.py の run(cfg)。
"""
import os, sys, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_omiai_josei_2026_10_14 as base

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "drafts")
base.D = os.path.join(ROOT, "omiai_kashikomaranai_2026-10")
OS = base.OMIAI_STYLE

CFG = {
    "draft_path": glob.glob(os.path.join(ROOT, "draft_2026-10-24_お見合いでかしこまらないで.md"))[0],
    "slug": "2026-10-24_omiai_kashikomaranai",
    "category_ids": ["5089ac63-e2ce-4de1-b472-3512a77401af"],  # お見合い
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-10-24-omiai-kashikomaranai",
    "excerpt": ("お見合いのあと、なぜかどっと疲れる。面談では生き生きしているのに、お見合いになると表情も声も姿勢も固くなっていませんか。"
                "公認心理師・仲人の中嶋美知が、早く結果を出す人やモテる人が最初から「普段の自分」で話している理由と、今日からできる小さな五つのスイッチをお伝えします。"),
    "focus_keyword": "お見合い 疲れる かしこまる 普段の自分",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "d372d6c7-06f8-47fe-a647-6229a0b94c80",  # お見合い
        "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
        "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
        "021e7932-59b1-43ae-9c76-4b00cd73b587",  # 好印象
        "b7302812-ad6a-4d65-a087-abd737781882",  # モテる
        "6d01ad45-7102-4cf8-a156-98c908a968fe",  # 魅力
        "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
        "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
        "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    ],
    "related": [
        "e150bc39-0099-4f9d-9db3-98a0802541d2",  # お見合いで、本当は聞かれたくないことがあるあなたへ
        "490faf91-c89f-489e-82ef-3d757165afea",  # 笑顔が、婚活を変える。
        "2cf3dbc8-6b9d-471a-bc78-8fe3c75f4ff4",  # 「聞き上手」をやめたら、うまくいく。
    ],
    "eyecatch_prompt": ("beautiful Japanese woman in her 30s, elegant refined features, an omiai meeting in a bright modern hotel lounge "
        "with large windows, a Japanese man in his 30s across the table, " + OS +
        "both laughing naturally and leaning slightly toward each other, teacups on the table, wide shot"),
    "eyecatch_main_html": 'なんだか<span class="accent">疲れた</span><br>お見合い。',
    "eyecatch_subtitle": "――面談ではあんなに楽しそうなのに、消えてしまうものがあります",
    "eyecatch_main_size": 66,
    "body_images": [
        ("それなのに、お見合いの席に着いた途端、その魅力がすっと消えてしまう。",
         "beautiful Japanese woman in her 30s, elegant refined features, sitting upright and a little stiffly at a table in a bright hotel lounge, "
         "polite faint smile, hands folded, a Japanese man in his 30s across the table, " + OS + "natural daylight"),
        ("一度に全部しなくて大丈夫です。ひとつ変えるだけで、お見合いの空気は、びっくりするほど変わります。",
         "beautiful Japanese woman in her 30s, elegant refined features, laughing brightly while telling a story with a lively hand gesture, "
         "a Japanese man in his 30s leaning back relaxed and smiling at her, " + OS + "bright hotel lounge, coffee cups on the table"),
        ("次のお見合いが終わった帰り道、「あー、楽しかった！」と、思わず声が出る。そんな日が、あなたにもきっと来ますよ😊",
         "beautiful Japanese woman in her 30s, elegant refined features, walking out of a hotel entrance on a sunny afternoon, "
         "smiling happily with a light cheerful step, soft pink elegant dress, hair down with gentle wave, clean bright atmosphere"),
    ],
}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        base.verify(sys.argv[2], CFG["cta_url"])
    else:
        base.run(CFG)
