"""
【男女共通】「一緒に暮らせない結婚なんて、女性に嫌がられますよね？」――別居婚・週末婚から始める結婚もある
2026-10-24作成（公開日はみっちゃんがWixで決める）。Wixには下書き保存のみ（publish:false）。
共通ロジックは post_omiai_josei_2026_10_14.py の run(cfg)。
"""
import os, sys, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_omiai_josei_2026_10_14 as base

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "drafts")
base.D = os.path.join(ROOT, "bekkyo_2026-10")

CFG = {
    "draft_path": glob.glob(os.path.join(ROOT, "draft_2026-10-24_別居婚*.md"))[0],
    "slug": "2026-10-24_bekkyo_kon",
    "category_ids": ["641187e4-a409-4c2f-9639-ecc548f26f15",   # 無料相談の前に読む
                     "a65acc05-b781-4ec9-95d7-66c9daefc19f"],  # シニアの婚活
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-10-24-bekkyo-kon",
    "excerpt": ("「一緒に暮らせない結婚なんて、嫌がられますよね」。無料相談で聞いたこの不安に、公認心理師・仲人の中嶋美知が、"
                "自分自身の結婚の形を交えてお答えします。別居婚・週末婚から始める結婚はちゃんとあります。男性も女性も、事情や望みを遠慮せず伝えていい理由をお話しします。"),
    "focus_keyword": "別居婚 週末婚 結婚相談所",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "c249fe67-ef22-410a-a395-309db2116a0b",  # 結婚
        "e27232c2-174e-47f8-afee-3132dcbb7516",  # 結婚生活
        "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
        "e9832229-ecaf-435f-98ec-6d3470a13cd4",  # 結婚相談所
        "39e04614-4c13-4514-a633-8b8fad0b75df",  # 遠慮
        "3a8d9ef3-9a26-4099-8ac8-546957aa1043",  # シニア
        "e3eb2069-a9c7-4900-9352-06c562f29761",  # 60代
        "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
        "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    ],
    "related": [
        "77e61211-46b1-433b-951f-afd39bfd4168",  # その将来不安、一人で抱えなくていいのかもしれません
        "11bd2e19-894d-40fc-9c6d-c21a5f0cf490",  # 50代の婚活、風向きが変わっています
        "54ddc242-fc91-4f71-8d4a-c5914805df56",  # ネイルサロンの椅子から見えた、仲良し夫婦の共通点
    ],
    "eyecatch_prompt": ("a Japanese couple in their late 50s walking side by side on a bright weekend street of a calm small city, "
        "smiling at each other with a relaxed natural warmth, casual smart clothes, wide shot"),
    "eyecatch_main_html": '「一緒に暮らせない結婚なんて、<br><span class="accent">嫌がられますよね？</span>」',
    "eyecatch_subtitle": "――ある男性の不安に、私が自分の結婚でお答えしました",
    "eyecatch_main_size": 52,
    "body_images": [
        ("そのお話をしたとき、相談に来てくださった男性の肩の力が、ふっと抜けるのが見えました。「そういう形でも、結婚と呼んでいいんですね」と、ほっとした表情で笑ってくださったんです。",
         "a kind-looking Japanese man in his 60s with neat short hair, sitting alone at a bright cafe table with a cup of tea, "
         "relieved warm smile, shoulders relaxed, looking out of the window, natural daylight, seen from the side"),
        ("夜、電話の向こうで「今日ね、こんなことがあってね」と話す声を聞きながら、自分らしく笑っている。月に数回会う日は、いつもよりちょっとだけ丁寧にごはんをつくって、一緒に食べる。離れていても、ちゃんと帰る場所がある。そんなふうに、お互いのエネルギーがチャージされる結婚が、私がお勧めしたい「素直婚」なんです。",
         "a Japanese woman in her late 50s relaxing on a sofa at home in the evening, smiling happily while talking on her smartphone, "
         "a cup of tea beside her, bright cozy modern living room, natural light from the window"),
        ("世間が決めた「結婚はこうあるべき」ではなく、ふたりが決めた「うちはこれでいこう」を、一緒に探していく。その相手と出会うために、婚活はあるのだと思います。",
         "a Japanese couple in their late 50s cooking together in a bright modern kitchen on a weekend, laughing, "
         "preparing a simple meal, natural daylight"),
    ],
}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        base.verify(sys.argv[2], CFG["cta_url"])
    else:
        base.run(CFG)
