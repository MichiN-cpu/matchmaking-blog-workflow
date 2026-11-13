"""
【男性向け】お見合いが組めない（2026-12-03(木) 9:00 想定）。Wixには下書き保存のみ（publish:false）。
みっちゃん口述（11/13）→本文OK（11/13、みっちゃん加筆済み）。共通ロジックは post_karikousai_line_2026_11.py と同じ。
使い方: python3 post_omiai_kumenai_dansei_2026_12_03.py     検証のみ: --verify <DRAFT_ID>
"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_karikousai_line_2026_11 as k
base, c, nr = k.base, k.c, k.nr
HERE = os.path.dirname(os.path.abspath(__file__))
base.D = os.path.join(HERE, "..", "drafts", "omiai_kumenai_2026-12")
os.makedirs(base.D, exist_ok=True)

MD = os.path.join(HERE, "..", "drafts", "draft_2026-12-03_omiai-kumenai-dansei.md")
TITLE = "【男性向け】お見合いがなかなか決まらない？―女性がプロフィールで、本当に見ているもの"  # 11/13みっちゃんがWixで変更
UTM = "2026-12-03-omiai-kumenai-dansei"
CTA = f"https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign={UTM}"

def load_draft(path):
    text = open(path, encoding="utf-8").read()
    body = text.split("## 本文\n", 1)[1].split("## 画像プロンプト", 1)[0].strip()
    blocks = [b for b in body.split("\n\n") if b.strip()]
    while blocks and blocks[-1].strip() == "---":
        blocks.pop()
    return TITLE, blocks
base.load_draft = load_draft

STYLE_M = "a friendly-looking Japanese man in his early 40s, East Asian appearance, short neat black hair, clean-shaven"
cfg = {
    "draft_path": MD, "slug": "2026-12-03_omiai_kumenai_dansei", "cta_url": CTA,
    "excerpt": ("お見合いの申し込みをしても、なかなか組めない男性へ。女性がプロフィールで見ているのは「清潔感と笑顔」と「将来の安心感」です。"
                "プロ撮影の写真で気をつけたいポイント、条件で勝負しなくても安心を伝えられるプロフィール文の書き方を、愛媛・松山の仲人がお伝えします。"),
    "focus_keyword": "お見合い 組めない 男性",
    "category_ids": ["5089ac63-e2ce-4de1-b472-3512a77401af"],  # お見合い
    "tag_ids": nr.tag_ids(["婚活", "お見合い", "男性心理", "プロフィール写真", "プロフィール文", "第一印象", "清潔感", "損失回避", "心理学", "愛媛 婚活"]),
    "related": ["e1155633-e7b8-4179-8a0d-1283da56565c", "58079daf-693b-48bd-b4e0-9bfcc0ae918d", "96068104-095f-4934-b2bc-db6f60b98e11"],
    "eyecatch_prompt": (STYLE_M + " in a well-fitted navy suit and white shirt, standing relaxed with a natural warm smile "
                        "in a bright clean photo studio with a soft light-gray backdrop, photographer's softbox light visible at the edge, wide shot"),
    "eyecatch_main_html": '申し込みの返事を見るたび、<br><span class="accent">ため息が出てしまうあなたへ</span>',
    "eyecatch_subtitle": "―女性がプロフィールで、本当に見ているもの",
    "eyecatch_main_size": 52,
    "body_images": [
        ("社会心理学の研究では、人は顔写真をほんの0.1秒見ただけで「信頼できそうか」「感じがよさそうか」を判断し始めることが分かっています。そして、その印象は、時間をかけて見直してもあまり変わらないそうです。",
         "a Japanese woman in her 30s sitting on a sofa in a bright living room, scrolling through profiles on a tablet with a thoughtful gentle expression, East Asian appearance, black hair, screen not visible"),
        ("それは、将来が不安だからです。",
         STYLE_M + " in a casual knit sweater packing a homemade bento lunch box in a bright clean kitchen in the morning, smiling softly"),
        ("自分のこととして、主体的に関わっていく。その姿勢が、対等な夫婦関係を望む多くの女性に、大きな安心感を与えてくれます。",
         "a young Japanese couple in their 30s cooking together side by side in a bright modern kitchen, laughing naturally, East Asian appearance, black hair, the man chopping vegetables"),
    ],
}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        base.verify(sys.argv[2], CTA); sys.exit()
    did = base.run(cfg)
    r = requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(),
                       json={"draftPost": {"seoSlug": "omiai-kumenai-dansei"}, "fieldMask": "seoSlug"}, timeout=30)
    print("seoSlug:", r.status_code)
    print("DRAFT_ID", did)
