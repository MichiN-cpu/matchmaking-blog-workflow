"""
モーニングジャーナル第11期 あすなる版を婚活向けに差し替え（2026-09-26）
既存のWix下書き 6560b7ab を上書き更新する（新規作成しない・公開しない）。
画像は婚活向けに3枚とも新規生成。
"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(__file__))
import post_keikaku_josei_dansei_2026_09_common as common
import post_morning_journal_11th as mj

DRAFT_ID = "6560b7ab-0802-4a12-b18d-94560075591d"
DRAFTS = os.path.join(os.path.dirname(__file__), "..", "drafts")
BASE_STYLE = mj.BASE_STYLE

cfg = dict(mj.CFGS["asunaru"])
cfg.update({
    "draft_path": os.path.join(DRAFTS, "draft_2026-09-26_morning-journal-11th_asunaru_konkatsu.md"),
    "slug": "2026-09-26_morning-journal-11th_asunaru_konkatsu",
    "title": "【男女共通】婚活の「ぐるぐる」、朝のノートに置いてみませんか？――モーニングジャーナル第11期、10月5日スタート",
    "excerpt": "婚活中、あれこれ考えすぎて頭の中がぐるぐるしていませんか？ そのぐるぐるは、紙に書き出すだけで少しずつほどけていきます。結婚観や家族観の思い込みに気づき、望む未来を毎朝思い出す。婚活にこそ役立つ朝の15分「モーニングジャーナル」第11期は10月5日スタートです。",
    "focus_keyword": "婚活 考えすぎ ジャーナリング 朝活 松山",
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-09-26-morning-journal-11-konkatsu",
    "insert_after": [
        ("この「少し離れて眺める」ことが、婚活ではとても大きな力になります。", "sec", "書き出すと、少し離れて自分を眺められる。"),
        ("けっこう変わってくるんですよね。", "hope", "望む未来を、毎朝思い出す。"),
    ],
    "eyecatch_prompt": (BASE_STYLE + ", early morning, bright soft dawn light, a beautiful Japanese woman in her 30s with black hair "
        "in a light knit sweater writing in an open notebook at a clean white desk by a large window, relaxed and relieved expression "
        "with a gentle smile, a cup of tea beside the notebook, fresh and hopeful mood, wide shot, plenty of empty space in the lower left"),
    "section_prompt": (BASE_STYLE + ", morning, a Japanese man in his 30s with black hair in a casual shirt sitting at a bright kitchen table, "
        "pausing from writing in a notebook and looking at the page thoughtfully with a calm, clear expression, pen in hand, "
        "fresh morning light, tidy modern room"),
    "hope_prompt": (BASE_STYLE + ", a happy Japanese couple in their 30s with black hair having breakfast together at a bright dining table "
        "in the morning, facing each other and smiling at each other, not looking at camera, toast, salad and coffee on the table, "
        "fresh morning sunlight, warm relationship, clean white and light green interior"),
    "eyecatch_main_html": '婚活の「ぐるぐる」を、<br><span class="accent">朝のノート</span>に置いてみる。',
    "eyecatch_subtitle": "――モーニングジャーナル第11期 10月5日スタート",
    "eyecatch_main_size": 46,
})

common.WIX_SITE_ID = cfg["site_id"]
common.CATEGORY_IDS = cfg["category_ids"]
common.RELATED_POST_IDS = cfg["related_post_ids"]

nodes = mj.build_nodes(cfg["draft_path"], cfg["cta_url"], True)
body = {
    "draftPost": {
        "title": cfg["title"],
        "excerpt": cfg["excerpt"],
        "richContent": {"nodes": nodes, "metadata": {"version": 1}},
    },
    "fieldMask": "title,excerpt,richContent",
}
r = requests.patch(f"{common.WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}", headers=common.wix_headers(), json=body, timeout=30)
print("本文・タイトル・抜粋の差し替え:", "完了" if r.ok else f"失敗 {r.status_code} {r.text[:300]}")
if not r.ok:
    sys.exit(1)
common.set_seo(DRAFT_ID, cfg)
common.add_images(DRAFT_ID, cfg)
print(f"編集URL: https://manage.wix.com/dashboard/{common.WIX_SITE_ID}/blog/post/{DRAFT_ID}")
