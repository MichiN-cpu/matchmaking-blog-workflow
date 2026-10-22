"""
【男性向け】気の利いたひと言が出てこなくて、帰り道に肩がずしっと重くなる。
2026-10-22作成 → 2026-10-29(木) 9:00 想定。Wixには下書き保存のみ（publish:false）。
共通ロジックは post_omiai_josei_2026_10_14.py の run(cfg) を使う（カテゴリと保存先だけ差し替え）。
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_omiai_josei_2026_10_14 as base

base.D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "drafts", "shinrai_2026-10")
base.CATEGORY_OMIAI = "3f5f378d-a4f4-47e0-90a7-ab4daa27504e"  # 仮交際

CFG = {
    "draft_path": os.path.join(base.D, "danseimuke_shinrai.md"),
    "slug": "2026-10-29_shinrai_dansei",
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-10-29-shinrai-dansei",
    "excerpt": ("甘い言葉も気の利いたセリフも出てこない。そんな自分に自信をなくしていませんか。"
                "公認心理師・仲人の中嶋美知が、自身の結婚の決め手と心理学の研究から、"
                "女性が結婚を決めるときに本当に見ている「言っていることと、していることが同じ」という安心感についてお話しします。"),
    "focus_keyword": "結婚の決め手 男性 信頼",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "18eef72c-620b-46dd-969b-30553b86c45a",  # 男性心理
        "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
        "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
        "1c7a4d95-e95b-492a-93e2-da1c8a63ab9b",  # デート
        "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
        "7ade8606-9f4c-4549-b06d-2d1790cfb448",  # 信頼
        "82ea073a-d3e6-44a0-9f65-7addcbcb8fb8",  # 結婚の決め手
        "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
        "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    ],
    "related": [
        "d9f205bf-f8ee-45af-894e-62b0cb82d5dc",  # 心から幸せに成婚退会していく女性は、男性の"ここ"を見ています。
        "89efea38-cc60-4f52-a7d4-0c2b7fb0e515",  # 仮交際中、LINEを送らない男性へ。
        "f71ec040-995d-4853-96b3-79d663703958",  # "リードしなきゃ"を、一人で抱えなくていい。
    ],
    "eyecatch_prompt": ("a kind-looking Japanese man in his 40s in a neat casual jacket, walking home on a calm early-evening street "
        "in a small Japanese city, a gentle thoughtful expression with a faint hopeful smile, soft city lights beginning to glow, wide shot"),
    "eyecatch_main_html": '気の利いたひと言が出てこなくて、<br>帰り道に<span class="accent">肩が重くなる</span>。',
    "eyecatch_subtitle": "――女性が結婚を決めるのは、ときめきより「安心して話せる」でした",
    "eyecatch_main_size": 50,
    "body_images": [
        ("この話を聞きながら、私は何度もうなずいていました。なぜなら、私自身もまったく同じ理由で、結婚を決めたからなんです。",
         "a Japanese couple in their 40s sitting side by side on a bench in a bright park, the man listening attentively "
         "to the woman with a gentle nod, both relaxed and smiling, natural daylight"),
        ("結婚を考える女性が探しているのは、まさにこの安全基地なんですよね。ドキドキさせてくれる人より、帰ってきたときにホッとできる人。そして、それをつくるのは話術ではなく、あなたの日々の行動なんです。",
         "a Japanese couple in their 40s at a bright modern home, the man handing the woman a cup of tea, "
         "the woman smiling with relief and comfort, calm everyday moment, natural daylight from the window"),
        ("三つ目は、「次」を言葉にして、そのとおりに動くことです。「次は〇〇に行ってみようか」と小さな予定をひとつ決めて、それを実際に叶える。気の利いたセリフよりも、「この人といると、ひとつずつ叶っていく」という実感のほうが、ずっと心に残るんです。",
         "a Japanese man and woman in their 40s arriving together at the entrance of a cozy bright cafe, "
         "the man holding the door open, both smiling naturally, the woman looking happy"),
    ],
}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        base.verify(sys.argv[2], CFG["cta_url"])
    else:
        base.run(CFG)
