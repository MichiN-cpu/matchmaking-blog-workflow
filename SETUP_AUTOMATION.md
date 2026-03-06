# 自動スケジュール設定（約30分で完了）

**3日に1回**、GitHub 上でブログ下書きを自動作成し、`drafts/` に保存・`stock.md` と `used/log.md` を更新するための設定手順です。API キーと GitHub の「秘密の値」を安全に設定すれば動きます。

---

## 前提

- このフォルダ（matchmaking-blog-workflow）を **GitHub のリポジトリ** として使うこと
- **OpenAI の API キー** を1つ取得すること（有料ですが、1記事あたり数円程度の利用量です）

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

## ステップ2：OpenAI の API キーを取得する（約5分）

1. [OpenAI のプラットフォーム](https://platform.openai.com/) を開き、ログインする（アカウントがない場合は作成）。
2. 左メニューで **API keys**（API キー）を開く。
3. **Create new secret key** をクリックし、名前（例：`blog-draft`）を付けて作成する。
4. 表示された **キー（sk-...で始まる文字列）** をコピーする。**この画面を閉じると二度と表示されない**ので、メモ帳などに一時的に貼り付けておく。

※ 請求先を設定していない場合は、先に [Billing](https://platform.openai.com/account/billing) でクレジットカードなどを登録する必要があります。利用量は少ないので、数ドル分のチャージで長く使えます。

---

## ステップ3：GitHub に「秘密の値」を登録する（約3分）

1. 自分の **リポジトリのページ**（matchmaking-blog-workflow）を開く。
2. 上部メニューの **Settings** をクリック。
3. 左メニューで **Secrets and variables** → **Actions** をクリック。
4. **New repository secret** をクリック。
5. 次のように入力する。
   - **Name**: `OPENAI_API_KEY`（この名前のまま、1文字も変えない）
   - **Secret**: ステップ2でコピーした API キー（sk-...）を貼り付ける
6. **Add secret** をクリックする。

これで、GitHub Actions からは「OPENAI_API_KEY という名前の秘密の値」として参照され、画面には表示されません。

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
| 「OPENAI_API_KEY が設定されていません」 | リポジトリの **Settings** → **Secrets and variables** → **Actions** で、名前が `OPENAI_API_KEY` の秘密が1つあるか確認。 |
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
