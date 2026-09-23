"""
【女性向け】「あのカフェ、寄りたい」が言えなかった日。
【男性向け】計画どおりに進んでいるのに、なぜか胸のあたりがザワつく旅の途中。
カテゴリ: 仮交際
2026-09-21作成 → 2026-09-23投稿

2本共通のロジック。個別の起動は post_keikaku_josei_2026_09_23.py /
post_keikaku_dansei_2026_09_24.py から `run(config)` を呼ぶ。
"""
import os, sys, re, uuid, base64, requests
from openai import OpenAI

sys.path.insert(0, os.path.dirname(__file__))
from eyecatch_composer import compose_eyecatch

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
REAL_PHOTO_URL = "https://static.wixstatic.com/media/a4e52d_cf3f0f8fec8d40e4ac0e0bb6dfc4771d~mv2.png"

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_KEY)

CATEGORY_IDS = ["1ec5b4de-8edb-4c97-8199-2ef82776c050"]  # 仮交際
RELATED_POST_IDS = [
    "64073f78-40d4-4695-ad8c-053ae2ff910e",  # 向かい合って話すだけが、デートじゃない。仮交際中の「なんか疲れる」を…
    "78d9e1c5-9567-4c4c-a7d8-9b318a131ee9",  # 「どこ行こうか」から、ふたりは始まる。
    "e739167c-44b5-4cbb-b200-2225c919b409",  # 「かまってほしい」と「ひとりにして」は、どちらも愛の形。
]

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "drafts", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)


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


def heading(text):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": 2}}


def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {"lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"}}


def section_heading(text):
    return [sp(), divider_node(), sp(), heading(text)]


def link_node_centered(text, url, underline=False):
    decos = [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]
    if underline:
        decos.append({"type": "UNDERLINE"})
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": decos}}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}


def cta_nodes(cta_url):
    return [
        link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", cta_url),
        link_node_centered(cta_url, cta_url, underline=True),
    ]


def real_photo_node():
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {
                "image": {"src": {"url": REAL_PHOTO_URL}},
                "containerData": {"width": {"size": "SMALL"}, "alignment": "CENTER"},
            }}


def image_node(file_obj, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {
                "image": {"src": {"url": file_obj["url"]}}, "caption": caption,
                "containerData": {"width": {"size": "SMALL"}, "alignment": "CENTER"},
            }}


def build_nodes_from_draft(draft_path, cta_url):
    """.md下書きの「## 本文」〜「## 差し込み画像」直前を、richContentノード列に変換する。
    見出し(###)→section_heading、[ここに実写カウンセリング写真を挿入]→real_photo_node、
    CTAの2行ブロック→cta_nodes、それ以外の空行区切りブロック→1ブロック=1PARAGRAPHノード。
    """
    text = open(draft_path, encoding="utf-8").read()
    body = text.split("## 本文\n\n", 1)[1].split("\n\n---\n\n## 差し込み画像")[0]
    blocks = body.split("\n\n")
    nodes = []
    for i, block in enumerate(blocks):
        if i > 0:
            nodes.append(sp())
        if block.startswith("### "):
            nodes.extend(section_heading(block[4:].strip()))
        elif block.strip() == "[ここに実写カウンセリング写真を挿入]":
            nodes.append(real_photo_node())
        elif block.startswith("⬇️"):
            nodes.extend(cta_nodes(cta_url))
        else:
            nodes.append(p(block.strip()))
    return nodes


def find_index_after_text_contains(nodes, substr):
    for i, n in enumerate(nodes):
        if n.get("type") == "PARAGRAPH":
            for t in n.get("nodes", []):
                if substr in t.get("textData", {}).get("text", ""):
                    return i
    return -1


def generate_image(prompt, filename):
    print(f"[gpt-image-1] generating: {filename}")
    resp = client.images.generate(model="gpt-image-1", prompt=prompt, size="1536x1024", quality="high", n=1)
    img_data = resp.data[0]
    if not img_data.b64_json:
        raise RuntimeError("b64_json missing")
    img_bytes = base64.b64decode(img_data.b64_json)
    local_path = os.path.join(IMAGES_DIR, filename)
    with open(local_path, "wb") as f:
        f.write(img_bytes)
    print(f"  保存完了: {local_path}")
    return local_path


def upload_image_file(local_path, filename, mime="image/png"):
    with open(local_path, "rb") as f:
        image_bytes = f.read()
    r = requests.post(f"{WIX_BASE}/site-media/v1/files/generate-upload-url", headers=wix_headers(),
                       json={"mimeType": mime, "displayName": filename}, timeout=30)
    if not r.ok:
        print("  upload URL failed:", r.status_code, r.text[:200]); return None
    data = r.json()
    upload_url = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    sep = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": mime, "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print("  upload failed:", ru.status_code, ru.text[:200]); return None
    file_obj = ru.json().get("file", {})
    if not file_obj.get("url"):
        print("  URL missing:", ru.json()); return None
    print(f"  -> {file_obj['url'][:80]}...")
    return file_obj


