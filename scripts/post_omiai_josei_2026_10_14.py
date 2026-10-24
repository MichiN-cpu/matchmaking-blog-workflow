"""
【女性向け】お見合いで、本当は聞かれたくないことがあるあなたへ。
2026-10-12作成 → 2026-10-14(水) 9:00 想定。Wixには下書き保存のみ（publish:false）。
テンプレート: post_junco_nail_2026_10_09.py / post_keikaku_josei_dansei_2026_09_common.py

共通ロジック run(cfg) は男性向け post_omiai_dansei_2026_10_15.py からも使う。
- 下書き .md の1行＝1PARAGRAPHノード、空行区切り→sp、`---`＋`## 見出し`→sp→DIVIDER→sp→HEADING(H2)
- 「（ここに本人の実写カウンセリング写真）」→実写写真ノード（SMALL・CENTER）
- 末尾CTA→2段落・中央寄せ・両方LINK（UTM付き）
- 本文差し込み画像3枚（gpt-image-1、SMALL・CENTER）、カバーは compose_eyecatch() で文字焼き込み
"""
import os, sys, base64, requests

sys.path.insert(0, os.path.dirname(__file__))
import post_keikaku_josei_dansei_2026_09_common as c
from eyecatch_composer import compose_eyecatch

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "drafts", "omiai_2026-10")
CATEGORY_OMIAI = "5089ac63-e2ce-4de1-b472-3512a77401af"  # お見合い

BASE_STYLE = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
              "clear skin, bright eyes, real-world setting, professional lifestyle photography style, "
              "shallow depth of field, clean bright modern atmosphere, no text, no warm yellowish tint, "
              "warm genuine smile, eyes bright with hope, NOT downcast, NOT teary, NOT vacant, "
              "clean bright natural daylight, crisp clean colors, vivid but neutral tones, "
              "NOT pale, NOT desaturated, NOT gloomy, NOT sepia")

OMIAI_STYLE = ("facing each other, looking at each other not at camera, the man in a neat dark suit with a dress shirt, the woman in a soft pink or white elegant dress, hair down with gentle blow-dried wave, loose and flowing, not tied up, ")

PHOTO_PLACEHOLDER = "（ここに本人の実写カウンセリング写真）"


def load_draft(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    assert lines[0].startswith("# "), "1行目がタイトルではありません"
    title = lines[0][2:].strip()
    body = "\n".join(lines[1:]).strip()
    return title, [b for b in body.split("\n\n") if b.strip()]


def build_nodes(blocks, cta_url, images):
    """images: {挿入直後にしたい行の全文: file_obj}"""
    nodes = []
    for block in blocks:
        b = block.strip()
        if b == "---":
            continue  # 区切り線は次の見出しの section_heading で入れる
        if b.startswith("## "):
            nodes.extend(c.section_heading(b[3:].strip()))
            continue
        if nodes:
            nodes.append(c.sp())
        if b == PHOTO_PLACEHOLDER:
            nodes.append(c.real_photo_node())
        elif b.startswith("⬇️"):
            nodes.extend(c.cta_nodes(cta_url))
        else:
            for line in b.split("\n"):
                line = line.strip()
                if not line:
                    continue
                nodes.append(c.p(line))
                if line in images:
                    nodes.extend([c.sp(), c.image_node(images[line]), c.sp()])
    return nodes


def generate_image(prompt, local_path):
    if os.path.exists(local_path):
        print("  既存画像を再利用:", os.path.basename(local_path))
        return local_path
    print("[gpt-image-1] generating:", os.path.basename(local_path))
    resp = c.client.images.generate(model="gpt-image-1.5", prompt=prompt, size="1536x1024", quality="high", n=1)
    with open(local_path, "wb") as f:
        f.write(base64.b64decode(resp.data[0].b64_json))
    return local_path


def verify(did, cta_url):
    r = requests.get(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}?fieldsets=CONTENT",
                     headers=c.wix_headers(), timeout=30)
    r.raise_for_status()
    d = r.json()["draftPost"]
    nodes = d["richContent"]["nodes"]
    imgs = [n for n in nodes if n["type"] == "IMAGE"]
    real = [n for n in imgs if "cf3f0f8fec8d40e4ac0e0bb6dfc4771d" in str(n)]
    ctas = [n for n in nodes if n["type"] == "PARAGRAPH" and cta_url in str(n)
            and n.get("paragraphData", {}).get("textStyle", {}).get("textAlignment") == "CENTER"]
    heads = [n for n in nodes if n["type"] == "HEADING"]
    divs = [n for n in nodes if n["type"] == "DIVIDER"]
    media = d.get("media", {}).get("wixMedia", {}).get("image", {})
    seo = d.get("seoData", {})
    kws = seo.get("settings", {}).get("keywords", [])
    desc = [t for t in seo.get("tags", []) if t.get("props", {}).get("name") == "description"]
    print("---- VERIFY ----")
    print("status:", d.get("status"), "| title:", d.get("title"))
    print("categoryIds:", d.get("categoryIds"), "| tags:", len(d.get("tagIds", [])),
          "| related:", len(d.get("relatedPostIds", [])))
    print("IMAGE nodes:", len(imgs), "(実写:", len(real), ") | HEADING:", len(heads), "| DIVIDER:", len(divs))
    for n in imgs:
        print("   ", n["imageData"]["image"]["src"].get("url", n["imageData"]["image"]["src"].get("id", ""))[:90],
              n["imageData"].get("containerData", {}).get("width"))
    print("CTA中央寄せ＋LINK段落:", len(ctas))
    print("cover:", media.get("url", "なし")[:90], "| displayed:", d.get("media", {}).get("displayed"))
    print("focus keyword:", kws, "| meta description:", bool(desc))
    print("excerpt:", (d.get("excerpt") or "")[:60])
    for u in [media.get("url")] + [n["imageData"]["image"]["src"].get("url") for n in imgs]:
        if u:
            print("   HTTP", requests.head(u, timeout=20).status_code, u[-40:])


