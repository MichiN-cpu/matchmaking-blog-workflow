# 日次ブログ作成ワークフロー（Cursor / Claude Code での進め方）

Claude Code で Gemini 等へ指示を回す場合は `SETUP.md` を参照。

**記事を書くとき・直すときは、次の4つを参照する：**
- **`BLOG_POLICY_ASUNARU.md`**（詳細な執筆方針）
- **`ASUNARU_EHIME_BRIEF.md`**（ブランド概要）
- **`EDITORIAL_GUIDELINES.md`**（品質チェック）
- **`次のチャット用メモ.md`**（matchmaking-blog-workflow 内。チャット引き継ぎ用のメモ）

---

## 記事の下書きを用意する2つのやり方

| やり方 | 誰が・何が書くか | 詳しい手順 |
|--------|------------------|-------------|
| **手動** | **Claude Code**（あなたが依頼文を渡す） | この WORKFLOW.md の「流れの全体像」〜ステップ3まで。あなたがチェック → OK なら画像生成・Wix 投稿。 |
| **自動（3日に1回）** | **手動の流れを自動化**。記事を書くのは **Claude**（Claude Code と同じ。API で呼び出し）。あなたの代わりに「stock の先頭トピックで1本つくる → drafts/ に保存・log と stock を更新」まで実行。 | **`SETUP_AUTOMATION.md`** に手順あり。GitHub Secrets に **ANTHROPIC_API_KEY** を登録すると Claude で書く。未設定なら **OPENAI_API_KEY** で OpenAI を使用。 |

※ 自動実行 = **手動でやっている「Claude Code で記事を書く」部分を、同じ Claude で自動で回している**イメージです。できあがった下書きは drafts/ に入るので、あとは手動と同じくあなたがチェック → OK なら画像生成・Wix 投稿です。

---

## 流れの全体像：Claude Code で書く → チェック → OK なら画像 → Wix 投稿

```
1. Claude Code で記事を書いてもらう
   （トピックは topics/stock.md の上から1つ。下の「Claude Code 用 依頼文」をコピペして渡す）

2. あなたがチェック
   → 内容を読んで「OK」か「ここを直して」を伝える。直しがあれば Claude Code に差し戻し。

3. OK が出たら
   ├─ 画像：Claude Code が書いた「画像用プロンプト」を ChatGPT に渡して画像を生成 → drafts/images/ に保存
   ├─ Cursor：記事本文を drafts/ に保存、used/log に記録、stock から削除、GBP 用テキスト作成
   └─ あなた：drafts/ の本文と drafts/images/ の画像を Wix に投稿（コピペ・アップロード）
```

※ 任意で、Claude Code が書いた記事を **Cursor で EDITORIAL_GUIDELINES と ASUNARU_EHIME_BRIEF に沿ってチェック**し、修正点を Claude Code に差し戻すと、より安心です。

---

## Cursor と Claude Code・ChatGPT の役割分担（手間なく書く）

**Claude Code も同じリポジトリ（matchmaking-blog-workflow）を開いて使えます。** フォルダを共有しているので、どれで作業しても同じ `topics/stock.md` や `drafts/` を参照・更新できます。

| 役割 | 向いているツール | やること |
|------|------------------|----------|
| **記事の本文を書く** | **Claude Code / ChatGPT** | これまでブログを書いてもらっていたので、文体・トーン・知見が活きる。トピックと依頼文を渡せばそのまま下書きを出してもらえる。 |
| **画像用プロンプトを書く** | **Claude Code** | 記事に合うアイキャッチ・図解の「画像生成用プロンプト」を書く。そのプロンプトを ChatGPT に渡して画像を作る（画像は ChatGPT の方が仕上がりが良いため）。 |
| **品質チェック・修正の差し戻し** | **Cursor** | Claude Code が書いてきた記事を `EDITORIAL_GUIDELINES.md` と `ASUNARU_EHIME_BRIEF.md` でチェック。修正点があれば箇条書きでまとめ、その内容を Claude Code に渡して修正してもらう。 |
| **トピック選び・ファイル操作・log/stock 更新** | **Cursor** | `stock.md` から使用トピックを決める、`drafts/` へ保存、`used/log.md` に記録、`stock.md` から削除など。 |

