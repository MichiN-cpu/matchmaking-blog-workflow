"""
「この人で本当にいいのかな」——真剣交際に進むときに、その不安が生まれたあなたへ
画像生成・アップロード・richContentへの差し込み
2026-08-06
"""
import os, uuid, base64, requests
from openai import OpenAI

OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
DRAFT_ID    = "35d610c7-50ee-45ad-8d0a-310b7893b9b6"

client = OpenAI(api_key=OPENAI_KEY)

IMAGE_PROMPTS = [
    {
        "name": "eyecatch",
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, "
            "beautiful Japanese woman in her 30s, elegant refined features, model-like appearance, clear skin, "
            "real-world setting, professional lifestyle photography style, shallow depth of field, "
            "clean bright modern atmosphere, no text, no warm yellowish tint. "
            "She sits quietly, gentle contemplative expression looking slightly downward, soft natural window light."
        ),
        "caption": "小さな揺れも、大きな揺れも、あって当然です",
        "filename": "2026-08-06_marriage_blue_josei_eyecatch.png",
    },
    {
        "name": "notebook",
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, close-up of a woman's hands "
            "writing in a small notebook, soft natural daylight, clean bright modern atmosphere, "
            "no text, no warm yellowish tint."
        ),
        "caption": "不安を書き出してみると、輪郭が見えてくる",
        "filename": "2026-08-06_marriage_blue_josei_notebook.png",
    },
    {
        "name": "couple",
        "prompt": (
            "Photorealistic, cinematic quality, natural soft lighting, East Asian appearance, black hair, "
            "a Japanese couple in their 30s sitting close together on a sofa, having a warm honest "
            "conversation, gentle genuine expressions, real-world setting, professional lifestyle "
            "photography style, shallow depth of field, clean bright modern living room, no text, "
            "no warm yellowish tint."
        ),
        "caption": "不安を分かち合うことが、夫婦のスタートかもしれません",
        "filename": "2026-08-06_marriage_blue_josei_couple.png",
    },
]

def wix_headers():
    return {"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID, "Content-Type": "application/json"}

def nid():
    return str(uuid.uuid4())[:8]

def upload_image_binary(image_bytes, filename):
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "displayName": filename},
        timeout=30,
    )
    if not r.ok:
        print(f"  upload URL failed: {r.status_code} {r.text[:200]}")
        return None
    data = r.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    if not upload_url:
        print(f"  uploadUrl missing: {data}")
        return None
    sep  = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print(f"  upload failed: {ru.status_code} {ru.text[:200]}")
        return None
    file_obj = ru.json().get("file", {})
    if not file_obj.get("url"):
        print(f"  URL missing: {ru.json()}")
        return None
    print(f"  -> {file_obj['url'][:80]}...")
    return file_obj

def generate_and_upload_image(prompt, filename):
    print(f"\n[gpt-image-1] generating: {filename}")
    resp = client.images.generate(model="gpt-image-1", prompt=prompt, size="1536x1024", quality="high", n=1)
    img_data = resp.data[0]
    if not img_data.b64_json:
        print("  b64_json missing")
        return None
    img_bytes = base64.b64decode(img_data.b64_json)
    save_path = os.path.join(os.path.dirname(__file__), f"../drafts/images/{filename}")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(img_bytes)
    print("  done. uploading to Wix...")
    return upload_image_binary(img_bytes, filename)

def image_node(file_obj, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": file_obj["url"]}}, "caption": caption}}

def get_current_nodes():
    r = requests.get(f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}?fieldsets=CONTENT", headers=wix_headers(), timeout=30)
    r.raise_for_status()
    return r.json()["draftPost"]["richContent"]["nodes"]

def find_index_after_text_contains(nodes, substr):
    for i, n in enumerate(nodes):
        if n.get("type") == "PARAGRAPH":
            for t in n.get("nodes", []):
                text = t.get("textData", {}).get("text", "")
                if substr in text:
                    return i
    return -1

def sp():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}
    ], "paragraphData": {}}

def main():
    files = {}
    for img in IMAGE_PROMPTS:
        f = generate_and_upload_image(img["prompt"], img["filename"])
        files[img["name"]] = {"file": f, "caption": img["caption"]}

    if not all(v["file"] for v in files.values()):
        print("\n一部の画像アップロードに失敗しました。処理を中断します。")
        return

    nodes = get_current_nodes()

    insert_after = [
        ("先方のご親族に受け入れてもらえるだろうか。ご家庭の文化が大きく違うんじゃないか。そんなことがすごく大きく、大層なことのように見えてくる。慣れるまでは未知の世界なので、そう思うのも当然です。", "eyecatch"),
        ("不安というのは、不確かさから生まれるものです。相手任せ、状況任せにしていると、不確かさはいつまでも減らないので、不安も怖さも、そのまま続いてしまいます。", "notebook"),
        ("一人で不安を抱え込まないでください。仲人にも相談してください。先に結婚した友人や、ご両親も、結婚の先輩です。話を聞いてみてください。そしてもちろん、公認心理師の私にも、いつでも相談してください。", "couple"),
    ]

    insertions = []
    for substr, key in insert_after:
        idx = find_index_after_text_contains(nodes, substr)
        if idx == -1:
            print(f"  挿入位置が見つかりません: {substr[:20]}...")
            continue
        insertions.append((idx, key))
    insertions.sort(key=lambda x: x[0], reverse=True)

    for idx, key in insertions:
        info = files[key]
        img_node = image_node(info["file"], info["caption"])
        nodes[idx+1:idx+1] = [sp(), img_node, sp()]

    patch_body = {
        "draftPost": {"richContent": {"nodes": nodes, "metadata": {"version": 1}}},
        "fieldMask": "richContent",
    }
    r = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}", headers=wix_headers(), json=patch_body, timeout=30)
    print("本文への画像差し込み:", "完了" if r.ok else f"失敗 {r.status_code} {r.text[:300]}")

    eyecatch_file = files["eyecatch"]["file"]
    media_patch = {
        "draftPost": {
            "media": {
                "custom": True,
                "wixMedia": {
                    "image": {
                        "id": eyecatch_file.get("id", ""),
                        "url": eyecatch_file["url"],
                        "height": eyecatch_file.get("height", 1024),
                        "width": eyecatch_file.get("width", 1536),
                        "filename": eyecatch_file.get("displayName", "eyecatch.png"),
                    }
                },
                "displayed": True,
            }
        },
        "fieldMask": "media",
    }
    rm = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{DRAFT_ID}", headers=wix_headers(), json=media_patch, timeout=30)
    print("カバー画像設定:", "完了" if rm.ok else f"失敗 {rm.status_code} {rm.text[:300]}")

if __name__ == "__main__":
    main()
