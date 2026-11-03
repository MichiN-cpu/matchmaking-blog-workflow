"""
【男女共通】2026-11-29(日)想定  神無月に伊勢へ。神様から教わった、夫婦のこと
（11/3 みっちゃんのモーニングジャーナルの気づき→口述→みっちゃん確認済み）。Wixには下書き保存のみ（publish:false）。
共通ロジックは post_omiai_josei_2026_10_14.py の run(cfg)／tag_ids は post_norichan_2026_11.py。
使い方: python3 post_kannazuki_2026_11.py        検証のみ: python3 post_kannazuki_2026_11.py --verify <DRAFT_ID>
⚠️ 伊勢から帰ったあと（11/20以降）に「行ってきました」の一文と顔を隠した写真を追加予定。
"""
import os, sys, requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_omiai_josei_2026_10_14 as base
import post_norichan_2026_11 as nori
c = base.c

HERE = os.path.dirname(os.path.abspath(__file__))
base.D = os.path.join(HERE, "..", "drafts", "kannazuki_2026-11")

CAT_ROADMAP = "998b685d-1453-4ebd-8bd2-0218e315186e"  # 成婚までのロードマップ
SEO_SLUG = "kami-no-tantouwake"

X = {
    "md": "kyotsu_kannazuki.md",
    "slug": "2026-11-29_kyotsu_kannazuki",
    "utm": "2026-11-29-kyotsu-kannazuki",
    "category_ids": [CAT_ROADMAP],
    "excerpt": ("神無月、伊勢の神様は出雲に行かない？ 結婚報告参拝の準備で知った神様の「担当分け」から、"
                "公認心理師・仲人の中嶋美知が、夫婦の役割分担、ふたりで定期的に相談すること、違う人生を生きてきたふたりだから広がる世界についてお話しします。"),
    "focus_keyword": "夫婦 役割分担 パートナーシップ",
    "tags": ["婚活", "パートナーシップ", "結婚生活", "夫婦関係", "役割分担", "話し合う", "再婚", "伊勢神宮", "心理学", "NLP"],
    "related": ["54ddc242-fc91-4f71-8d4a-c5914805df56",   # 仲良し夫婦の共通点
                "341ba8cc-5c75-41fa-b497-6a8a245952fe",   # 尊重してリードする
                "5f06cf7f-c400-48ff-bc56-5feb72990223"],  # 弱さを見せてもいい
    "eyecatch_prompt": ("a Japanese couple in their 50s seen from behind walking side by side on a gravel path toward a large plain wooden "
        "shrine gate surrounded by tall cedar trees, calm sacred forest atmosphere, wide shot, bright clear morning daylight"),
    "eyecatch_main_html": '神様にも<br><span class="accent">「担当分け」</span>が<br>あるそうです。',
    "eyecatch_subtitle": "――神無月の伊勢参りで気づいた、夫婦のこと",
    "eyecatch_main_size": 60,
    "body_images": [
        ("急に不安になって（汗）、慌てて調べてみました。",
         "a Japanese woman in her 50s at a bright home table in the morning with an open notebook and a smartphone, "
         "looking at the phone with a curious surprised expression, a cup of tea beside her, natural daylight"),
        ("決まった瞬間から、ふたりの役割が自然と分かれていったんですね。",
         "a Japanese couple in their 50s in a car on a sunny countryside road, the man driving with a relaxed smile, "
         "the woman in the passenger seat cheerfully talking and holding a travel guidebook, seen from the side, bright daylight"),
        ("それだけで、ふたりの関係はずいぶん楽になるんです。",
         "a Japanese couple in their 50s sitting side by side at a bright dining table with tea cups and a small notebook, "
         "talking and planning together with warm smiles, relaxed atmosphere, natural daylight"),
    ],
}


def make_cfg():
    path = os.path.join(base.D, X["md"])
    lines = open(path, encoding="utf-8").read().split("\n")
    resolved = []
    for prefix, prompt in X["body_images"]:
        hit = [l.strip() for l in lines if l.strip().startswith(prefix)]
        assert len(hit) == 1, f"挿入位置が一意に特定できません: {prefix} -> {len(hit)}"
        resolved.append((hit[0], prompt))
    return {
        "draft_path": path, "slug": X["slug"],
        "cta_url": f"https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign={X['utm']}",
        "excerpt": X["excerpt"], "focus_keyword": X["focus_keyword"],
        "category_ids": X["category_ids"], "tag_ids": nori.tag_ids(X["tags"]), "related": X["related"],
        "eyecatch_prompt": X["eyecatch_prompt"], "eyecatch_main_html": X["eyecatch_main_html"],
        "eyecatch_subtitle": X["eyecatch_subtitle"], "eyecatch_main_size": X["eyecatch_main_size"],
        "body_images": resolved,
    }


def set_slug(did):
    r = requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(),
                       json={"draftPost": {"seoSlug": SEO_SLUG}, "fieldMask": "seoSlug"}, timeout=30)
    print("seoSlug:", r.status_code, r.json().get("draftPost", {}).get("seoSlug") if r.ok else r.text[:300])


if __name__ == "__main__":
    cfg = make_cfg()
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        base.verify(sys.argv[2], cfg["cta_url"])
    else:
        did = base.run(cfg)
        set_slug(did)
