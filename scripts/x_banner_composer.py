"""
Xヘッダー画像（バナー）作成スクリプト。ロゴ＋実写写真を1500x500に合成する。
"""
from PIL import Image

LOGO_PATH = "/Users/nakashimamichi/Downloads/grow heart.png"
PHOTO_PATH = "/Users/nakashimamichi/matchmaking-blog-workflow/drafts/images/michi_real_photo.png"
OUT_PATH = "/Users/nakashimamichi/matchmaking-blog-workflow/drafts/images/2026-09-11_x_banner.png"

W, H = 1500, 500
SPLIT = 780  # 左：ロゴ側の幅

logo = Image.open(LOGO_PATH).convert("RGBA")
bg_color = logo.getpixel((5, 5))  # ロゴ背景色をサンプリングして地の色に使う

canvas = Image.new("RGB", (W, H), bg_color[:3])

# 右側：実写写真をSPLIT〜Wの幅・高さHにカバー方式でトリミングして配置
photo = Image.open(PHOTO_PATH).convert("RGB")
right_w = W - SPLIT
pw, ph = photo.size
scale = max(right_w / pw, H / ph)
new_w, new_h = int(pw * scale), int(ph * scale)
photo_resized = photo.resize((new_w, new_h), Image.LANCZOS)
# 中央基準でクロップ
left = (new_w - right_w) // 2
top = (new_h - H) // 2
photo_cropped = photo_resized.crop((left, top, left + right_w, top + H))
canvas.paste(photo_cropped, (SPLIT, 0))

# 左側：ロゴを中央に配置（縦幅の70%程度にリサイズ）
logo_h = int(H * 0.78)
logo_w = int(logo.width * (logo_h / logo.height))
logo_resized = logo.resize((logo_w, logo_h), Image.LANCZOS)
logo_x = (SPLIT - logo_w) // 2
logo_y = (H - logo_h) // 2
canvas.paste(logo_resized, (logo_x, logo_y), logo_resized)

canvas.save(OUT_PATH)
print(f"saved: {OUT_PATH} size={canvas.size} bg_color_sampled={bg_color}")
