"""
【男性向け】きっかけLINE（2026-11-26(木) 9:00 想定）。Wixには下書き保存のみ（publish:false）。
みっちゃんとダーリンのLINE（VOICE_MEMOS 11/11）。みっちゃん本文OK（11/12）。共通ロジックは post_karikousai_line_2026_11.py と同じ。
使い方: python3 post_josei_wo_shiawase_2026_11_19.py     検証のみ: --verify <DRAFT_ID>
"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_karikousai_line_2026_11 as k
base, c, nr = k.base, k.c, k.nr
HERE = os.path.dirname(os.path.abspath(__file__))
base.D = os.path.join(HERE, "..", "drafts", "line_kikkake_2026-11")
os.makedirs(base.D, exist_ok=True)

MD = os.path.join(HERE, "..", "drafts", "draft_2026-11-26_line-kikkake-dansei.md")
TITLE = "【男性向け】LINEを開いても、指が止まってしまうあなたへ。―59歳で結婚した仲人の夫が、毎朝送ってくる一枚の写真"
UTM = "2026-11-26-line-kikkake-dansei"
CTA = f"https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign={UTM}"

def load_draft(path):
    text = open(path, encoding="utf-8").read()
    body = text.split("## 本文\n", 1)[1].split("## 画像プロンプト", 1)[0].strip()
    blocks = [b for b in body.split("\n\n") if b.strip()]
    while blocks and blocks[-1].strip() == "---":
        blocks.pop()
    return TITLE, blocks
base.load_draft = load_draft

STYLE_M = "a kind-looking Japanese man in his 50s, East Asian appearance, black hair with a little gray"
cfg = {
    "draft_path": MD, "slug": "2026-11-26_line_kikkake_dansei", "cta_url": CTA,
    "excerpt": ("LINEが苦手で、何を送ればいいかわからない男性へ。59歳で結婚した仲人・中嶋美知の夫が、交際中から今も続けている「きっかけLINE」をご紹介します。"
                "毎朝の運勢の写真、今日したことの一言、相手の話を覚えて返すコツなど、そのまま真似できるアイディアを愛媛・松山で婚活中の方へお届けします。"),
    "focus_keyword": "LINE 苦手 男性 婚活",
    "category_ids": ["3f5f378d-a4f4-47e0-90a7-ab4daa27504e"],
    "tag_ids": nr.tag_ids(["婚活", "仮交際", "男性心理", "LINE", "コミュニケーション", "単純接触効果", "自己開示", "心理学", "素直婚", "愛媛 婚活"]),
    "related": ["e6e786eb-4f44-4ae7-84a6-236cc046d4c4", "19c9bbaf-2fc1-454b-86f0-cd9692ec2ebc", "c04b8a01-c0e6-4ac9-8b75-b9aa34eb6e43"],
    "eyecatch_prompt": (STYLE_M + " in a neat sweater sitting at a bright breakfast table in the morning, "
                        "smiling gently while taking a photo of a folded newspaper with his smartphone, cup of coffee, wide shot"),
    "eyecatch_main_html": 'LINEを開いても、<br><span class="accent">指が止まってしまうあなたへ</span>',
    "eyecatch_subtitle": "―59歳で結婚した仲人の夫が、毎朝送ってくる一枚の写真",
    "eyecatch_main_size": 56,
    "body_images": [
        ("社会心理学には「単純接触効果」という考え方があります。人は、何度も接するものに、自然と親しみを感じるようになるんです。内容は、大したことでなくていい。毎日届く、ということそのものが、安心と親しみを育ててくれます。",
         "a Japanese woman in her 50s smiling softly while looking at her smartphone by a sunny kitchen window in the morning, holding a cup of tea, East Asian appearance, black hair"),
        ("社会心理学には「自己開示の返報性」という考え方があります。自分のことを少し話すと、相手も自分のことを話しやすくなる、という心の働きです。あなたの「今日したこと」の一言が、彼女の「今日したこと」を引き出してくれるんですね。",
         STYLE_M + " in golf wear sitting on a bench at a green golf course on a clear day, smiling while typing a message on his smartphone"),
        ("家族社会学や家族療法の分野では、「おはよう」「おやすみ」のような、ふたりの間で毎日くり返される小さな習慣を「儀式（リチュアル）」と呼び、関係を安定させる力があると考えられています。毎朝の運勢写メも、ふたりだけの小さな儀式になっているんですね。",
         "close-up of a smartphone on a wooden breakfast table next to a folded newspaper and two coffee cups in bright morning light, no faces visible, vivid clean colors"),
    ],
}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        base.verify(sys.argv[2], CTA); sys.exit()
    did = base.run(cfg)
    r = requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(),
                       json={"draftPost": {"seoSlug": "line-kikkake-dansei"}, "fieldMask": "seoSlug"}, timeout=30)
    print("seoSlug:", r.status_code)
    print("DRAFT_ID", did)