def run(cfg):
    title, blocks = load_draft(cfg["draft_path"])
    slug = cfg["slug"]

    # 本文差し込み画像3枚
    images = {}
    for i, (after_line, prompt) in enumerate(cfg["body_images"], 1):
        assert any(after_line in b.split("\n") for b in blocks), f"挿入位置が見つかりません: {after_line[:20]}"
        path = generate_image(BASE_STYLE + ", " + prompt, os.path.join(D, f"{slug}_body{i}.png"))
        fo = c.upload_image_file(path, f"{slug}_body{i}.png")
        assert fo, f"body{i} upload failed"
        images[after_line] = fo

    nodes = build_nodes(blocks, cfg["cta_url"], images)
    body = {"draftPost": {"title": title, "richContent": {"nodes": nodes, "metadata": {"version": 1}},
            "categoryIds": cfg.get("category_ids", [CATEGORY_OMIAI]), "tagIds": cfg["tag_ids"], "relatedPostIds": cfg["related"],
            "excerpt": cfg["excerpt"], "memberId": c.MEMBER_ID}, "publish": False}
    r = requests.post(f"{c.WIX_BASE}/blog/v3/draft-posts", headers=c.wix_headers(), json=body, timeout=30)
    print("draft create:", r.status_code)
    if not r.ok:
        print(r.text[:500]); r.raise_for_status()
    did = r.json()["draftPost"]["id"]

    c.set_seo(did, {"title": title, "excerpt": cfg["excerpt"], "focus_keyword": cfg["focus_keyword"]})

    # アイキャッチ：写真生成→フック焼き込み→カバー設定
    bg = generate_image(BASE_STYLE + ", " + cfg["eyecatch_prompt"], os.path.join(D, f"{slug}_eyecatch.png"))
    composed = compose_eyecatch(bg_path=bg, main_html=cfg["eyecatch_main_html"],
                                subtitle_text=cfg["eyecatch_subtitle"],
                                out_path=os.path.join(D, f"{slug}_eyecatch_composed.png"),
                                main_size=cfg.get("eyecatch_main_size", 50))
    cov = c.upload_image_file(composed, f"{slug}_eyecatch_composed.png")
    assert cov, "cover upload failed"
    mp = {"draftPost": {"media": {"custom": True, "wixMedia": {"image": {
          "id": cov.get("id", ""), "url": cov["url"], "height": cov.get("height", 1024),
          "width": cov.get("width", 1536), "filename": f"{slug}_eyecatch_composed.png"}}, "displayed": True}},
          "fieldMask": "media"}
    rm = requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{did}", headers=c.wix_headers(), json=mp, timeout=30)
    print("cover:", rm.status_code)

    verify(did, cfg["cta_url"])
    print("DRAFT_ID =", did)
    print(f"https://manage.wix.com/dashboard/{c.WIX_SITE_ID}/blog/post/{did}")
    return did


