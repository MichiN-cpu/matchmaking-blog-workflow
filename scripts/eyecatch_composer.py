"""
アイキャッチ画像に「タイトルのフック」を文字で焼き込むための共通コンポーザー。
2026-09-02: カバー画像バージョンアップ（文字なし写真 → 文字入りサムネ風）の一環で新設。

使い方（他のpost_*.pyスクリプトから呼び出す想定）:

    from eyecatch_composer import compose_eyecatch

    compose_eyecatch(
        bg_path="drafts/images/2026-09-01_hanbetsu_ryouiki_eyecatch.png",
        main_html='婚活が長引く人と<br>早く決まる人、<span class="accent">「たった一つ」</span>の違い',
        subtitle_text="――同じ村を、何度も訪ねていませんか？",
        out_path="drafts/images/2026-09-01_hanbetsu_ryouiki_eyecatch_composed.png",
    )

ルール（BLOG_POLICY_ASUNARU.md §5-8参照）:
- 対象タグ（男女共通／男性向け／女性向け）のバッジは画像には入れない（2026-09-02にみっちゃんの指示で廃止）
- メインの文字はタイトルの「フック部分」をそのまま使う（結論を明かさない）
- キーフレーズ（数字・「たった一つ」等の強調語）だけアクセントカラーにする
- サブタイトルは小さく、メインの下に一段
- 本文中の差し込み画像には文字を入れない（このコンポーザーはアイキャッチ専用）
"""
import os
import subprocess
import uuid

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: {width}px;
    height: {height}px;
    font-family: 'Hiragino Sans', 'Noto Sans JP', sans-serif;
    position: relative;
    overflow: hidden;
  }}
  .bg {{
    position: absolute;
    inset: 0;
    width: {width}px;
    height: {height}px;
    object-fit: cover;
  }}
  .shade {{
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(20,10,15,0.05) 0%, rgba(20,10,15,0.15) 40%, rgba(20,10,15,0.82) 78%, rgba(15,8,12,0.92) 100%);
  }}
  .textblock {{
    position: absolute;
    left: 56px;
    right: 56px;
    bottom: 64px;
  }}
  .line {{
    color: #ffffff;
    font-size: {main_size}px;
    font-weight: 800;
    line-height: 1.28;
    letter-spacing: 0.01em;
    text-shadow: 0 3px 14px rgba(0,0,0,0.5);
  }}
  .accent {{
    color: #f3caa8;
  }}
  .sub {{
    margin-top: 22px;
    color: rgba(255,255,255,0.88);
    font-size: {sub_size}px;
    font-weight: 500;
    letter-spacing: 0.03em;
  }}
</style>
</head>
<body>
  <img class="bg" src="{bg_path}">
  <div class="shade"></div>
  <div class="textblock">
    <div class="line">{main_html}</div>
    <div class="sub">{subtitle_text}</div>
  </div>
</body>
</html>
"""


def compose_eyecatch(bg_path, main_html, subtitle_text, out_path,
                      width=1536, height=1024, main_size=62, sub_size=28):
    bg_abs = os.path.abspath(bg_path)
    html = TEMPLATE.format(
        width=width, height=height, main_size=main_size, sub_size=sub_size,
        bg_path=bg_abs, main_html=main_html, subtitle_text=subtitle_text,
    )
    tmp_html = f"/tmp/eyecatch_{uuid.uuid4().hex[:8]}.html"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)

    out_abs = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)
    subprocess.run([
        CHROME_PATH, "--headless", "--disable-gpu", "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={out_abs}",
        f"file://{tmp_html}",
    ], check=True, capture_output=True)
    os.remove(tmp_html)
    print(f"  アイキャッチ文字入れ完了: {out_abs}")
    return out_abs


if __name__ == "__main__":
    # 動作確認用サンプル
    compose_eyecatch(
        bg_path="../michi-hq/docs/eyecatch_sample/before.png",
        main_html='婚活が長引く人と<br>早く決まる人、<span class="accent">「たった一つ」</span>の違い',
        subtitle_text="――同じ村を、何度も訪ねていませんか？",
        out_path="../michi-hq/docs/eyecatch_sample/after_via_script.png",
    )
