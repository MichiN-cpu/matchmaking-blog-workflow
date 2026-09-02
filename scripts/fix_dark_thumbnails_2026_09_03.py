"""
サムネイル明るさ差し替え（引き継ぎメモ「次のチャット用メモ.md」対象10本のうち、
明らかに暗い・沈んだ印象と判断した7本を一括処理）。
2026-09-03

対象外（判断の結果、そのまま残す）：
- kugiri_danjo（fcbe0358）：日中の窓際、表情は思案顔だが背景明るく許容範囲
- omamori_items（3f93b867）：人物の暗い表情ではなく静物（PC・カップ）中心のため優先度低、今回は対象外
"""
import os, sys, base64, requests
from openai import OpenAI

sys.path.insert(0, os.path.dirname(__file__))
from eyecatch_composer import compose_eyecatch

WIX_API_KEY = os.environ["WIX_API_KEY"]
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE = "https://www.wixapis.com"
OPENAI_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_KEY)

def wix_headers():
    return {"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID, "Content-Type": "application/json"}

BASE_STYLE = (
    "Photorealistic, cinematic quality, natural soft daylight, East Asian appearance, "
    "beautiful Japanese woman, elegant refined features, model-like appearance, clear skin, "
    "real-world setting, professional lifestyle photography style, shallow depth of field, "
    "clean bright modern atmosphere, no text, no illustration style, no flat colors."
)

ITEMS = [
    {
        "key": "yokatta_wo_kazoeru",
        "draft_id": "6d3b8a82-26b8-4e51-ab0b-f039435bd343",
        "prompt": BASE_STYLE + (
            " A Japanese woman sitting on a light gray sofa in a bright living room during the day, "
            "large window with soft natural daylight, holding a small notebook and smiling gently and "
            "warmly while writing in it, content and peaceful expression, eyes soft with quiet happiness, "
            "neutral cream and soft gray tones, crisp clean colors, no text, no logos."
        ),
        "main_html": '婚活が続く人ほど、<br>実は<span class="accent">「小さなよかった」</span>を<br>数えている。',
        "subtitle_text": "――ドラマチックな出会いより、地味な習慣が結果を分ける話",
        "main_size": 46,
        "out_name": "2026-09-03_yokatta_wo_kazoeru_eyecatch_v2",
    },
    {
        "key": "app_tsukare_josei",
        "draft_id": "6f4cdc1e-0655-4256-97a4-d18f9f133aaa",
        "prompt": BASE_STYLE + (
            " A Japanese woman sitting at a bright cafe table near a window during the day, resting her "
            "chin gently on her hand, looking at her phone with a soft tired but calm expression, gentle "
            "exhale, NOT crying, NOT distressed, eyes calm and thoughtful, soft natural daylight, a faint "
            "gentle smile at the corner of her mouth, neutral pastel tones, crisp clean colors, no text, no logos."
        ),
        "main_html": 'その「もう疲れた」、<br><span class="accent">気のせいじゃありません</span>',
        "subtitle_text": "――マッチングアプリを頑張ってきた人にこそ伝えたいこと",
        "main_size": 62,
        "out_name": "2026-09-03_app_tsukare_josei_eyecatch_v2",
    },
    {
        "key": "isogashii_dansei",
        "draft_id": "66b9bbdf-99b5-4fc9-874f-0bdbe3d218f8",
        "prompt": BASE_STYLE + (
            " A Japanese businessman in a neat dark suit standing in a bright modern office corridor or "
            "sunny train platform during the day, checking his phone with a confident, energetic, genuine "
            "slight smile, purposeful and positive expression, bright natural daylight, clean modern "
            "architecture background, crisp clean colors, no text, no logos."
        ),
        "main_html": '忙しい人ほど、<br><span class="accent">婚活はうまくいく</span>。',
        "subtitle_text": "――「時間がない」を、始めない理由にしないための話",
        "main_size": 58,
        "out_name": "2026-09-03_isogashii_dansei_eyecatch_v2",
    },
    {
        "key": "hanbetsu_ryouiki",
        "draft_id": "43b84e67-a49e-4d1c-b95f-cb1fc436a16b",
        "prompt": BASE_STYLE + (
            " A Japanese woman standing at a fork in a path in a bright green park on a clear sunny day, "
            "blue sky with soft white clouds, looking forward with a calm, confident, thoughtful expression, "
            "a gentle determined half-smile, natural bright daylight, crisp clean colors, no text, no logos."
        ),
        "main_html": '婚活が長引く人と<br>早く決まる人、<span class="accent">「たった一つ」</span>の違い',
        "subtitle_text": "――同じ村を、何度も訪ねていませんか？",
        "main_size": 62,
        "out_name": "2026-09-03_hanbetsu_ryouiki_eyecatch_v2",
    },
    {
        "key": "anshin_josei",
        "draft_id": "77e61211-46b1-433b-951f-afd39bfd4168",
        "prompt": BASE_STYLE + (
            " A Japanese woman sitting by a bright window at home during the day, holding a warm cup of tea "
            "with both hands, looking outside with a calm, softly relieved expression, a gentle warm genuine "
            "smile, eyes peaceful and hopeful, natural daylight, soft neutral tones, crisp clean colors, "
            "no text, no logos."
        ),
        "main_html": 'その将来不安、<br><span class="accent">一人で抱えなくて</span><br>いいのかもしれません。',
        "subtitle_text": "――結婚で得られる「頼れる人がいる」という安心",
        "main_size": 50,
        "out_name": "2026-09-03_anshin_josei_eyecatch_v2",
    },
    {
        "key": "sabishisa_dansei",
        "draft_id": "3e9bd986-6d7e-4409-8657-b58387197ea4",
        "prompt": BASE_STYLE + (
            " A Japanese man in a casual shirt sitting at his kitchen table in the evening, in a well-lit "
            "modern apartment with warm ambient room lighting turned on so the whole room is evenly and "
            "comfortably bright (NOT dim, NOT shadowy, NOT pitch dark background), holding a drink can "
            "quietly, looking down in a calm, thoughtful, reflective expression, NOT distressed, NOT crying, "
            "a soft contemplative half-smile, evenly lit scene, clean modern interior, crisp balanced colors, "
            "no text, no logos."
        ),
        "main_html": '夜、なんとなく<br>手が伸びる<span class="accent">一杯</span>。',
        "subtitle_text": "――その正体、実は「寂しさ」かもしれません",
        "main_size": 58,
        "out_name": "2026-09-03_sabishisa_dansei_eyecatch_v2",
    },
    {
        "key": "anzen_shinrai",
        "draft_id": "c5b47c12-6ad3-4f05-9006-9f330c7ec906",
        "prompt": BASE_STYLE + (
            " A Japanese woman sitting at a bright kitchen table during the day, looking at her phone with a "
            "curious, discerning expression, slightly raised eyebrow, thoughtful and alert but calm, natural "
            "daylight from a nearby window, soft neutral tones, crisp clean colors, no text, no logos."
        ),
        "main_html": 'その「素敵な人」、<br><span class="accent">写真の通り</span>だと<br>思いますか？',
        "subtitle_text": "――婚活で、心と一緒に守ってほしいもの",
        "main_size": 52,
        "out_name": "2026-09-03_anzen_shinrai_eyecatch_v2",
    },
]


def upload_image_file(local_path, filename):
    with open(local_path, "rb") as f:
        image_bytes = f.read()
    r = requests.post(f"{WIX_BASE}/site-media/v1/files/generate-upload-url", headers=wix_headers(),
                       json={"mimeType": "image/png", "fileName": filename})
    if r.status_code != 200:
        print("  upload URL failed:", r.status_code, r.text[:300]); return None
    data = r.json()
    upload_url = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    sep = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": "image/png"}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if ru.status_code not in (200, 201):
        print("  upload failed:", ru.status_code, ru.text[:300]); return None
    return ru.json().get("file")


def patch_cover(draft_id, eyecatch_file, filename):
    media_patch = {
        "draftPost": {"media": {"custom": True, "wixMedia": {"image": {
            "id": eyecatch_file.get("id", ""), "url": eyecatch_file["url"],
            "height": eyecatch_file.get("height", 1024), "width": eyecatch_file.get("width", 1536),
            "filename": filename,
        }}, "displayed": True}},
        "fieldMask": "media",
    }
    rm = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=media_patch, timeout=30)
    return rm.ok, rm.status_code, rm.text[:300]


