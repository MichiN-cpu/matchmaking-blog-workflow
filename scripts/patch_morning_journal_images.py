#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
モーニングジャーナル下書き（d5023baa）に画像・タグを追加
"""

import os, re, time, uuid, requests, base64

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
DRAFT_ID    = "d5023baa-851c-462d-aab9-46761ef0be0b"
IMG_DIR     = os.path.expanduser("~/matchmaking-blog-workflow/drafts/images")

def wix_h():
    return {"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID, "Content-Type": "application/json"}

def nid(): return str(uuid.uuid4())[:8]

def generate_image(prompt, filename):
    print(f"  生成中: {filename}")
    r = requests.post("https://api.openai.com/v1/images/generations",
                      headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
                      json={"model": "gpt-image-1", "prompt": prompt,
                            "size": "1536x1024", "quality": "medium", "n": 1},
                      timeout=120)
    if not r.ok:
        print(f"  生成失敗: {r.status_code} {r.text[:100]}")
        return None
    img_bytes = base64.b64decode(r.json()["data"][0]["b64_json"])
    path = os.path.join(IMG_DIR, filename)
    with open(path, 'wb') as f:
        f.write(img_bytes)
    return img_bytes

def upload_to_wix(img_bytes, filename):
    print(f"  Wixアップロード中: {filename}")
    # Get upload URL
    r = requests.post(f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
                      headers=wix_h(),
                      json={"mimeType": "image/png", "fileName": filename},
                      timeout=30)
    if not r.ok:
        print(f"  upload URL失敗: {r.status_code} {r.text[:100]}")
        return None

    data = r.json()
    upload_url = data.get("uploadUrl")
    if not upload_url:
        print(f"  uploadUrl not found: {data}")
        return None

    # PUT file
    put_r = requests.put(upload_url, data=img_bytes,
                         headers={"Content-Type": "image/png"}, timeout=60)
    if not put_r.ok:
        print(f"  PUT失敗: {put_r.status_code} {put_r.text[:100]}")
        return None

    put_data = put_r.json()
    file_id = (put_data.get("file") or {}).get("id") or put_data.get("fileId")
    if not file_id:
        print(f"  file_id not found: {str(put_data)[:150]}")
        return None

    for i in range(20):
        time.sleep(3)
        chk = requests.get(f"{WIX_BASE}/site-media/v1/files/{file_id}", headers=wix_h(), timeout=15)
        if chk.ok:
            fd = chk.json().get("file", {})
            if fd.get("state") in ("READY", "OK"):
                url = fd.get("url", "")
                m = re.search(r"/media/([^?#\s]+)", url)
                print(f"  完了: {url[:60]}...")
                return {"url": url, "id": m.group(1) if m else file_id,
                        "height": 1024, "width": 1536, "filename": filename}
            print(f"  待機... ({fd.get('state')}, {i+1}/20)")
    return None

def gen_and_upload(prompt, filename):
    img_bytes = generate_image(prompt, filename)
    if not img_bytes:
        return None
    return upload_to_wix(img_bytes, filename)

def img_node(fi, caption=""):
    url = fi["url"]
    m = re.search(r"/media/([^?#\s]+)", url)
    wix_uri = f"wix:image://v1/{m.group(1)}/img.png" if m else url
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": wix_uri}}, "caption": caption}}

def main():
    today = "2026-06-12"
    base = ("Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
            "real-world setting, professional lifestyle photography style, "
            "shallow depth of field, clean bright modern atmosphere, no text, no warm tones")

    prompts = [
        f"{base}. Sitting at a wooden desk near a large bright window in early morning, writing peacefully in an open notebook, serene focused expression, morning light.",
        f"{base}. Smiling gently while using a laptop in early morning at a bright desk, energized and happy morning expression.",
        "Photorealistic, cinematic quality, a cup of coffee and an open notebook with a pen on a white desk near a bright morning window, soft natural daylight, fresh and clean atmosphere, no people, no text, no warm tones.",
    ]

    # 1. Generate & upload images
    print("\n[1/3] 画像生成・アップロード...")
    img1 = gen_and_upload(prompts[0], f"{today}_morning_journal_eyecatch.png")
    img2 = gen_and_upload(prompts[1], f"{today}_morning_journal_img2.png")
    img3 = gen_and_upload(prompts[2], f"{today}_morning_journal_img3.png")

    # 2. Update cover image
    print("\n[2/3] カバー画像・タグ更新...")
    patch = {"draftPost": {}, "fieldMask": "tagIds"}
    patch["draftPost"]["tagIds"] = [
        "6e84b3d4-a336-4adc-94ff-7e326267a310",  # 朝活（新規）
        "b2bf9e74-a740-4f75-9377-189632b532b4",  # モーニングジャーナル（新規）
        "f1e8e385-794b-4f25-b981-d3e16f81b3bd",  # 婚活マインド
        "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
        "d5599216-6bdd-47df-9af3-07d1c15c1539",  # 願いを叶える
    ]

    if img1:
        m = re.search(r"/media/([^?#\s]+)", img1["url"])
        patch["draftPost"]["media"] = {"custom": True, "wixMedia": {"image": {
            "id": m.group(1) if m else img1["id"],
            "url": img1["url"], "height": 1024, "width": 1536, "filename": img1["filename"]
        }}}
        patch["fieldMask"] += ",media"

    r = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}",
                       headers=wix_h(), json=patch, timeout=30)
    print(f"  カバー・タグ更新: {'OK' if r.ok else r.text[:200]}")

    # 3. Patch body images into richContent if uploaded
    if img2 or img3:
        print("\n[3/3] 本文画像をrichContentに追加...")
        # Get current draft
        dr = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}", headers=wix_h(), timeout=15)
        if dr.ok:
            nodes = dr.json().get("draftPost", {}).get("richContent", {}).get("nodes", [])

            def sp():
                return {"type": "PARAGRAPH", "id": nid(), "nodes": [
                    {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}
                ], "paragraphData": {}}

            # Find heading "モーニングジャーナルって何？" and insert img2 after its section
            # Find heading "脳科学的に説明できること" and insert img3 after its section
            new_nodes = []
            for i, node in enumerate(nodes):
                new_nodes.append(node)
                if img2 and node.get("type") == "PARAGRAPH":
                    texts = "".join(t.get("textData", {}).get("text", "")
                                   for t in node.get("nodes", []))
                    if "なんでわざわざZoomで繋ぐの" in texts:
                        new_nodes.append(sp())
                        new_nodes.append(img_node(img2, "毎朝Zoomで繋がりながら、静かに書く時間"))
                        new_nodes.append(sp())
                        img2 = None
                if img3 and node.get("type") == "PARAGRAPH":
                    texts = "".join(t.get("textData", {}).get("text", "")
                                   for t in node.get("nodes", []))
                    if "行ってらっしゃい" in texts:
                        new_nodes.append(sp())
                        new_nodes.append(img_node(img3, "朝の静けさが、一日の土台をつくる"))
                        new_nodes.append(sp())
                        img3 = None

            pr = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}",
                                headers=wix_h(),
                                json={"draftPost": {"richContent": {"nodes": new_nodes}},
                                      "fieldMask": "richContent"},
                                timeout=30)
            print(f"  本文画像追加: {'OK' if pr.ok else pr.text[:200]}")

    print(f"\n✅ 完了！")
    print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")

if __name__ == "__main__":
    main()
