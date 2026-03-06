# ステップ1 詳解：GitHub のリポジトリを用意して、フォルダをのせる

「最初の一つ」＝**GitHub にリポジトリを作り、今のフォルダ（matchmaking-blog-workflow）をそこに載せる**手順です。このフォルダを GitHub 上に置くことで、あとで「3日に1回の自動実行」が動くようになります。

---

## A. GitHub でリポジトリを「空で」作る（画面でやること）

1. **ブラウザで https://github.com を開く**
2. **ログイン**する（アカウントがなければ「Sign up」で作成）
3. **右上の「＋」マーク** をクリック → **「New repository」** を選ぶ
4. 次のように入力する：
   - **Repository name**（リポジトリ名）：`matchmaking-blog-workflow` と入力（そのままでOK）
   - **Private** のままでも **Public** でもどちらでもよい
   - **「Add a README file」などにはチェックを入れない**（何も追加しない「空」のリポジトリにする）
5. **「Create repository」** をクリック
6. 作成されると、「…or push an existing repository from the command line」という説明が出た画面になる。**この画面は開いたまま**にしておく（あとでここに書いてあるコマンドを使う）

---

## B. 自分のパソコンで「このフォルダ」を Git の管理下にして GitHub に送る（ターミナルでやること）

ここでは **ターミナル（コマンドを打つ画面）** を使います。  
Mac なら **「ターミナル」** アプリを開いてください（Spotlight で「ターミナル」と検索すると出てきます）。

### B-1. フォルダに移動する

ターミナルに、次の **1行** をコピーして貼り付け、Enter を押します。

```bash
cd /Users/nakashimamichi/Documents/matchmaking-blog-workflow
```

※ このフォルダが別の場所にある場合は、そのパスに書き換えてください。

---

### B-2. まだ Git を使っていない場合だけ：Git を初期化する

次のコマンドを **1行ずつ** 実行します。すでにこのフォルダで `git init` をしたことがある場合は、「fatal: not a git repository」と出なければ **B-3 へ進んでOK** です。

```bash
git init
```

```bash
git add .
```

```bash
git commit -m "Initial: ブログワークフローと自動生成スクリプト"
```

```bash
git branch -M main
```

---

### B-3. GitHub の「自分のリポジトリ」とつなげる

**「あなたのユーザー名」** のところを、GitHub のユーザー名に書き換えてから実行してください。  
例：GitHub のユーザー名が `nakashima` なら、  
`https://github.com/nakashima/matchmaking-blog-workflow.git` になります。

```bash
git remote add origin https://github.com/あなたのユーザー名/matchmaking-blog-workflow.git
```

※ すでに `origin` があるとエラーになる場合は、  
`git remote remove origin` を実行してから、もう一度 `git remote add origin ...` を実行してください。

---

### B-4. GitHub に送る（push）

```bash
git push -u origin main
```

ここで **GitHub のユーザー名とパスワード** を聞かれた場合：

- **パスワード** には、GitHub の「ログイン用パスワード」は使えません。  
  **Personal Access Token（PAT）** を使います。
- 作り方：GitHub の画面で **右上のアイコン → Settings → Developer settings → Personal access tokens** で「Generate new token」からトークンを作り、そのトークンを「パスワード」の欄に貼り付けてください。
- まだトークンを作ったことがない場合は、[GitHub の説明](https://docs.github.com/ja/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) を参照するか、「GitHub Personal Access Token 作り方」で検索すると手順が出てきます。

**push が成功すると**、GitHub のリポジトリのページを更新すると、フォルダの中身（WORKFLOW.md や topics/stock.md など）が一覧で見えるようになります。

---

## ここまでできたら「ステップ1」は完了

- GitHub に **matchmaking-blog-workflow** というリポジトリができている  
- その中に、今のフォルダの内容が全部上がっている  

この2つができていれば、次の **ステップ2（OpenAI の API キー取得）** に進んで大丈夫です。

---

## うまくいかないとき

| 症状 | 対処 |
|------|------|
| `git` と打っても「command not found」 | パソコンに Git が入っていません。[Git の公式](https://git-scm.com/downloads) からインストールするか、**GitHub Desktop** を入れて、そのアプリから「Add local repository」でこのフォルダを選び、Publish する方法でもOKです。 |
| `git push` で「Permission denied」や「Authentication failed」 | GitHub にログインする情報が足りていません。**Personal Access Token** を作り、パスワードの代わりにそのトークンを使うか、**GitHub Desktop** でログインしてから再度 push を試してください。 |
| 「あなたのユーザー名」がわからない | GitHub にログインした状態で、右上のアイコンをクリックすると表示される名前、またはブラウザのアドレスバーに `github.com/〇〇` と出ている **〇〇** がユーザー名です。 |

まだ「ここがわからない」というところがあれば、その画面やメッセージを教えてもらえれば、そこだけもう少し砕いて説明できます。
