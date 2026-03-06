# 自動スケジュール設定（約30分で完了）

**3日に1回**、**手動の流れ（Claude Code で記事を書く）を自動化**します。GitHub 上で Claude が記事を1本つくり、`drafts/` に保存・`stock.md` と `used/log.md` を更新。あとは手動と同じく、あなたがチェック → OK なら画像生成・Wix 投稿です。

---

## 前提

- このフォルダ（matchmaking-blog-workflow）を **GitHub のリポジトリ** として使うこと
- **API キー**を1つ用意する：**ANTHROPIC_API_KEY**（Claude＝手動の Claude Code と同じ）を推奨。未設定なら **OPENAI_API_KEY** でも動きます（有料です）。

---

## ステップ1：GitHub リポジトリを用意する（約5分）

**※ 初めてで「やり方がわからない」場合は → [STEP1_GITHUBのリポジトリの作り方.md](STEP1_GITHUBのリポジトリの作り方.md) に画面の流れとコマンドを詳しく書いてあります。**

1. [GitHub](https://github.com) にログインする。
2. 右上の **+** → **New repository** をクリック。
3. リポジトリ名を入力（例：`matchmaking-blog-workflow`）。**Private** のままでも **Public** でも可。
4. **Create repository** をクリック。
5. 自分のパソコンで、このフォルダがまだ Git 管理されていなければ、ターミナルで次を実行する（パスは実際のフォルダに合わせる）。

   ```bash
   cd /Users/nakashimamichi/Documents/matchmaking-blog-workflow
   git init
   git add .
   git commit -m "Initial: ブログワークフローと自動生成スクリプト"
   git branch -M main
   git remote add origin https://github.com/あなたのユーザー名/matchmaking-blog-workflow.git
   git push -u origin main
   ```

   ※ すでに `git init` 済みで別のフォルダからコピーしただけの場合は、`git remote add origin ...` と `git push` だけ実行すればよいです。

---

## ステップ2：API キーを取得する（約5分）

**手動の Claude Code と同じ流れにしたいなら、Anthropic（Claude）のキーを推奨します。**

### 推奨：Anthropic（Claude）の API キー

1. [Anthropic のコンソール](https://console.anthropic.com/) を開き、ログインする。
2. **API Keys** で **Create Key** をクリックし、名前（例：`blog-draft`）を付けて作成する。
3. 表示されたキーをコピーする（この画面を閉じると二度と表示されないのでメモしておく）。
4. GitHub の **Settings → Secrets and variables → Actions** で **New repository secret** をクリック。
   - **Name**: `ANTHROPIC_API_KEY`
   - **Secret**: コピーした Anthropic のキーを貼り付け → **Add secret**。

※ 請求先の設定が必要な場合があります。[Anthropic の Billing](https://console.anthropic.com/settings/billing) で確認してください。

### 代替：OpenAI の API キー

Anthropic を使わない場合は、**OPENAI_API_KEY** を登録すれば OpenAI（GPT）で記事を生成します。

1. [OpenAI のプラットフォーム](https://platform.openai.com/) で **API keys** → **Create new secret key**。
2. 表示されたキー（sk-...）をコピーする。
3. GitHub の **Settings → Secrets and variables → Actions** で **New repository secret**。
   - **Name**: `OPENAI_API_KEY`
   - **Secret**: コピーしたキーを貼り付け → **Add secret**。

※ スクリプトは **ANTHROPIC_API_KEY があれば Claude、なければ OPENAI_API_KEY** を使います。両方ある場合は Claude が使われます。

---

## ステップ3：GitHub に「秘密の値」を登録したか確認する（約1分）

上記のとおり、**ANTHROPIC_API_KEY**（推奨）または **OPENAI_API_KEY** のどちらかを **Settings → Secrets and variables → Actions** に登録していれば OK です。

---

## ステップ4：動作確認（約5分）

1. リポジトリのページで **Actions** タブを開く。
2. 左で **「ブログ下書きを自動作成（3日に1回）」** というワークフローを選ぶ。
3. 右の **Run workflow** → **Run workflow** をクリックする。
4. 数十秒〜1分ほど待つ。緑のチェックになれば成功。
5. **Code** タブに戻り、`drafts/` フォルダと `topics/stock.md`・`used/log.md` を開いて、下書きが1件増え、先頭トピックが削除され、log に1行追加されていれば完了です。

※ 初回は「トピックが1件も見つかりません」で終了することがあります。その場合は `topics/stock.md` にトピックが入っているか確認してください。

---

## 実行タイミング

- **自動**：**3日に1回**、日本時間で **翌朝5時頃**（UTC 20:00 のため）に実行されます。月の 1, 4, 7, 10, 13... 日など、約3日おきです。
- **手動**：いつでも **Actions** タブ → 該当ワークフロー → **Run workflow** で実行できます。

---

## トラブルシューティング

| 症状 | 確認すること |
|------|----------------|
| 「ANTHROPIC_API_KEY または OPENAI_API_KEY のどちらかを設定してください」 | **Settings** → **Secrets and variables** → **Actions** で、`ANTHROPIC_API_KEY` または `OPENAI_API_KEY` のどちらかが登録されているか確認。手動の流れに合わせるなら `ANTHROPIC_API_KEY`（Claude）を推奨。 |
| 「トピックが1件も見つかりません」 | `topics/stock.md` の `---` の下に、`- 〇〇` や `【〇〇】` の行が残っているか確認。 |
| API エラー（料金・制限） | [OpenAI の Billing](https://platform.openai.com/account/billing) でクレジット残高と利用上限を確認。 |
| ワークフローは成功するがリポジトリが更新されない | ブランチが `main` か確認。Actions の **Contents** 権限で **read and write** になっているかは、このワークフローでは `permissions: contents: write` で指定済みです。 |

---

## まとめ

1. **リポジトリを GitHub に push**
2. **OpenAI で API キーを取得**
3. **GitHub の Settings → Secrets に `OPENAI_API_KEY` を登録**
4. **Actions から「Run workflow」で1回試す**

ここまでできれば、あとは 3日に1回、自動で下書きが `drafts/` に追加され、あなたはそのファイルを開いて確認・編集するだけです。
