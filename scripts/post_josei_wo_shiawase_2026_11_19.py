"""
【男性向け】女性を幸せにする（2026-11-19(木) 9:00 想定）。Wixには下書き保存のみ（publish:false）。
知人女性（結婚10年目）の話・ご本人掲載OK（11/11）。共通ロジックは post_karikousai_line_2026_11.py と同じ。
使い方: python3 post_josei_wo_shiawase_2026_11_19.py     検証のみ: --verify <DRAFT_ID>
"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_karikousai_line_2026_11 as k
base, c, nr = k.base, k.c, k.nr
HERE = os.path.dirname(os.path.abspath(__file__))
base.D = os.path.join(HERE, "..", "drafts", "josei_wo_shiawase_2026-11")
os.makedirs(base.D, exist_ok=True)

MD = os.path.join(HERE, "..", "drafts", "draft_2026-11-19_josei-wo-shiawase-ni.md")
TITLE = "【男性向け】「自分に女性を幸せにできるだろうか」と不安なあなたへ。―結婚10年目の妻の答えは、拍子抜けするほどシンプルでした"
UTM = "2026-11-19-josei-wo-shiawase-ni"
CTA = f"https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign={UTM}"

def load_draft(path):
    text = open(path, encoding="utf-8").read()
    body = text.split("## 本文\n", 1)[1].split("## 画像プロンプト", 1)[0].strip()
    blocks = [b for b in body.split("\n\n") if b.strip()]
    while blocks and blocks[-1].strip() == "---":
        blocks.pop()
    return TITLE, blocks
base.load_draft = load_draft

STYLE_M = "a kind-looking Japanese man in his 40s, East Asian appearance, black hair"
cfg = {
    "draft_path": MD, "slug": "2026-11-19_josei_wo_shiawase", "cta_url": CTA,
    "excerpt": ("「自分に女性を幸せにできるだろうか」と不安な男性へ。結婚10年目の知人女性が「この人と結婚してよかった」と気づいた瞬間は、特別な出来事ではありませんでした。"
                "公認心理師・仲人の中嶋美知が、女性を幸せにする男性が毎日続けていることを、愛媛・松山で婚活中の方へお話しします。"),
    "focus_keyword": "女性を幸せにする 自信がない",
    "category_ids": ["998b685d-1453-4ebd-8bd2-0218e315186e"],
    "tag_ids": nr.tag_ids(["婚活", "男性心理", "結婚生活", "パートナーシップ", "安全基地", "心構え", "心理学", "素直婚", "愛媛 婚活"]),
    "related": ["f71ec040-995d-4853-96b3-79d663703958", "d62fc137-2e3b-494b-bf2f-c4a121f342c4", "0c004668-d23a-40d3-a971-385f8dc6d799"],
    "eyecatch_prompt": (STYLE_M + " in a neat casual jacket walking home along a quiet residential street at dusk, "
                        "looking ahead with a calm, gently hopeful smile, warm house lights in the background, wide shot"),
    "eyecatch_main_html": '「自分に女性を<br><span class="accent">幸せにできるだろうか」</span>',
    "eyecatch_subtitle": "―結婚10年目の妻の答えは、拍子抜けするほどシンプルでした",
    "eyecatch_main_size": 58,
    "body_images": [
        ("彼女にとってご主人は、まさにこの安全基地になっていたんですね。",
         "a Japanese couple in their 40s at a bright dining table at home in the evening, the woman talking and smiling, the man listening attentively with a kind face, steaming mugs, East Asian appearance, black hair"),
        ("どれも、特別な才能はいりません。今日から、婚活中の今から、始められることばかりです。",
         STYLE_M + " gently wrapping a soft scarf around a smiling Japanese woman's neck at the entrance of a bright house on a chilly morning"),
        ("夜中にふと目が覚めたとき、隣に寝息が聞こえる。",
         "close-up of a Japanese couple's hands holding each other while walking along a calm seaside promenade at sunset, no faces visible, vivid clean colors"),
    ],
}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        base.verify(sys.argv[2], CTA); sys.exit()
    did = base.run(cfg)
    r = requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(),
                       json={"draftPost": {"seoSlug": "josei-wo-shiawase-ni"}, "fieldMask": "seoSlug"}, timeout=30)
    print("seoSlug:", r.status_code)
    print("DRAFT_ID", did)
