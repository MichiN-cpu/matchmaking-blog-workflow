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