CFG = {
    "draft_path": os.path.join(D, "joseimuke_omiai_jibun.md"),
    "slug": "2026-10-14_omiai_josei",
    "cta_url": "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-10-14-omiai-josei",
    "excerpt": ("お見合いで、聞かれたくない質問や興味の持てない話に、笑顔で合わせて疲れていませんか。"
                "お見合いは面接ではなく、二人でどんな時間をつくれるかを見る場です。"
                "公認心理師・仲人の中嶋美知が、やんわり伝える言い方と、相手を見極めるポイントをお伝えします。"),
    "focus_keyword": "お見合い 聞かれたくないこと 女性",
    "tag_ids": [
        "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
        "d372d6c7-06f8-47fe-a647-6229a0b94c80",  # お見合い
        "e00fdb14-3f82-4569-9c70-a7226cb7d058",  # 女性心理
        "1f43ee6a-bc46-4566-944a-b278f7e4d485",  # 心構え
        "15b9f04d-03e6-4649-a32b-dec43d522bee",  # コミュニケーション
        "61b87be5-2b10-4fa7-abb0-6cff0b363c4f",  # パートナーシップ
        "39e04614-4c13-4514-a633-8b8fad0b75df",  # 遠慮
        "d3951cb7-1ad4-406d-9d61-544c4e155c9d",  # 相手の見極め方
        "10dc8abd-4250-4356-a7ad-9f4465502257",  # 心理学
        "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    ],
    "related": [
        "2cf3dbc8-6b9d-471a-bc78-8fe3c75f4ff4",  # 「聞き上手」をやめたら、うまくいく。
        "6eb8b8e1-db3b-48d7-a8ad-f56b75ff51e5",  # お見合いで仕事の苦労話をされたとき、あなたはどう感じましたか？
        "490faf91-c89f-489e-82ef-3d757165afea",  # 笑顔が、婚活を変える。
    ],
    "eyecatch_prompt": ("beautiful Japanese woman in her 30s, elegant refined features, model-like appearance, "
        "an omiai meeting in a bright modern hotel lounge with large windows, a Japanese man in his 30s across the table, "
        ""
        + OMIAI_STYLE + "the woman smiling brightly and speaking with relaxed confidence, the man smiling, teacups on the table, wide shot"),
    "eyecatch_main_html": 'お見合いで、本当は<br><span class="accent">聞かれたくないこと</span>が<br>あるあなたへ。',
    "eyecatch_subtitle": "――実は、その時間のハンドルはあなたも握っていいんです",
    "eyecatch_main_size": 58,
    "body_images": [
        ("二人でどんな時間をつくれるかを見る時間なのだから、あなたが会話をリードしてもいいし、話の流れを別の方向に向けたっていいんです。",
         "beautiful Japanese woman in her 30s, elegant refined features, sitting in a bright hotel lounge, "
         "cheerfully telling a story with a light hand gesture, a Japanese man in his 30s sitting across from her "
         "listening with interest and smiling, "
        + OMIAI_STYLE + "seen from the side, coffee cups on the table"),
        ("お見合いの席での「ちょっとしたお願い」への反応は、実はその力を見る、とてもいい機会なんですよね。",
         "a kind-looking Japanese man in his 30s nodding and smiling warmly while listening, a beautiful Japanese woman "
         "across the table smiling with relief, "
        + OMIAI_STYLE + "bright hotel lounge, natural daylight"),
        ("それだけで、お見合いが「審査される場」から「二人で時間をつくる場」に変わっていきます。",
         "beautiful Japanese woman in her 30s, elegant refined features, laughing naturally and relaxed as if "
         "with a close friend, sitting at a bright cafe table by a window, holding a teacup, candid moment"),
    ],
}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        verify(sys.argv[2], CFG["cta_url"])  # 例: python3 post_omiai_josei_2026_10_14.py --verify <DRAFT_ID>
    else:
        run(CFG)
