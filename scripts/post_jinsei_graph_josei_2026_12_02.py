"""
【女性向け】どんな人と合う？人生グラフ（2026-12-02(水) 9:00 想定）。Wixには下書き保存のみ（publish:false）。
ネタ: drafts/neta_2026-11-25_muryosodan/neta.md ネタ3。共通ロジックは post_karikousai_line_2026_11.py と同じ。
使い方: python3 post_jinsei_graph_josei_2026_12_02.py     検証のみ: --verify <DRAFT_ID>
"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_karikousai_line_2026_11 as k
base, c, nr = k.base, k.c, k.nr
HERE = os.path.dirname(os.path.abspath(__file__))
base.D = os.path.join(HERE, "..", "drafts", "jinsei_graph_2026-12")
os.makedirs(base.D, exist_ok=True)

MD = os.path.join(HERE, "..", "drafts", "draft_2026-12-02_jinsei-graph-josei.md")
TITLE = open(MD, encoding="utf-8").readline()[2:].strip()
UTM = "2026-12-02-jinsei-graph-josei"
CTA = f"https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign={UTM}"
CAT = "69d23361-4fe7-4af6-a69e-2276e1f08417"  # 恋愛経験が少ない人の婚活（仮決定）

def load_draft(path):
    text = open(path, encoding="utf-8").read()
    body = text.split("## 本文\n", 1)[1].split("## 画像プロンプト", 1)[0].strip()
    blocks = [b for b in body.split("\n\n") if b.strip()]
    while blocks and blocks[-1].strip() == "---":
        blocks.pop()
    return TITLE, blocks
base.load_draft = load_draft

lines = [l.strip() for l in open(MD, encoding="utf-8").read().split("## 本文\n", 1)[1].split("\n")]
def line(prefix):
    hit = [l for l in lines if l.startswith(prefix)]
    assert len(hit) == 1, (prefix, len(hit))
    return hit[0]

W = "a beautiful Japanese woman in her 30s, East Asian appearance, black hair"
related = [p["id"] for p in requests.post(f"{c.WIX_BASE}/blog/v3/posts/query", headers=c.wix_headers(),
           json={"query": {"filter": {"categoryIds": {"$hasSome": [CAT]}}, "paging": {"limit": 3}}}).json()["posts"]]

cfg = {
    "draft_path": MD, "slug": "2026-12-02_jinsei_graph_josei", "cta_url": CTA,
    "excerpt": ("「自分はどんな人と合うのかわからない」と感じる女性へ。恋愛経験が少なくても大丈夫です。人生グラフと「一緒にいたい人トップ3」で、"
                "あなたが力を発揮できる相手の資質が見えてきます。愛媛・松山の仲人が、自分でできる自己分析のワークをお伝えします。"),
    "focus_keyword": "婚活 どんな人と合う 女性",
    "category_ids": [CAT],
    "tag_ids": nr.tag_ids(["婚活", "女性心理", "自己分析", "人生グラフ", "恋愛経験が少ない", "相性", "心構え", "心理学", "NLP", "愛媛 婚活"]),
    "related": related,
    "eyecatch_prompt": (W + ", smiling happily at a bright cafe table by a window, drawing a hand-drawn line graph on a notebook with a pen, "
                        "a cup of tea beside her, hopeful bright expression, wide shot"),
    "eyecatch_main_html": '「私は、どんな人と<br><span class="accent">合うんでしょう？」</span>',
    "eyecatch_subtitle": "――答えは、あなたの人生のグラフの中に隠れていました",
    "eyecatch_main_size": 58,
    "body_images": [
        (line("不安は性格ではなく、反応パターン。"),
         W + ", sitting on a bright sofa in a living room, holding a notebook and smiling gently with a relieved expression, natural daylight"),
        (line("それでは、実際にやってみましょう。"),
         W + ", at a bright wooden desk by a window with a blank sheet of paper and a pen, about to draw a graph, smiling with anticipation, no readable text"),
        (line("お見合いの日。"),
         W + ", in an elegant bright hotel lounge with a kind Japanese man in his 30s across the table nodding and listening, both smiling naturally, the woman relaxed, teacups on the table"),
    ],
}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        base.verify(sys.argv[2], CTA); sys.exit()
    did = base.run(cfg)
    r = requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(),
                       json={"draftPost": {"seoSlug": "jinsei-graph-aisho-josei"}, "fieldMask": "seoSlug"}, timeout=30)
    print("seoSlug:", r.status_code)
    print("DRAFT_ID", did)
