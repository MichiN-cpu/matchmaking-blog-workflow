# みっちゃんの物語シリーズ — 統一アバター スタイルガイド

2026-08-17 決定。「57歳、仲人婚活始めました。」シリーズで使う、みっちゃんのイラストアバター。

## 決定事項

- **スタイル**：少女漫画風（B案）
- **生成方法**：実写を元に image-to-image で変換する（テキストのみでの生成は、垂れ目など本人の特徴が反映されず「別人」「おばあちゃんっぽい」になる問題があったため不採用）
- **元にする実写**：`/Users/nakashimamichi/Downloads/中嶋.jpeg`（本人提供、スタジオ撮影の正面顔写真）

## 生成プロンプトテンプレート（image-to-imageのprompt欄）

```
Transform this photo into a soft shoujo manga style illustration.
Preserve her actual facial features precisely: her distinctive downturned/drooping eyes shape,
her face structure, her hairstyle. Delicate linework, gentle screentone shading,
slightly stylized but proportionate, dreamy soft color palette, Japanese girls' comic aesthetic.
Warm confident smile, dignified feel, not overly aged, not overly young.
[ここにシーン固有の描写を追加：場所・ポーズ・表情・光の質など]
```

## 調整の経緯（次回の参考用）

1. v1（テキストのみ生成）→「おばあちゃんっぽい」と却下
2. v2（若返らせすぎ）→「若すぎる」と却下
3. v3（年齢を戻す）→「もうちょい若く」と却下
4. v4（中間調整）→「垂れ目が全然違う、本人に見えない」と気づく（テキストのみ生成の根本限界）
5. v5（実写からimage-to-image、本人提供の写真を使用）→ **B案（少女漫画風）で決定**

## Why
テキストだけでは「みっちゃん本人」の顔の特徴（特に垂れ目）を再現できない。実写を起点にすることで、本人らしさを保ったまま画風だけを変換できる。

## How to apply
今後このシリーズで新しい画像が必要になったら、上記のプロンプトテンプレートに`/Users/nakashimamichi/Downloads/中嶋.jpeg`を入力画像として渡し、シーンごとの描写を追記して生成する。

## 2026-08-30：色味・表情の調整、差し替え実施

第1話アイキャッチ（`2026-08-17_57sai_eyecatch.png`）が、色味がセピア調で薄く・表情も伏し目がちで寂しい印象に見えるとみっちゃんから指摘（「楽しい婚活が始まった感じにならない」）。`2026-08-30_57sai_eyecatch_v3.png`に差し替え、Wix上で公開済み（post ID: 771006c5-5963-457e-b7c9-cdf514e0a0ac）。

**プロンプトに追加した指定（次回以降も踏襲）：**
- 色：「vivid and warm, NOT pale, NOT sepia, NOT washed-out, NOT desaturated」を明記（テンプレートの「dreamy soft color palette」だけだと薄く出やすい）
- 表情：「genuinely joyful, bright, eyes sparkling with excitement and hope, a warm open smile」を明記（「warm confident smile」だけだと控えめな微笑みになりがち）
- ⚠️ **image-to-imageで元写真にノートPC等の小物が写っていると、実在ブランドのロゴ（今回は「LAVIE」）がそのまま再現されてしまう事故が1回発生**。以後、小物を出すシーンでは "no text, no logos, no brand names, no readable writing, no electronic devices" を明記してブロックする
