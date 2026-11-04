"""
男性向けLINE記事2本（仮交際）。Wixには下書き保存のみ（publish:false）。
  henji   : 2026-11-05(木)想定  返事が来ない／遅い
  kakukoto: 2026-11-12(木)想定  何を書けばいいかわからない
使い方: python3 post_karikousai_line_2026_11.py henji|kakukoto
検証のみ: python3 post_karikousai_line_2026_11.py --verify <henji|kakukoto> <DRAFT_ID>
共通ロジックは post_omiai_josei_2026_10_14.py の run(cfg)（本文の読み込み・ミニ診断の箇条書きだけ差し替え）。
"""
import os, sys, requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_omiai_josei_2026_10_14 as base
import post_norichan_2026_11 as nr
c = base.c
HERE = os.path.dirname(os.path.abspath(__file__))
base.D = os.path.join(HERE, "..", "drafts", "karikousai_line_2026-11")
os.makedirs(base.D, exist_ok=True)

CAT_KARIKOUSAI = "3f5f378d-a4f4-47e0-90a7-ab4daa27504e"  # 仮交際 （仮決定）
TITLES = {}


def load_draft(path):
    text = open(path, encoding="utf-8").read()
    body = text.split("## 本文\n", 1)[1].strip()
    return TITLES[path], [b for b in body.split("\n\n") if b.strip()]


def bullet_list(items):
    li = [{"type": "LIST_ITEM", "id": c.nid(), "nodes": [c.p(t)]} for t in items]
    return {"type": "BULLETED_LIST", "id": c.nid(), "nodes": li}


def build_nodes(blocks, cta_url, images):
    nodes = []
    for block in blocks:
        b = block.strip()
        if b == "---":
            continue
        if b.startswith("## "):
            nodes.extend(c.section_heading(b[3:].strip()))
            continue
        if nodes:
            nodes.append(c.sp())
        lines = [l.strip() for l in b.split("\n") if l.strip()]
        if b.startswith("（ここに本人の実写"):
            nodes.append(c.real_photo_node())
        elif b.startswith("⬇️"):
            nodes.extend(c.cta_nodes(cta_url))
        elif lines and all(l.startswith("・") for l in lines):
            nodes.append(bullet_list([l[1:].strip() for l in lines]))
        else:
            for line in lines:
                nodes.append(c.p(line))
                if line in images:
                    nodes.extend([c.sp(), c.image_node(images[line]), c.sp()])
    return nodes


base.load_draft = load_draft
base.build_nodes = build_nodes