**重要**：Cursor に納めてある `EDITORIAL_GUIDELINES.md` と `ASUNARU_EHIME_BRIEF.md` が品質の基準です。Claude Code が書いた記事も、この2つに照らして Cursor でチェックし、必要なら修正点を Claude Code に差し戻すと安心です。

**手間なくやるおすすめの流れ**

1. **Claude Code（または ChatGPT）で記事を書いてもらう**  
   → 下の「Claude Code 用 依頼文」をコピーし、`【トピック】` のところに今日使うトピック（`topics/stock.md` の上から1つ）を入れて Claude Code に貼る。出てきた本文を確認する。
2. **（任意）Cursor でチェック → 修正点を Claude Code に差し戻し**  
   → Claude Code が書いた記事本文を Cursor に貼り、「EDITORIAL_GUIDELINES と ASUNARU_EHIME_BRIEF でチェックして。修正点があれば箇条書きで出して」と依頼。出てきた修正点をそのまま Claude Code に渡し、「この修正点で直して」と依頼すると、Claude Code が修正してくれる。
3. **画像は Claude Code がプロンプトを書く → ChatGPT で画像生成**  
   → Claude Code に「この記事用のアイキャッチ（と図解）の画像生成プロンプトを書いて。そのプロンプトを ChatGPT に渡して画像を作る想定」と依頼。出てきたプロンプトを ChatGPT に貼り、「このプロンプトで画像を生成して」と依頼。できた画像を `drafts/images/` に保存。
4. **Cursor に仕上げを依頼する**  
   → 「この記事の本文を drafts に保存して、used/log に記録、stock からこのトピックを削除して。Wix・GBP 用テキストも作って」と依頼。Cursor がファイル操作・GBP 用短文を対応。

記事執筆は「知っている」Claude Code / ChatGPT に任せ、画像は **Claude Code がプロンプトを書き → ChatGPT で画像生成**、保存・log 更新は Cursor に任せると、ブログ記事を手間なく仕上げられます。

---

## 毎日の流れ

### ステップ1: 今日のブログを書いてもらう
Cursor または Claude Code のチャットで次のように依頼する：

```
matchmaking-blog-workflow の topics/stock.md からまだ使っていないトピックを1つ選んで、
結婚相談所のブログ記事の下書きを書いて。
EDITORIAL_GUIDELINES.md と ASUNARU_EHIME_BRIEF.md に沿って（あすなる愛媛の良さが伝わり、歴史・成婚実績の数は強調しない）、
顧客目線・失敗しうる点・会員の幸せな未来に繋がるか・心理学以外の観点も入れて。
図解が必要なテーマなら図の構成案も出して。内容を出したら一度止まって、OKかどうか確認させて。
```

→ AI がトピックを選び、記事本文（＋必要なら図解構成案）を出力する。**ここで内容を確認し、「OK」または修正指示を伝える。**

**Claude Code で書くとき用（コピペで使える依頼文）**  
`topics/stock.md` の上から使うトピックを1つ決め、下の【トピック】を差し替えてから Claude Code に貼る。Claude Code がこのリポジトリを開いていれば、`EDITORIAL_GUIDELINES.md` と `ASUNARU_EHIME_BRIEF.md` を参照できる。

```
【トピック】初めての結婚相談所の選び方

このトピックで、あすなる愛媛の結婚相談所ブログの記事下書きを書いて。
このリポジトリの EDITORIAL_GUIDELINES.md と ASUNARU_EHIME_BRIEF.md を読んでから書いて（歴史・成婚実績の数は強調しない。一人ひとりに寄り添う・諦めないで柔軟に・サポートの中身で選ぶ、という良さが伝わるように）。
顧客目線・失敗しうる点・会員の幸せな未来に繋がるか・心理学以外の観点も入れて。図解が必要なテーマなら図の構成案も出して。
あと、この記事用のアイキャッチ画像（と図解が必要なら図解画像）の「画像生成用プロンプト」も書いて。そのプロンプトはあとで ChatGPT に渡して画像を作る想定なので、ChatGPT にそのまま貼り付けて使える形で出して。内容を出したら一度止まって、OKかどうか確認させて。
```

※ トピックだけ差し替えればよい（例：`【トピック】見学・無料相談の流れと準備`）。

