#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3日に1回の自動実行用：手動の流れ（Claude Code で書く）を自動化する。
stock.md の先頭トピックで記事下書きを生成し、drafts/ に保存、used/log と stock を更新する。
環境変数: ANTHROPIC_API_KEY があれば Claude（Claude Code と同じ）で書く。なければ OPENAI_API_KEY で OpenAI を使用。
"""

import os
import re
import requests
from datetime import date
from pathlib import Path
from typing import Optional, Tuple

# リポジトリルート（このスクリプトは scripts/ にある想定）
ROOT = Path(__file__).resolve().parent.parent


def load_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def get_first_topic(stock_content: str) -> Tuple[Optional[str], Optional[str]]:
    """stock.md の内容から先頭1トピックを取得。('見出し用タイトル', '元の1行') または (None, None)。"""
    parts = stock_content.split("---", 1)
    if len(parts) < 2:
        return None, None
    lines = [s.strip() for s in parts[1].strip().split("\n")]
    for line in lines:
        if not line or line.startswith("#"):
            continue
        if line.startswith("- "):
            title = line[2:].strip()
            return title, line
        if "【" in line:
            return line.strip(), line
    return None, None


def remove_topic_from_stock(stock_content: str, exact_line: str) -> str:
    """stock.md の内容から、指定した1行（とその直後のサブ行があれば）を削除。"""
    lines = stock_content.split("\n")
    new_lines = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == exact_line.strip():
            i += 1
            # 次の行が全角スペース始まりの補足なら一緒に削除
            if i < len(lines) and lines[i].startswith("　"):
                i += 1
            continue
        new_lines.append(lines[i])
        i += 1
    return "\n".join(new_lines)


def sanitize_filename(title: str) -> str:
    """ファイル名に使えない文字をアンダースコアに。"""
    return re.sub(r'[\\/:*?"<>|\s]+', "_", title).strip("_") or "draft"


def build_prompt(topic: str, guidelines: str, brief: str) -> str:
    return f"""以下は「あすなる愛媛」の結婚相談所ブログ用の編集方針とブリーフです。この2つに厳密に沿って、指定トピックで記事下書きを1本書いてください。

【編集方針】
{guidelines}

【あすなる愛媛用ブリーフ】
{brief}

【依頼】
トピック：「{topic}」

上記トピックで、**「あすなる愛媛」のブログ**として記事の本文を書いてください。

■ あすなる愛媛らしさ（必須）
- **一般的な結婚相談所の説明にならないように。** 読んだ人が「この相談所なら話を聞いてみたい」と感じる、具体的で温かみのあるトーンで書く。
- 記事の随所に、次の視点を自然に織り込む：少人数で一人ひとりに寄り添う／諦めないで柔軟に進められる／サポートの中身・相性で選ぶ／愛媛で婚活する人を応援／その人らしいペースで、安心して話せる場。
- 冒頭や締めで「愛媛で」「少人数で」「寄り添う」などを、押しつけにならない形で入れる。抽象的な「結婚相談所は」だけで終わらせない。
- **避けること**：どの相談所のブログかわからないような一般的な説明、ぼんやりとした表現。あすなる愛媛ならではの視点（寄り添い・柔軟・愛媛・安心して話せる）が伝わるように書く。
- 歴史・成婚退会の「数」は強調しない。

■ その他
- 顧客目線・失敗しうる点・会員の幸せな未来・心理学以外の観点も入れる。
- 見出しは ## で。最後に改行を1つ入れて終えてください。画像用プロンプトは不要です。
"""


def generate_with_claude(prompt: str, api_key: str) -> str:
    """Claude（Claude Code と同じ）で記事本文を生成。"""
    from anthropic import Anthropic
    client = Anthropic(api_key=api_key)
    resp = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    if not resp.content or not resp.content[0].text:
        return ""
    return resp.content[0].text.strip()


def generate_with_openai(prompt: str, api_key: str) -> str:
    """OpenAI で記事本文を生成（ANTHROPIC が未設定時のフォールバック）。"""
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return (resp.choices[0].message.content or "").strip()


def build_image_prompt_request(topic: str, body: str) -> str:
    return f"""以下の結婚相談所ブログ記事に合う画像プロンプトを3点、英語で作成してください。

【トピック】{topic}

【記事本文（冒頭）】
{body[:800]}

以下の形式で出力してください（余計な説明は不要）：

IMAGE1: <英語プロンプト>
IMAGE2: <英語プロンプト>
IMAGE3: <英語プロンプト>