def create_draft(cfg):
    nodes = build_nodes_from_draft(cfg["draft_path"], cfg["cta_url"])
    body = {
        "draftPost": {
            "title": cfg["title"],
            "richContent": {"nodes": nodes, "metadata": {"version": 1}},
            "categoryIds": CATEGORY_IDS,
            "tagIds": cfg["tag_ids"],
            "relatedPostIds": RELATED_POST_IDS,
            "excerpt": cfg["excerpt"],
            "memberId": MEMBER_ID,
        },
        "publish": False,
    }
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(), json=body, timeout=30)
    if not r.ok:
        print("下書き作成失敗:", r.status_code, r.text[:500]); return None
    draft = r.json()["draftPost"]
    print("下書き作成完了 ID:", draft["id"])
    return draft["id"]


def set_seo(draft_id, cfg):
    seo_patch = {
        "draftPost": {
            "seoData": {
                "tags": [
                    {"type": "title", "children": cfg["title"]},
                    {"type": "meta", "props": {"name": "description", "content": cfg["excerpt"]}},
                ],
                "settings": {"preventAutoRedirect": False, "keywords": [{"term": cfg["focus_keyword"], "isMain": True}]},
            }
        },
        "fieldMask": "seoData",
    }
    rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=seo_patch, timeout=30)
    print("SEOメタ更新:", "完了" if rp.ok else f"失敗 {rp.status_code} {rp.text[:300]}")


def add_images(draft_id, cfg):
    eyecatch_path = generate_image(cfg["eyecatch_prompt"], f"{cfg['slug']}_eyecatch.png")
    sec_path = generate_image(cfg["section_prompt"], f"{cfg['slug']}_section.png")
    hope_path = generate_image(cfg["hope_prompt"], f"{cfg['slug']}_hope.png")

    files = {
        "sec": upload_image_file(sec_path, f"{cfg['slug']}_section.png"),
        "hope": upload_image_file(hope_path, f"{cfg['slug']}_hope.png"),
    }
    if not all(files.values()):
        print("画像アップロードに失敗しました。"); return

    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    nodes = r.json()["draftPost"]["richContent"]["nodes"]

    insertions = []
    for substr, key, caption in cfg["insert_after"]:
        idx = find_index_after_text_contains(nodes, substr)
        if idx == -1:
            print("  挿入位置が見つかりません:", substr[:20]); continue
        insertions.append((idx, key, caption))
    insertions.sort(key=lambda x: x[0], reverse=True)
    for idx, key, caption in insertions:
        img = image_node(files[key], caption)
        nodes[idx + 1:idx + 1] = [sp(), img, sp()]

    patch_body = {"draftPost": {"richContent": {"nodes": nodes, "metadata": {"version": 1}}}, "fieldMask": "richContent"}
    rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=patch_body, timeout=30)
    print("本文への画像差し込み:", "完了" if rp.ok else f"失敗 {rp.status_code} {rp.text[:300]}")

    composed_path = os.path.join(IMAGES_DIR, f"{cfg['slug']}_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=eyecatch_path,
        main_html=cfg["eyecatch_main_html"],
        subtitle_text=cfg["eyecatch_subtitle"],
        out_path=composed_path,
        main_size=cfg.get("eyecatch_main_size", 50),
    )
    eyecatch_file = upload_image_file(composed_path, f"{cfg['slug']}_eyecatch_composed.png")
    if not eyecatch_file:
        print("アイキャッチのアップロードに失敗しました。"); return
    media_patch = {
        "draftPost": {"media": {"custom": True, "wixMedia": {"image": {
            "id": eyecatch_file.get("id", ""), "url": eyecatch_file["url"],
            "height": eyecatch_file.get("height", 1024), "width": eyecatch_file.get("width", 1536),
            "filename": eyecatch_file.get("displayName", "eyecatch.png"),
        }}, "displayed": True}},
        "fieldMask": "media",
    }
    rm = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=media_patch, timeout=30)
    print("カバー画像設定:", "完了" if rm.ok else f"失敗 {rm.status_code} {rm.text[:300]}")


def run(cfg):
    draft_id = create_draft(cfg)
    if not draft_id:
        return None
    set_seo(draft_id, cfg)
    add_images(draft_id, cfg)
    print("\nDRAFT_ID =", draft_id)
    print(f"編集URL: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog/post/{draft_id}")
    return draft_id