if __name__ == "__main__":
    results = []
    for item in ITEMS:
        print(f"\n=== {item['key']} ===")
        print("  [gpt-image-1] generating brighter photo...")
        resp = client.images.generate(model="gpt-image-1", prompt=item["prompt"], size="1536x1024", quality="high", n=1)
        raw_path = f"drafts/images/{item['out_name']}_raw.png"
        with open(raw_path, "wb") as f:
            f.write(base64.b64decode(resp.data[0].b64_json))
        print("  raw saved:", raw_path)

        composed_path = f"drafts/images/{item['out_name']}_composed.png"
        compose_eyecatch(
            bg_path=raw_path,
            main_html=item["main_html"],
            subtitle_text=item["subtitle_text"],
            out_path=composed_path,
            main_size=item["main_size"],
        )

        filename = f"{item['out_name']}_composed.png"
        eyecatch_file = upload_image_file(composed_path, filename)
        if not eyecatch_file:
            results.append((item["key"], "UPLOAD FAILED"))
            continue
        ok, status, text = patch_cover(item["draft_id"], eyecatch_file, filename)
        results.append((item["key"], "OK" if ok else f"PATCH FAILED {status} {text}"))
        print("  patch:", "OK" if ok else f"FAILED {status} {text}")

    print("\n=== SUMMARY ===")
    for key, status in results:
        print(f"  {key}: {status}")
