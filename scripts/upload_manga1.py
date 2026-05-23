import os, requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"

IMAGES = [
    "/Users/nakashimamichi/Downloads/1_1.png",
    "/Users/nakashimamichi/Downloads/2_1.png",
    "/Users/nakashimamichi/Downloads/3_1.png",
    "/Users/nakashimamichi/Downloads/4_1.png",
]

def wix_headers():
    return {
        "Authorization": WIX_API_KEY,
        "wix-site-id":   WIX_SITE_ID,
        "Content-Type":  "application/json",
    }

def upload_image(local_path, display_name):
    # Step 1: アップロードURLを取得
    r = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "fileName": display_name},
        timeout=30,
    )
    if not r.ok:
        print(f"[ERROR] URLの取得失敗 {display_name}: {r.status_code} {r.text[:200]}")
        return None

    data = r.json()
    upload_url = data.get("uploadUrl")
    upload_token = data.get("uploadToken")
    if not upload_url:
        print(f"[ERROR] uploadUrlなし: {data}")
        return None

    # Step 2: ファイルをアップロード
    with open(local_path, "rb") as f:
        file_data = f.read()

    upload_headers = {"Content-Type": "image/png"}
    if upload_token:
        upload_headers["Authorization"] = upload_token

    r2 = requests.put(upload_url, headers=upload_headers, data=file_data, timeout=60)
    if not r2.ok:
        print(f"[ERROR] アップロード失敗 {display_name}: {r2.status_code} {r2.text[:200]}")
        return None

    # Step 3: レスポンスからURLを取得
    try:
        resp_data = r2.json()
        file_url = (resp_data.get("file") or {}).get("url") or resp_data.get("fileUrl")
        if file_url:
            print(f"[OK] {display_name}: {file_url}")
            return file_url
        else:
            print(f"[OK] アップロード完了（URLは後で確認）: {display_name}")
            print(f"     レスポンス: {resp_data}")
            return resp_data
    except Exception:
        print(f"[OK] アップロード完了: {display_name}")
        return True

def main():
    print("漫画#1 Wixアップロード開始\n")
    results = []
    for i, path in enumerate(IMAGES, 1):
        name = f"manga1_page{i}.png"
        print(f"アップロード中 ({i}/4): {name}")
        result = upload_image(path, name)
        results.append(result)
        print()

    print("=" * 50)
    print("完了！")
    for i, r in enumerate(results, 1):
        print(f"  ページ{i}: {r}")

if __name__ == "__main__":
    main()
