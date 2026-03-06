#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3日に1回の自動実行用：stock.md の先頭トピックで記事下書きを生成し、
drafts/ に保存、used/log.md に記録、stock.md から該当行を削除する。
環境変数 OPENAI_API_KEY が必要です。
"""

import os
import re
from datetime import date
from pathlib import Path

# リポジトリルート（このスクリプトは scripts/ にある想定）
ROOT = Path(__file__).resolve().parent.parent


def load_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def get_first_topic(stock_content: str) -> tuple[str | None, str | None]:
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

上記トピックで、ブログ記事の本文だけを書いてください。
- 歴史・成婚退会の「数」は強調しない。一人ひとりに寄り添う・諦めないで柔軟に・サポートの中身で選ぶ、という良さが伝わるように。
- 顧客目線・失敗しうる点・会員の幸せな未来・心理学以外の観点も入れる。
- 見出しは ## で。最後に改行を1つ入れて終えてください。画像用プロンプトは不要です。
"""


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY が設定されていません。")
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
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        body = (resp.choices[0].message.content or "").strip()
    except Exception as e:
        print(f"OpenAI API エラー: {e}")
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

    print("完了しました。")


if __name__ == "__main__":
    main()