---

### ステップ1.5（任意）: Cursor で品質チェック → Claude Code に差し戻し
**Claude Code が書いた記事**を Cursor に貼り付けて、次のように依頼する：

```
この記事を EDITORIAL_GUIDELINES.md と ASUNARU_EHIME_BRIEF.md の全項目でチェックして。
客観視・顧客目線・失敗しうる点・現実性・多角的観点・あすなる愛媛の良さ（歴史・成婚数は強調しない）に沿っているか。不足や修正点があれば箇条書きで指摘と修正案を出して。
```

→ Cursor が修正点をまとめて出力する。**その修正点を Claude Code にコピーして渡し、「この修正点で記事を直して」**と依頼すると、Claude Code が修正した版を返してくれる。納めてある EDITORIAL_GUIDELINES と ASUNARU_EHIME_BRIEF を Cursor で共有し、Claude Code の記事をそれに合わせて整える流れになる。

### ステップ2: OK が出たら（Cursor に仕上げを依頼）
**Claude Code で記事を書いた場合**：できた本文を Cursor のチャットに貼り付けて、次のように依頼する。

```
OK。この記事の本文を drafts/ に draft_YYYY-MM-DD_タイトル.md で保存して。
Wix用の記事全文と、GBP用の概略テキストを drafts/ に保存して。
使ったトピック「〇〇」を used/log.md に日付付きで記録して、stock.md からは削除して。
```

**⚠️ GBPテキストの保存は必須（重要）**
- Wix は予約投稿のため、公開後にしか記事URLがわからない
- GBPテキストは記事作成時に `drafts/gbp_YYYY-MM-DD_タイトル.md` として必ず保存する
- 保存内容：GBP投稿テキスト本文＋「記事URL（公開後に記入）：」のプレースホルダー
- 記事が公開されたら、ファイルを開いてURLを記入し → GBPに貼り付けて投稿
- 「無料相談はこちらから」のCTAとリンクはGBPテキストには含めない

（日付・タイトル・トピック名は実際のものに置き換える。省略して「この記事を保存して、logとstockの更新もして」とだけ伝えてもよい。）

**画像について**：Claude Code が書いた「画像生成用プロンプト」を **ChatGPT** に貼り、「このプロンプトで画像を生成して」と依頼する。画像は ChatGPT の方が仕上がりが良いため。できた画像は `drafts/images/` に保存する。

→ Cursor が以下を行う：
- Wix に貼り付ける用の記事全文を `drafts/` に保存（ファイル名例: `draft_YYYY-MM-DD_タイトル.md`）
- GBP 用の短い概略＋「続きはブログで」リンク用テキストを `drafts/` に保存（例: `gbp_YYYY-MM-DD.txt`）
- `used/log.md` に使用したトピックと日付を追記
- `topics/stock.md` から使用したトピックを削除（または「使用済み」に移動）

---

### ステップ3: あなたが行うこと
1. **Wix**: `drafts/` の下書きファイルを開き、本文を Wix のブログ記事下書きにコピー。画像は `drafts/images/` を Wix メディアにアップロードして挿入。
2. **GBP**: 記事を公開したら、`drafts/gbp_YYYY-MM-DD.txt` の内容を Google Business Profile の投稿に貼り付け、詳細リンクに Wix ブログのURLを設定。

---

## 出力ファイルの例

| ファイル | 用途 |
|----------|------|
| `drafts/draft_2025-03-06_初めての結婚相談所の選び方.md` | Wix 記事下書き用本文 |
| `drafts/gbp_2025-03-06.txt` | GBP 用概略＋リンク用テキスト |
| `drafts/images/2025-03-06_eyecatch.png` | アイキャッチ画像（Wix にアップロード用） |
| `drafts/images/2025-03-06_diagram_見学の流れ.png` | 図解画像（必要な記事のみ） |
| `drafts/diagrams/2025-03-06_構成メモ.md` | 図解の構成案・メモ（必要時） |

## 図解が必要な記事のとき
流れ・比較・手順などを説明する記事では、`EDITORIAL_GUIDELINES.md` の「図解の要不要」に従い、記事作成時に「図解の構成案も出して」と依頼する。OK 後に図解画像を生成し `drafts/images/` に保存する。
