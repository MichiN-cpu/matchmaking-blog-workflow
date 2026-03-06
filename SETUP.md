# セットアップ：Claude Code と マルチAI（Gemini 等）でのブログ作成

## Claude Code for VS Code 拡張機能のインストール

Cursor ではターミナルから拡張をインストールするコマンドが標準では用意されていません。次のいずれかでインストールしてください。

### 方法A：拡張機能ビューから（推奨）

1. **拡張機能を開く**  
   `Cmd + Shift + X`（Mac） / `Ctrl + Shift + X`（Windows）
2. **検索**  
   検索欄に「**Claude Code**」と入力
3. **インストール**  
   「**Claude Code for VS Code**」（Anthropic 提供）を選んで「インストール」

### 方法B：コマンドパレットから

1. `Cmd + Shift + P`（Mac） / `Ctrl + Shift + P`（Windows）でコマンドパレットを開く
2. 「**Extensions: Install Extensions**」で拡張機能ビューを開く
3. 「Claude Code」で検索してインストール

### インストール後

- Anthropic アカウントでのサインインが必要な場合があります
- スパークアイコンやステータスバーの ✱ から Claude Code を起動できます
- 詳細: [Claude Code for VS Code - Marketplace](https://marketplace.visualstudio.com/items?itemName=Anthropic.claude-code)

---

## マルチAI運用（Claude Code → Gemini 等でブログ下書き完成まで）

Claude Code から **Gemini や他の AI** に指示を出して、ブログ記事下書きを完成させる流れです。

### 想定フロー

1. **トピック選択**  
   `topics/stock.md` から今日の1トピックを選ぶ（手動または AI に任せる）。
2. **Claude Code で指示**  
   「このトピックで結婚相談所ブログの下書きを書いて。`EDITORIAL_GUIDELINES.md` に沿って、顧客目線・失敗しうる点・心理学以外の観点も入れて。図解が必要なら構成案も出して」などと依頼。
3. **別AI（Gemini 等）に投げる場合**  
   Claude Code が生成した「指示文・アウトライン・チェックリスト」をコピーし、Gemini や他の AI に貼り付けて「この指示で記事本文を書いて」と依頼。必要なら図解の説明文も渡す。
4. **品質チェック**  
   戻ってきた案を、`EDITORIAL_GUIDELINES.md` の客観視・顧客目線・失敗点・現実性・多角的観点でチェック。Claude Code や Cursor に「この記事を EDITORIAL_GUIDELINES でレビューして」と依頼してもよい。
5. **あなたの確認**  
   内容を確認し、「OK」なら次へ、「ここを直して」と指示。
6. **下書き完成**  
   OK が出たら、Wix 用テキスト・GBP 用概略・図解メモ（必要なら画像生成）を `drafts/` に保存。`used/log.md` に使用トピックを記録。

### Claude Code に渡す指示文の例

```
matchmaking-blog-workflow の topics/stock.md の先頭トピックで、
結婚相談所ブログの記事下書きを書いて。

参照してほしいルール：
- EDITORIAL_GUIDELINES.md の全項目（客観視・顧客目線・失敗点・現実性・多角的観点）
- 心理学以外に、社会学・歴史・マーケ・結婚のライバル視点も入れる
- 図解が必要なテーマなら、図の構成案も出す

完成したら一度止まって、内容のOK/修正を確認させて。
```

### Gemini 等に渡すときの例

（Claude Code がアウトラインやチェックリストを出した場合）

```
以下のアウトラインと編集方針に沿って、結婚相談所のブログ記事本文を書いて。
【ここにアウトライン・キーワード・観点を貼り付け】
```

---

## 画像生成（アイキャッチ・図解）

- **画像は ChatGPT で作る**  
  ブログ用画像は **ChatGPT** に任せると仕上がりが良いため、画像生成は ChatGPT で行う。
- **流れ**  
  1. **Claude Code** に「この記事用のアイキャッチ（と図解）の画像生成用プロンプトを、ChatGPT にそのまま貼って使える形で書いて」と依頼。  
  2. 出てきたプロンプトを **ChatGPT** に貼り、「このプロンプトで画像を生成して」と依頼。  
  3. できた画像を `drafts/images/` に保存し、Wix にアップロードして使う。

---

## 図解が必要な記事のとき

- **図解の要不要**  
  `EDITORIAL_GUIDELINES.md` の「図解の要不要」を参照。流れ・比較・手順などは図解を検討。
- **保存場所**  
  図の構成案・説明文は `drafts/diagrams/` に保存。画像は `drafts/images/` に保存して Wix にアップロード。
- **AI への依頼例**  
  「この記事用に、[見学の流れ / 結婚相談所とアプリの比較 など] の図解構成案を出して。drafts/diagrams/ にメモを保存して。」

---

## まとめ

| やりたいこと           | 使うもの・場所 |
|------------------------|----------------|
| 拡張機能のインストール | Cursor の拡張機能ビューで「Claude Code」を検索 |
| 記事の種のストック     | `topics/stock.md` |
| 編集方針・品質チェック | `EDITORIAL_GUIDELINES.md` |
| 日次フロー             | `WORKFLOW.md` |
| 下書き・GBP・図解      | `drafts/` 配下 |
| 使用済みトピック       | `used/log.md` |

Claude Code で Gemini 等へ指示を回す場合は、**「EDITORIAL_GUIDELINES に沿った指示文・アウトラインを書く」**役を Claude Code に、「**その通りに記事本文を書く**」役を Gemini 等に振ると、ブログ維持と品質の両立がしやすくなります。**画像**は Claude Code がプロンプトを書き、**ChatGPT** にそのプロンプトを渡して生成すると仕上がりが良いです。
