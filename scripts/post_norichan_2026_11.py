"""
のりちゃん対話メモ(topics/2026-09-24_norichan-taiwa.md)からの3本。Wixには下書き保存のみ（publish:false）。
  josei  : 【女性向け】2026-11-11(水)想定  交際初期の違和感は「伝えたら直してくれる人か」（元ネタD）
  dansei : 【男性向け】2026-11-05(木)想定  アプリで「モテていた」のは幻？（元ネタB）
  kyotsu : 【男女共通】2026-11-22(日)想定  46歳アメリカ半年／冒険と無謀（元ネタH）
共通ロジックは post_omiai_josei_2026_10_14.py の run(cfg)。使い方: python3 post_norichan_2026_11.py josei|dansei|kyotsu
              検証のみ: python3 post_norichan_2026_11.py --verify <name> <DRAFT_ID>
⚠️ 料理名（伏せ字の〇〇ー）は本文・タイトル・タグ・画像プロンプトのどこにも出さない。片目の話は書かない。
"""
import os, sys, requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_omiai_josei_2026_10_14 as base
c = base.c

HERE = os.path.dirname(os.path.abspath(__file__))
base.D = os.path.join(HERE, "..", "drafts", "norichan_2026-11")

CAT_KARIKOUSAI = "3f5f378d-a4f4-47e0-90a7-ab4daa27504e"   # 仮交際
CAT_MUSHI = "641187e4-a409-4c2f-9639-ecc548f26f15"        # 無料相談の前に読む
CAT_HAJIME = "0122d61b-14c6-42d9-a950-d4b527ea39d1"       # 結婚相談所の始め方

OMIAI = base.OMIAI_STYLE


def tag_ids(labels):
    """既存タグを取得して再利用。なければ作成。"""
    existing, off = {}, 0
    while True:
        r = requests.get(f"{c.WIX_BASE}/blog/v3/tags?paging.limit=100&paging.offset={off}", headers=c.wix_headers()).json()
        t = r.get("tags", [])
        for x in t:
            existing[x["label"]] = x["id"]
        if len(t) < 100:
            break
        off += 100
    ids = []
    for lb in labels:
        if lb not in existing:
            rr = requests.post(f"{c.WIX_BASE}/blog/v3/tags", headers=c.wix_headers(), json={"label": lb})
            print("tag create:", lb, rr.status_code)
            existing[lb] = rr.json()["tag"]["id"]
        ids.append(existing[lb])
    return ids


