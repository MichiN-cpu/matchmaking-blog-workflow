#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
post_to_x.py

ブログ記事のURLとタイトルをX（Twitter）に投稿するスクリプト。

使い方:
    python scripts/post_to_x.py --url "https://..." --title "記事タイトル" --excerpt "記事の抜粋"

必要な環境変数:
    TWITTER_API_KEY
    TWITTER_API_SECRET
    TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_TOKEN_SECRET
"""

import os
import sys
import argparse
import requests
from requests_oauthlib import OAuth1

# ── 設定 ──────────────────────────────────────────────────────────────────────

TWITTER_API_KEY             = os.environ.get("TWITTER_API_KEY", "")
TWITTER_API_SECRET          = os.environ.get("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN        = os.environ.get("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")

TWITTER_POST_URL = "https://api.twitter.com/2/tweets"

# ── ツイート文生成 ──────────────────────────────────────────────────────────────

def build_tweet(title: str, url: str, excerpt: str = "") -> str:
    """ツイート文を生成する（140字以内に収める）"""
    hashtags = "#婚活 #結婚相談所 #あすなる愛媛"

    if excerpt:
        # 抜粋がある場合：タイトル＋抜粋（短縮）＋URL＋ハッシュタグ
        # URL は Twitter 側で自動的に23文字にカウントされる
        max_excerpt = 60
        short_excerpt = excerpt[:max_excerpt] + "…" if len(excerpt) > max_excerpt else excerpt
        tweet = f"【新着ブログ】{title}\n\n{short_excerpt}\n\n{url}\n\n{hashtags}"
    else:
        tweet = f"【新着ブログ】{title}\n\n{url}\n\n{hashtags}"

    return tweet


# ── 投稿 ───────────────────────────────────────────────────────────────────────

def post_tweet(text: str) -> dict:
    """Twitter API v2 でツイートを投稿する"""
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
        print("エラー: Twitter APIキーが設定されていません。")
        print("~/.zshrc に以下の環境変数を設定してください:")
        print("  TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET")
        sys.exit(1)

    auth = OAuth1(
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET,
    )

    payload = {"text": text}
    response = requests.post(TWITTER_POST_URL, json=payload, auth=auth)

    if response.status_code == 201:
        data = response.json()
        tweet_id = data["data"]["id"]
        print(f"✅ ツイート投稿成功！")
        print(f"   ツイートID: {tweet_id}")
        print(f"   URL: https://twitter.com/MichiNakashima/status/{tweet_id}")
        return data
    else:
        print(f"❌ 投稿失敗: {response.status_code}")
        print(response.text)
        sys.exit(1)


# ── メイン ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ブログ記事をX（Twitter）に投稿する")
    parser.add_argument("--url",     required=True,  help="ブログ記事のURL")
    parser.add_argument("--title",   required=True,  help="ブログ記事のタイトル")
    parser.add_argument("--excerpt", default="",     help="記事の抜粋（省略可）")
    parser.add_argument("--dry-run", action="store_true", help="投稿せずにツイート文だけ表示する")
    args = parser.parse_args()

    tweet_text = build_tweet(args.title, args.url, args.excerpt)

    print("─" * 50)
    print("【ツイート内容】")
    print(tweet_text)
    print(f"（{len(tweet_text)} 文字）")
    print("─" * 50)

    if args.dry_run:
        print("dry-run モード: 投稿はしません。")
        return

    confirm = input("この内容で投稿しますか？ [y/N]: ").strip().lower()
    if confirm != "y":
        print("キャンセルしました。")
        return

    post_tweet(tweet_text)


if __name__ == "__main__":
    main()
