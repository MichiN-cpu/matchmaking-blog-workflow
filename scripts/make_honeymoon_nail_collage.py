"""新婚旅行ネイル インスタ用コラージュ（1080x1440, 3:4）
juncoさんのインスタ投稿画像とかぶらないよう、複数の写真を重ねて1枚にまとめる。
"""
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
import os

DL = os.path.expanduser("~/Downloads")
OUT_DIR = os.path.expanduser("~/Desktop/インスタ_新婚旅行ネイル")
SRC = {
    "hands": f"{DL}/900064253_1132473226185081_3538723008846478605_n.jpg",
    "flower": f"{DL}/896199392_1914303989557302_3043463994224112715_n.jpg",
    "thumb": f"{DL}/898460503_1445001044499517_6532007338709498133_n.jpg",
    "wagara": f"{DL}/896101472_2338090303606024_5908955877815721679_n.jpg",
    "twoshot": os.path.expanduser(
        "~/asunaru-shindan/campaign/nyukaikin-off-2026-09/assets/nail-collab/group-photo-michi-junko.jpg"),
}
W, H = 1080, 1440
BG = (250, 248, 245)
INK = (92, 74, 68)
ACCENT = (196, 92, 62)  # 鳥居の朱色をイメージ
MINCHO = "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"
SERIF = "/System/Library/Fonts/Supplemental/Didot.ttc"


def load(key):
    return ImageOps.exif_transpose(Image.open(SRC[key])).convert("RGB")


def crop_inner(im, frac=0.045, bottom=0.17):
    """juncoさんのポラロイド枠（白枠・ロゴ）を外して写真部分だけにする"""
    w, h = im.size
    return im.crop((int(w * frac), int(h * frac), int(w * (1 - frac)), int(h * (1 - bottom))))


def polaroid(photo, width, angle, pad=18, bottom_pad=18):
    r = width / photo.width
    photo = photo.resize((width, int(photo.height * r)), Image.LANCZOS)
    card = Image.new("RGB", (width + pad * 2, photo.height + pad + bottom_pad), "white")
    card.paste(photo, (pad, pad))
    card = card.convert("RGBA")
    # 影
    sh_pad = 30
    shadow = Image.new("RGBA", (card.width + sh_pad * 2, card.height + sh_pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle(
        (sh_pad, sh_pad + 6, sh_pad + card.width, sh_pad + card.height + 6), fill=(60, 40, 30, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    shadow.alpha_composite(card, (sh_pad, sh_pad))
    return shadow.rotate(angle, resample=Image.BICUBIC, expand=True)


def place(canvas, img, cx, cy):
    canvas.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))


canvas = Image.new("RGBA", (W, H), BG + (255,))
d = ImageDraw.Draw(canvas)

# タイトル
t1 = ImageFont.truetype(SERIF, 64)
t2 = ImageFont.truetype(MINCHO, 34, index=0)
title = "Honeymoon Nail"
tw = d.textlength(title, font=t1)
d.text(((W - tw) / 2, 58), title, font=t1, fill=INK)
sub = "新婚旅行に向けて、かわいくしてもらいました"
sw = d.textlength(sub, font=t2)
d.text(((W - sw) / 2, 150), sub, font=t2, fill=INK)
d.line(((W / 2 - 40, 210), (W / 2 + 40, 210)), fill=ACCENT, width=3)

# 写真（奥から順に）
place(canvas, polaroid(crop_inner(load("hands")), 560, 4), 345, 520)
place(canvas, polaroid(crop_inner(load("flower")), 430, -5), 785, 470)
wg = load("wagara"); w_, h_ = wg.size
wg = wg.crop((int(w_*0.07), int(h_*0.10), int(w_*0.72), int(h_*0.62)))  # 親指の和柄＋朱色のお花に寄せる
place(canvas, polaroid(wg, 420, 6), 800, 880)
place(canvas, polaroid(load("twoshot"), 600, -3), 380, 1080)

# フッター
f = ImageFont.truetype(MINCHO, 26, index=0)
foot = "nail by junco*"
fw = d.textlength(foot, font=f)
ImageDraw.Draw(canvas).text(((W - fw) / 2, H - 70), foot, font=f, fill=INK)

os.makedirs(OUT_DIR, exist_ok=True)
out = os.path.join(OUT_DIR, "インスタ_新婚旅行ネイル_コラージュ.png")
canvas.convert("RGB").save(out)
print(out)
