"""
2026-09-03: 3本の下書きに「出典」リンクを追記。
女性向け「その将来不安」記事には、みっちゃん本人の実体験エピソードも追加。
"""
import os, uuid, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"

def wix_headers():
    return {"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID, "Content-Type": "application/json"}

def nid():
    return str(uuid.uuid4())[:8]

def sp():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}
    ], "paragraphData": {}}

def p(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "paragraphData": {}}

def p_bold_small(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": text,
            "decorations": [{"type": "BOLD", "fontWeightValue": 700}],
        }}
    ], "paragraphData": {}}

def source_link_line(label, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {
            "text": "・" + label,
            "decorations": [
                {"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}},
            ],
        }}
    ], "paragraphData": {}}

def sources_block(items):
    nodes = [sp(), p_bold_small("【出典】")]
    for label, url in items:
        nodes.append(source_link_line(label, url))
    nodes.append(sp())
    return nodes

def find_index_after_text_contains(nodes, substr):
    for i, n in enumerate(nodes):
        if n.get("type") == "PARAGRAPH":
            for t in n.get("nodes", []):
                text = t.get("textData", {}).get("text", "")
                if substr in text:
                    return i
    return -1

def get_nodes(draft_id):
    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    return r.json()["draftPost"]["richContent"]["nodes"]

def patch_nodes(draft_id, nodes):
    patch_body = {"draftPost": {"richContent": {"nodes": nodes, "metadata": {"version": 1}}}, "fieldMask": "richContent"}
    rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=patch_body, timeout=30)
    print("  更新:", "完了" if rp.ok else f"失敗 {rp.status_code} {rp.text[:300]}")

# ---------- 1. 【男女共通】その「素敵な人」、写真の通りだと思いますか？ ----------
DRAFT_ANZEN = "c5b47c12-6ad3-4f05-9006-9f330c7ec906"
print("記事1（安全性）に出典を追加...")
nodes = get_nodes(DRAFT_ANZEN)
idx = find_index_after_text_contains(nodes, "仲人が間に入るからこそ、安心してその両方を大事にできるんです。")
if idx == -1:
    print("  挿入位置が見つかりません")
else:
    block = sources_block([
        ("警察庁「令和6年における特殊詐欺及びSNS型投資・ロマンス詐欺の状況」", "https://www.npa.go.jp/bureau/criminal/souni/tokusyusagi/hurikomesagi_toukei2024.pdf"),
        ("東京都消費生活総合センター「マッチングアプリを上手に利用しましょう」", "https://www.shouhiseikatu.metro.tokyo.lg.jp/trouble/matching_appli.html"),
    ])
    nodes[idx+1:idx+1] = block
    patch_nodes(DRAFT_ANZEN, nodes)

# ---------- 2. 【男性向け】夜、なんとなく手が伸びる一杯。 ----------
DRAFT_DANSEI = "3e9bd986-6d7e-4409-8657-b58387197ea4"
print("記事2（男性の寂しさ）に出典を追加...")
nodes = get_nodes(DRAFT_DANSEI)
idx = find_index_after_text_contains(nodes, '一人で抱え込まず、素直に「誰かと一緒にいたい」という気持ちを認めて、婚活という形で一歩を踏み出す。私はそうした素直な選び方を"素直婚"と呼んでいます。')
if idx == -1:
    print("  挿入位置が見つかりません")
else:
    block = sources_block([
        ("国立社会保障・人口問題研究所「第15回出生動向基本調査」結婚の利点", "https://www.ipss.go.jp/ps-doukou/j/doukou15/report15html/NFS15R_html02.html"),
        ("孤独と社会的孤立の健康リスクに関する研究解説（現代ビジネス）", "https://gendai.media/articles/-/125435"),
        ("配偶関係別の死亡年齢中央値分析（Yahoo!ニュース individual・荒川和久氏）", "https://news.yahoo.co.jp/expert/articles/afc7fac67c5e9a7cf41f0c1096096c5851c25872"),
    ])
    nodes[idx+1:idx+1] = block
    patch_nodes(DRAFT_DANSEI, nodes)

# ---------- 3. 【女性向け】その将来不安、一人で抱えなくていいのかもしれません。 ----------
DRAFT_JOSEI = "77e61211-46b1-433b-951f-afd39bfd4168"
print("記事3（女性の将来不安）に本人エピソード＋出典を追加...")
nodes = get_nodes(DRAFT_JOSEI)

# 3-1. ミニ診断の直後に、みっちゃん本人のエピソードを挿入
idx_anecdote = find_index_after_text_contains(nodes, "――どれか一つでも「あるかも」と思った方は、このあとの話が、きっと役に立ちます。")
if idx_anecdote == -1:
    print("  エピソード挿入位置が見つかりません")
else:
    anecdote_nodes = [
        sp(),
        p("実は私自身にも、覚えがあります。"),
        sp(),
        p("初めて車を買い替えるとき、何を基準に選べばいいのか分からないまま、一人で悩んだこと。窓の鍵が壊れてしまったときは、業者への連絡から修理の立ち会いまで、全部一人でこなしたこと。"),
        sp(),
        p('裏のお家が解体された影響で、家に初めてネズミが出てしまったときは、どうしていいか分からず本当に心細くて、「こんなときダーリンがいたらな」と思ったのを、今でも覚えています。'),
    ]
    nodes[idx_anecdote+1:idx_anecdote+1] = anecdote_nodes

# 3-2. 出典ブロックを末尾近くに追加
idx_source = find_index_after_text_contains(nodes, '強くあろうとする自分と、素直に頼りたい自分。そのどちらも我慢せず、両方を大事にしながら進んでいく婚活のかたちを、私は"素直婚"と呼んでいます。')
if idx_source == -1:
    print("  出典挿入位置が見つかりません")
else:
    block = sources_block([
        ("国立社会保障・人口問題研究所「第15回出生動向基本調査」結婚の利点", "https://www.ipss.go.jp/ps-doukou/j/doukou15/report15html/NFS15R_html02.html"),
        ("孤独と社会的孤立の健康リスクに関する研究解説（現代ビジネス）", "https://gendai.media/articles/-/125435"),
        ("内閣府「一人暮らし高齢者に関する意識調査結果」", "https://www8.cao.go.jp/kourei/ishiki/h26/kenkyu/gaiyo/pdf/kekka1.pdf"),
    ])
    nodes[idx_source+1:idx_source+1] = block

patch_nodes(DRAFT_JOSEI, nodes)

print("\n完了")
