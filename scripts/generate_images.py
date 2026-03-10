#!/usr/bin/env python3
"""DALL-E 3で記事用画像を3枚生成するスクリプト"""

import os
import urllib.request
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

OUTPUT_DIR = "/home/user/matchmaking-blog-workflow/drafts/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

images = [
    {
        "filename": "01_app_stress.png",
        "prompt": (
            "A Japanese woman in her 30s sitting alone at a cafe, looking tired and overwhelmed, "
            "staring at her smartphone with many chat bubbles and notifications on screen. "
            "Soft watercolor illustration style, warm muted tones, no text in image."
        ),
        "label": "① アプリ疲れ（孤独なやりとり）",
    },
    {
        "filename": "02_counselor_consultation.png",
        "prompt": (
            "A warm and professional marriage counselor (Japanese woman, 40s) sitting across a table "
            "from a young woman client in a cozy private consultation room. They are having a heartfelt "
            "conversation with documents and tea on the table. Soft watercolor illustration style, "
            "warm peach and beige tones, no text in image."
        ),
        "label": "② 仲人との相談（安心感・信頼）",
    },
    {
        "filename": "03_couple_happy.png",
        "prompt": (
            "A happy Japanese couple in their 30s on a first date, sitting face-to-face at a bright "
            "cafe, smiling and talking naturally. The atmosphere feels genuine and warm, not staged. "
            "Soft watercolor illustration style, bright and hopeful colors, no text in image."
        ),
        "label": "③ お見合い（リアルな出会い）",
    },
]

for img in images:
    print(f"生成中: {img['label']} ...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=img["prompt"],
        size="1792x1024",
        quality="standard",
        n=1,
    )
    url = response.data[0].url
    out_path = os.path.join(OUTPUT_DIR, img["filename"])
    urllib.request.urlretrieve(url, out_path)
    print(f"  保存: {out_path}")

print("\n完了！3枚の画像を drafts/images/ に保存しました。")
