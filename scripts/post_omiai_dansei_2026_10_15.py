"""
【男性向け】お見合い、会話は途切れなかったのに、なぜかお断り。
2026-10-12作成 → 2026-10-15(木) 9:00 想定。Wixには下書き保存のみ（publish:false）。
共通ロジックは post_omiai_josei_2026_10_14.py の run(cfg) を使う。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from post_omiai_josei_2026_10_14 import run, verify, D, OMIAI_STYLE

CFG = {
    "draft_path": os.path.join(D, "danseimuke_omiai_shitsumon.md"),
    "slug": "2026-10-15_omiai_dansei",
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-10-15-omiai-dansei",
    "excerpt": ("会話は途切れなかったのに、なぜかお断り。その理由は、離婚の理由や活動歴を確かめる「査定する質問」にあるかもしれません。"
                "公認心理師・仲人の中嶋美知が、相手の素敵なところを引き出す質問への変え方と、ご自身の離婚の話を伝えるタイミングをお伝えします。"),
    "focus_keyword": "お見合い 質問 男性 お断り",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "d372d6c7-06f8-47fe-a647-6229a0b94c80",  # お見合い
        "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
        "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
        "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
        "021e7932-59b1-43ae-9c76-4b00cd73b587",  # 好印象
        "bc47248a-e548-43b9-bd31-8da1d1d4e189",  # 再婚
        "d454c1ff-e2b4-4d07-84dc-626693e74f61",  # 離婚
        "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
        "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    ],
    "related": [
        "e7a299f5-57ad-4de8-8d31-21d366b0661e",  # お見合いで「モテるでしょ？！」と聞く男性ほどモテないって知ってる？
        "6ae51a61-7db6-4510-b865-f026ec1700fa",  # お見合いで仕事の苦労話をしていませんか？
        "96068104-095f-4934-b2bc-db6f60b98e11",  # "話が面白いのに、なぜか伝わらない"男性へ。
    ],
    "eyecatch_prompt": ("an omiai meeting in a bright modern hotel lounge with large windows, a friendly Japanese man in his late 30s "
        "smiling warmly while asking a question, a beautiful Japanese woman across the table smiling and laughing, "
        + OMIAI_STYLE + "teacups on the table, seen from the side, wide shot"),
    "eyecatch_main_html": 'お見合い、会話は途切れなかったのに、<br>なぜか<span class="accent">お断り</span>。',
    "eyecatch_subtitle": "――そのモヤモヤ、最初の質問に答えがあるかもしれません",
    "eyecatch_main_size": 54,
    "body_images": [
        ("その答えを聞いて、あなたは何を判断しようとしていたのでしょうか。",
         "a Japanese man in his late 30s in a neat casual jacket, sitting by a bright cafe window with a coffee cup, "
         "calm thoughtful expression with a gentle smile, looking out of the window, natural daylight"),
        ("この目標があるだけで、出てくる質問は自然と変わってくるんですよね。",
         "a Japanese man in his late 30s and a beautiful Japanese woman in her 30s sitting across from each other "
         "in a bright hotel lounge, the woman laughing happily while talking, the man listening with a warm smile, "
         + OMIAI_STYLE + "seen from the side, teacups on the table"),
        ("そして、そんな安心をくれる男性こそが、女性から「この人と一緒にいたい」と選ばれていくんですよね。",
         "a Japanese married couple in their late 30s having dinner at a bright modern dining table at home, "
         "the wife smiling and telling a story about her day, the husband listening and laughing, "
         "clean bright interior, natural evening light from the window"),
    ],
}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        verify(sys.argv[2], CFG["cta_url"])
    else:
        run(CFG)