ルール：
- flat illustration style, no text, soft warm tones, Japanese characters and setting
- 必ず `no text` を含める
- 人物が出る場合は `East Asian appearance, black hair` を含める
- 写真ではなくイラスト調にする
"""


def parse_image_prompts(text: str) -> list:
    prompts = []
    for m in re.finditer(r'IMAGE\d:\s*(.+)', text):
        prompts.append(m.group(1).strip())
    return prompts


def generate_image_prompts(topic: str, body: str, anthropic_key: str = None, openai_key: str = None) -> list:
    prompt = build_image_prompt_request(topic, body)
    try:
        if anthropic_key:
            from anthropic import Anthropic
            client = Anthropic(api_key=anthropic_key)
            resp = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.content[0].text.strip()
        else:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            text = (resp.choices[0].message.content or "").strip()
        return parse_image_prompts(text)
    except Exception as e:
        print(f"画像プロンプト生成エラー: {e}")
        return []


def generate_images_dalle(prompts: list, draft_path: Path, openai_key: str) -> None:
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
    images_dir = draft_path.parent / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    date_str = re.search(r'\d{4}-\d{2}-\d{2}', draft_path.name)
    date_str = date_str.group(0) if date_str else date.today().strftime("%Y-%m-%d")

    for idx, prompt_text in enumerate(prompts, 1):
        label = "eyecatch" if idx == 1 else f"img{idx}"
        out_path = images_dir / f"{date_str}_{label}.png"
        print(f"  [{idx}/{len(prompts)}] DALL-E 3 生成中...")
        try:
            resp = client.images.generate(
                model="dall-e-3",
                prompt=prompt_text,
                size="1792x1024",
                quality="standard",
                n=1,
            )
            img_url = resp.data[0].url
            img_data = requests.get(img_url, timeout=60).content
            out_path.write_bytes(img_data)
            print(f"       保存: {out_path.name}")
        except Exception as e:
            print(f"       画像生成エラー（{label}）: {e}")


def main() -> None:
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not anthropic_key and not openai_key:
        print("ANTHROPIC_API_KEY または OPENAI_API_KEY のどちらかを設定してください。手動の流れに合わせるなら ANTHROPIC_API_KEY（Claude）を推奨します。")
        exit(1)

    stock_path = ROOT / "topics" / "stock.md"
    guidelines_path = ROOT / "EDITORIAL_GUIDELINES.md"
    brief_path = ROOT / "ASUNARU_EHIME_BRIEF.md"
    log_path = ROOT / "used" / "log.md"

    stock_content = load_text(stock_path)
    topic_title, exact_line = get_first_topic(stock_content)
    if not topic_title or not exact_line:
        print("トピックが1件も見つかりません。stock.md を確認してください。")
        exit(0)

    guidelines = load_text(guidelines_path)
    brief = load_text(brief_path)
    prompt = build_prompt(topic_title, guidelines, brief)

    try:
        if anthropic_key:
            print("Claude（手動の Claude Code と同じ）で記事を生成しています...")
            body = generate_with_claude(prompt, anthropic_key)
        else:
            print("OpenAI で記事を生成しています...")
            body = generate_with_openai(prompt, openai_key)
    except Exception as e:
        print(f"API エラー: {e}")
        exit(1)

    if not body:
        print("記事本文が空でした。")
        exit(1)

    today = date.today().strftime("%Y-%m-%d")
    safe_title = sanitize_filename(topic_title)[:50]
    draft_path = ROOT / "drafts" / f"draft_{today}_{safe_title}.md"
    save_text(draft_path, body)
    print(f"下書きを保存しました: {draft_path}")

    # used/log.md に追記
    log_content = load_text(log_path)
    new_row = f"| {today} | {topic_title} |"
    lines = log_content.split("\n")
    if "（未使用）" in log_content:
        # 「（未使用）」の行を今回の行に置き換え
        lines = [new_row if "（未使用）" in line else line for line in lines]
    else:
        # 表の区切り行の直後に挿入
        for i, line in enumerate(lines):
            if "|----" in line or "|----------" in line:
                lines.insert(i + 1, new_row)
                break
        else:
            lines.append(new_row)
    save_text(log_path, "\n".join(lines))
    print(f"used/log.md に記録しました: {topic_title}")

    # stock.md から該当トピックを削除
    new_stock = remove_topic_from_stock(stock_content, exact_line)
    save_text(stock_path, new_stock)
    print("topics/stock.md から該当トピックを削除しました。")

    # 画像生成（OPENAI_API_KEY がある場合のみ）
    if openai_key:
        print("\n画像プロンプトを生成しています...")
        image_prompts = generate_image_prompts(topic_title, body, anthropic_key, openai_key)
        if image_prompts:
            print(f"画像プロンプト {len(image_prompts)} 件生成完了。DALL-E 3 で画像を生成しています...")
            generate_images_dalle(image_prompts, draft_path, openai_key)
        else:
            print("画像プロンプトの生成に失敗しました。スキップします。")
    else:
        print("OPENAI_API_KEY が未設定のため画像生成をスキップします。")

    print("\n完了しました。")


if __name__ == "__main__":
    main()