CFGS = {
 "henji": {
    "md": "draft_2026-11-05_karikousai-line.md",
    "title": "【男性向け】既読を確かめるたび、気分が沈んでいく。――返事が遅い彼女を、責めたくなる前に知ってほしいこと",
    "slug": "2026-11-05_karikousai_line_henji", "seo_slug": "karikousai-line-henji",
    "utm": "2026-11-05-karikousai-line-henji",
    "excerpt": ("仮交際中、LINEの返事が遅いと「事故かも」「誠実じゃないのでは」と悪い想像が膨らんでしまう男性へ。公認心理師・仲人の中嶋美知が、"
                "想像が現実を連れてくる仕組みと、気持ちがラクになる想像の入れ替え方、スマホとの距離感の確かめ方を、愛媛・松山で婚活中の方へお話しします。"),
    "focus_keyword": "仮交際 LINE 返事が来ない",
    "tags": ["婚活", "仮交際", "男性心理", "LINE", "コミュニケーション", "心構え", "パートナーシップ", "予言の自己成就", "心理学", "NLP"],
    "eyecatch_prompt": ("a kind-looking Japanese man in his 30s in a neat smart casual jacket sitting by a bright window at a cafe, "
        "holding a smartphone loosely and looking at it with a thoughtful expression with a faint hopeful smile, wide shot"),
    "eyecatch_main_html": '既読を確かめるたび、<br><span class="accent">気分が沈んでいく。</span>',
    "eyecatch_subtitle": "――返事が遅い彼女を、責めたくなる前に知ってほしいこと",
    "eyecatch_main_size": 60,
    "body_images": [
        ("不安は性格ではなく、反応パターン。パターンなら、変えていけます。",
         "a kind-looking Japanese man in his 30s sitting on a sofa in a bright living room looking at his smartphone with a thoughtful face turning into a gentle smile, natural daylight"),
        ("プライベートの時間を充実させている女性ほど",
         "a beautiful Japanese woman in her 30s enjoying her evening hobby at home, painting or doing skincare at a bright dressing table, smartphone lying far away on a shelf, relaxed happy smile"),
        ("この一通を受け取った女性は",
         "a beautiful Japanese woman in her 30s sitting at a bright cafe window seat reading a message on her smartphone with a happy relieved smile"),
    ],
 },
 "kakukoto": {
    "md": "draft_2026-11-12_karikousai-line-kakukoto.md",
    "title": "【男性向け】「仮交際に進めたけれど、毎日何を書けば？」――短い一行でも女性が喜ぶLINEのコツ",
    "slug": "2026-11-12_karikousai_line_kakukoto", "seo_slug": "karikousai-line-kakukoto",
    "utm": "2026-11-12-karikousai-line-kakukoto",
    "excerpt": ("仮交際中、LINEに何を書けばいいかわからない男性へ。公認心理師・仲人の中嶋美知が、男性会員さんからいちばん多い相談に答えます。"
                "LINEは「情報」ではなく「気持ち」のやりとり。短くていい理由と、そのまま使える例文、返事が来たときの共感の返し方を、愛媛・松山で婚活中の方へお話しします。"),
    "focus_keyword": "仮交際 LINE 何を送る",
    "tags": ["婚活", "仮交際", "男性心理", "LINE", "コミュニケーション", "心構え", "パートナーシップ", "バックトラッキング", "心理学", "NLP"],
    "eyecatch_prompt": ("a kind-looking Japanese man in his 30s in a neat smart casual jacket smiling gently while typing on his smartphone, "
        "sitting at a bright cafe table by a window, wide shot"),
    "eyecatch_main_html": '「仮交際に進めたけれど、<br><span class="accent">毎日何を書けば？」</span>',
    "eyecatch_subtitle": "――短い一行でも女性が喜ぶLINEのコツ",
    "eyecatch_main_size": 56,
    "body_images": [
        ("不安は性格ではなく、反応パターン。パターンなら、使い方を変えるだけで、ぐっとラクになります。",
         "a kind-looking Japanese man in his 30s at a bright home desk with a smartphone in hand, smiling gently as he thinks of what to write, natural daylight"),
        ("街を歩いていて",
         "beautiful autumn flowers blooming in a sunny city street flower bed, a hand holding a smartphone taking a photo of them, no faces visible, vivid clean colors"),
        ("彼女が「今日、やっと企画が通ったんです！」",
         "a Japanese man and woman in their 30s sitting across from each other at a bright cafe table, the woman happily telling a story, the man smiling and nodding warmly with a kind expression, natural daylight"),
    ],
 },
}


def make_cfg(name):
    x = CFGS[name]
    path = os.path.join(HERE, "..", "drafts", x["md"])
    TITLES[path] = x["title"]
    lines = open(path, encoding="utf-8").read().split("## 本文\n", 1)[1].split("\n")
    resolved = []
    for prefix, prompt in x["body_images"]:
        hit = [l.strip() for l in lines if l.strip().startswith(prefix)]
        assert len(hit) == 1, f"挿入位置が一意に特定できません: {prefix} -> {len(hit)}"
        resolved.append((hit[0], prompt))
    related = [p["id"] for p in requests.post(f"{c.WIX_BASE}/blog/v3/posts/query", headers=c.wix_headers(),
               json={"query": {"filter": {"categoryIds": {"$hasSome": [CAT_KARIKOUSAI]}}, "paging": {"limit": 3}}}).json()["posts"]]
    return {
        "draft_path": path, "slug": x["slug"], "seo_slug": x["seo_slug"],
        "cta_url": f"https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign={x['utm']}",
        "excerpt": x["excerpt"], "focus_keyword": x["focus_keyword"],
        "category_ids": [CAT_KARIKOUSAI], "tag_ids": nr.tag_ids(x["tags"]), "related": related,
        "eyecatch_prompt": x["eyecatch_prompt"], "eyecatch_main_html": x["eyecatch_main_html"],
        "eyecatch_subtitle": x["eyecatch_subtitle"], "eyecatch_main_size": x["eyecatch_main_size"],
        "body_images": resolved,
    }


if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[1] == "--verify":
        base.verify(sys.argv[3], make_cfg(sys.argv[2])["cta_url"])
    else:
        cfg = make_cfg(sys.argv[1])
        did = base.run(cfg)
        r = requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(),
                           json={"draftPost": {"seoSlug": cfg["seo_slug"]}, "fieldMask": "seoSlug"}, timeout=30)
        print("seoSlug:", r.status_code, r.json().get("draftPost", {}).get("seoSlug") if r.ok else r.text[:300])
