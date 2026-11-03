"""
入会金11,000円OFFキャンペーン インスタ投稿用キャッチコピー画像を生成（4:5縦長 1080x1350）
2026-09-16
"""
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from eyecatch_composer import compose_eyecatch

ASSETS_DIR = os.path.expanduser("~/asunaru-shindan/campaign/nyukaikin-off-2026-09/assets")
OUT_DIR = os.path.join(ASSETS_DIR, "instagram")
os.makedirs(OUT_DIR, exist_ok=True)

HERO = os.path.join(ASSETS_DIR, "hero-couple.jpg")
MOMENT = os.path.join(ASSETS_DIR, "moment-photo.jpg")

posts = [
    dict(
        name="1_yokoku",
        bg=HERO,
        main_html='もうすぐ、<br>うれしい<span class="accent">お知らせ</span>',
        subtitle="9/19(土)〜",
        main_size=58,
    ),
    dict(
        name="2_kokuchi",
        bg=HERO,
        main_html='入会金<br><span class="accent">11,000円 OFF</span>',
        subtitle="9/19(土)〜10/18(日) 期間限定",
        main_size=66,
    ),
    dict(
        name="3_reminder",
        bg=MOMENT,
        main_html='あと少しで<br><span class="accent">終了</span>します',
        subtitle="入会金11,000円OFF ／ 10/18(日)まで",
        main_size=58,
    ),
    dict(
        name="4_lastcall",
        bg=HERO,
        main_html='<span class="accent">ラストチャンス</span><br>です',
        subtitle="入会金11,000円OFFキャンペーンは10/18(日)まで",
        main_size=58,
    ),
]

for post in posts:
    out_path = os.path.join(OUT_DIR, f"{post['name']}.png")
    compose_eyecatch(
        bg_path=post["bg"],
        main_html=post["main_html"],
        subtitle_text=post["subtitle"],
        out_path=out_path,
        width=1080,
        height=1350,
        main_size=post["main_size"],
        sub_size=32,
    )

print("完了:", OUT_DIR)
