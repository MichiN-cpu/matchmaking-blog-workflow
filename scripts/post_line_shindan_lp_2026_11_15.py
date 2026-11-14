"""
Google広告（デマンドジェネ）の飛び先用：結婚力診断の案内ページ（ブログ記事形式・asunaru.jp内）。
2026-11-15作成。Wixには下書き保存のみ（publish:false）。みっちゃん確認→公開→広告の最終URLを差し替え。
CTA：結婚力診断（計測リンク Ok4zdLo）／LINE友だち追加（iZtuNiW）／無料相談（/soudan UTM付き）
共通ロジックは post_karikousai_line_2026_11.py（build_nodes）＋ post_omiai_josei_2026_10_14.py（run）。
使い方: python3 post_line_shindan_lp_2026_11_15.py     検証のみ: --verify <DRAFT_ID>
"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_karikousai_line_2026_11 as k
base, c, nr = k.base, k.c, k.nr
HERE = os.path.dirname(os.path.abspath(__file__))
base.D = os.path.join(HERE, "..", "drafts", "line_shindan_lp_2026-11")
os.makedirs(base.D, exist_ok=True)

MD = os.path.join(HERE, "..", "drafts", "draft_2026-11-15_line-shindan-lp.md")
TITLE = "【2分でできる】結婚力診断｜あなたの婚活パターンと処方箋を、LINEでお届けします"
SHINDAN = "https://line-harness.design-3333.workers.dev/t/Ok4zdLo"
LINE_ADD = "https://line-harness.design-3333.workers.dev/t/iZtuNiW"
SOUDAN = "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=line-shindan-lp"


def lp_cta_nodes(_cta_url):
    return [
        c.link_node_centered("⬇️2分でわかる！結婚力診断はこちら（無料）⬇️", SHINDAN),
        c.link_node_centered("▶ 結婚力診断をはじめる", SHINDAN, underline=True),
        c.sp(),
        c.p("先にLINEだけ登録しておきたい方は、こちらからどうぞ。"),
        c.link_node_centered("▶ あすなる愛媛の公式LINEを友だち追加する", LINE_ADD, underline=True),
        c.sp(),
        c.p("直接お話ししてみたい方は、無料相談も承っております。"),
        c.link_node_centered("▶ 無料相談のご案内", SOUDAN, underline=True),
    ]
c.cta_nodes = lp_cta_nodes


def load_draft(path):
    text = open(path, encoding="utf-8").read()
    body = text.split("## 本文\n", 1)[1].strip()
    return TITLE, [b for b in body.split("\n\n") if b.strip()]
base.load_draft = load_draft


def related_from_category(cat, n=3):
    r = requests.get(f"{c.WIX_BASE}/blog/v3/posts?categoryIds={cat}&paging.limit={n}&sort=PUBLISHED_DATE_DESC",
                     headers=c.wix_headers(), timeout=30).json()
    return [p["id"] for p in r.get("posts", [])][:n]


CAT = "641187e4-a409-4c2f-9639-ecc548f26f15"  # 無料相談の前に読む
STYLE_W = "a friendly Japanese woman in her 30s, East Asian appearance, black hair"
cfg = {
    "draft_path": MD, "slug": "2026-11-15_line_shindan_lp", "cta_url": SHINDAN,
    "excerpt": ("6つの質問に答えるだけ、約2分でできる「結婚力診断」。婚活でくり返しやすいあなたのパターンと、それを変えていく処方箋を、"
                "あすなる愛媛の公式LINEでお届けします。公認心理師・仲人の中嶋美知（愛媛・松山）がつくった無料の診断です。"),
    "focus_keyword": "婚活 診断",
    "category_ids": [CAT],
    "tag_ids": nr.tag_ids(["婚活", "婚活診断", "LINE", "心理学", "無料相談", "愛媛 婚活", "女性心理", "男性心理"]),
    "related": related_from_category(CAT),
    "eyecatch_prompt": (STYLE_W + " sitting on a sofa in a bright living room, holding a smartphone and smiling with a curious, "
                        "pleasantly surprised expression as if discovering something about herself, wide shot"),
    "eyecatch_main_html": '2分でわかる、<br><span class="accent">あなたの婚活パターン</span>',
    "eyecatch_subtitle": "―結果と処方箋は、LINEでお届けします",
    "eyecatch_main_size": 56,
    "body_images": [
        ("パターンが分かれば、変えていくことができます。",
         STYLE_W + " walking on a sunny street lined with trees, looking ahead with a light relaxed smile, natural daylight"),
        ("女性向けと男性向けの2種類があります。",
         "close-up of a woman's hands holding a smartphone, tapping an answer on a simple quiz screen with pastel buttons, bright cafe table, screen content blurred"),
        ("読むだけでも大丈夫です。",
         STYLE_W + " relaxing with a cup of tea at a bright window, reading a message on her smartphone with a warm, relieved smile"),
    ],
}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        base.verify(sys.argv[2], SHINDAN); sys.exit()
    did = base.run(cfg)
    r = requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(),
                       json={"draftPost": {"seoSlug": "line-shindan"}, "fieldMask": "seoSlug"}, timeout=30)
    print("seoSlug:", r.status_code)
    print("DRAFT_ID", did)