CFGS = {
 "josei": {
    "md": "josei_ikan.md",
    "slug": "2026-11-11_josei_ikan",
    "utm": "2026-11-11-josei-ikan",
    "category_ids": [CAT_KARIKOUSAI],
    "excerpt": ("交際初期に「ん？」と感じても、その場でアウトにしなくて大丈夫です。公認心理師・仲人の中嶋美知が、"
                "自身の初デートの体験をもとに、直せる違いと直しにくい違いの見分け方、伝えたあとの「反応」の見方を、愛媛・松山で婚活中の方へお話しします。"),
    "focus_keyword": "交際初期 違和感 女性",
    "tags": ["婚活", "仮交際", "女性心理", "コミュニケーション", "デート", "相手の見極め方", "パートナーシップ", "遠慮", "心理学", "NLP", "違和感"],
    "related": ["f22aea1c-f175-40f1-baf0-9fbf92ae2c4b", "b0a4cf56-1d12-4102-b61a-2bcee4169e6b", "6f938ec5-c7e0-4c33-b3a9-cb6da95bb66c"],
    "eyecatch_prompt": ("a Japanese woman in her 30s sitting at a table by a big window in a quiet mountain cafe with green forest outside, "
        "an amused and cheerful expression as if hearing a funny unexpected story, a man across the table softly out of focus, "
        "two simple lunch plates on the table, wide shot, bright natural daylight"),
    "eyecatch_main_html": '〇〇ーを食べているのに、<br>彼が<span class="accent">お腹を下した話</span>を<br>始めた日。',
    "eyecatch_subtitle": "――交際初期の違和感は、「アウト」と決める前に見てほしいことがあります",
    "eyecatch_main_size": 56,
    "body_images": [
        ("山の中の、静かなカフェでした。",
         "a Japanese woman in her 30s smiling happily at a table in a quiet mountain cafe with large windows overlooking green trees, "
         "looking out the window, a lunch plate in front of her, relaxed first-date mood, natural daylight"),
        ("悪気がまったくないんですよね。",
         "a Japanese woman in her 30s laughing with her hand lightly over her mouth, amused and relaxed, sitting across from a man "
         "softly out of focus in a bright cafe, candid moment, natural daylight"),
        ("伝え方は、責めるのではなく",
         "a Japanese couple in their 40s at a bright cafe table, the woman gently speaking with a soft smile, "
         "the man listening attentively and nodding with a kind expression, both relaxed, natural daylight"),
    ],
 },
 "dansei": {
    "md": "dansei_app.md",
    "slug": "2026-11-05_dansei_app",
    "utm": "2026-11-05-dansei-app",
    "category_ids": [CAT_MUSHI],
    "excerpt": ("アプリでは「いいね」が続いていたのに、結婚相談所に来たら気持ちが沈む。そんな40代の男性へ。公認心理師・仲人の中嶋美知が、"
                "ジャムの実験や「チェンジ」のしやすさから、アプリと結婚相談所の違い、そして制限が決断を助ける理由を、愛媛・松山で婚活を考える方へお話しします。"),
    "focus_keyword": "マッチングアプリ 結婚相談所 男性 40代",
    "tags": ["婚活", "マッチングアプリ", "男性心理", "40代", "結婚相談所", "決断できない", "婚活マインド", "男性の自信", "心理学", "NLP"],
    "related": ["6f4cdc1e-0655-4256-97a4-d18f9f133aaa", "55c37fce-c22c-45d4-8025-89bcb4f674f2", "7a86da2b-a794-449a-874f-d0a6caaee954"],
    "eyecatch_prompt": ("a kind-looking Japanese man in his 40s in a neat smart casual jacket sitting at a bright cafe table holding a smartphone, "
        "a thoughtful expression with a faint hopeful smile, clean bright natural daylight from a window, wide shot"),
    "eyecatch_main_html": 'アプリでは、あんなに<br><span class="accent">「いいね」</span>が来ていたのに。',
    "eyecatch_subtitle": "――40代で結婚相談所に来て、画面を開くたび気分が沈むあなたへ",
    "eyecatch_main_size": 56,
    "body_images": [
        ("返ってきたのは、こんな答えでした。",
         "a Japanese man and woman in their 50s chatting casually at a home dining table with tea cups, the man talking with a gentle smile, "
         "the woman listening with interest, bright natural daylight"),
        ("マッチングアプリは、いわばジャム",
         "a supermarket shelf lined with dozens of colorful jam jars of many kinds, a customer's hand hovering undecided, "
         "no faces visible, bright clean store lighting, shallow depth of field"),
        ("結婚という目的がはっきりしていて",
         "a Japanese man and woman in their 40s sitting across from each other at a table in a bright hotel lounge, "
         + OMIAI + "both smiling and relaxed, teacups on the table"),
    ],
 },
 "kyotsu": {
    "md": "kyotsu_boken.md",
    "slug": "2026-11-22_kyotsu_boken",
    "utm": "2026-11-22-kyotsu-boken",
    "category_ids": [CAT_HAJIME],
    "excerpt": ("「今さら動いても遅いのかな」と迷っていませんか。公認心理師・仲人の中嶋美知が、46歳でひとりアメリカに半年住んだ経験と、"
                "パートナーに教わったゴルフのたとえから、「冒険」と「無謀」の違い、そして婚活の一歩を冒険にする考え方を、愛媛・松山で婚活を考える方へお話しします。"),
    "focus_keyword": "婚活 一歩 踏み出せない 年齢",
    "tags": ["婚活", "チャレンジ", "婚活マインド", "心構え", "コーチ", "未来思考", "迷い", "結婚相談所", "心理学", "NLP"],
    "related": ["1cc8f960-3915-40d0-a2b2-b9ae2bf4d13e", "935c10a3-40fd-4a54-92af-68cc5596df81", "3f84d312-9c4f-40b7-8476-963876091b38"],
    "eyecatch_prompt": ("a Japanese woman in her 40s with a small suitcase walking on a sunny university campus path with red brick buildings and tall green trees, "
        "smiling confidently and looking ahead, wide shot, bright natural daylight"),
    "eyecatch_main_html": '46歳、ひとりで<br><span class="accent">アメリカへ半年。</span>',
    "eyecatch_subtitle": "――婚活の一歩が「冒険」になる人と「無謀」になる人の違い",
    "eyecatch_main_size": 62,
    "body_images": [
        ("住まいは大学の寮でした。",
         "a Japanese woman in her 40s standing in front of an American university dormitory building on a sunny day with a suitcase, "
         "looking up with a bright curious smile, wide shot, blue sky"),
        ("ゴルフには、攻めるホールと",
         "a beautiful sunny golf course short par four hole with a fairway, bunkers beside the green and a golfer seen from behind, "
         "blue sky, vivid green grass, wide shot"),
        ("ゴルフにキャディさんがいるように",
         "a Japanese man and woman in their 40s sitting side by side at a bright cafe table, looking together at a notebook and planning, "
         "both smiling hopefully, natural daylight"),
    ],
 },
}


def make_cfg(name):
    x = CFGS[name]
    path = os.path.join(base.D, x["md"])
    lines = open(path, encoding="utf-8").read().split("\n")
    resolved = []
    for prefix, prompt in x["body_images"]:
        hit = [l.strip() for l in lines if l.strip().startswith(prefix)]
        assert len(hit) == 1, f"挿入位置が一意に特定できません: {prefix} -> {len(hit)}"
        resolved.append((hit[0], prompt))
    return {
        "draft_path": path, "slug": x["slug"],
        "cta_url": f"https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign={x['utm']}",
        "excerpt": x["excerpt"], "focus_keyword": x["focus_keyword"],
        "category_ids": x["category_ids"], "tag_ids": tag_ids(x["tags"]), "related": x["related"],
        "eyecatch_prompt": x["eyecatch_prompt"], "eyecatch_main_html": x["eyecatch_main_html"],
        "eyecatch_subtitle": x["eyecatch_subtitle"], "eyecatch_main_size": x["eyecatch_main_size"],
        "body_images": resolved,
    }


if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[1] == "--verify":
        base.verify(sys.argv[3], make_cfg(sys.argv[2])["cta_url"])
    else:
        base.run(make_cfg(sys.argv[1]))
