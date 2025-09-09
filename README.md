# Researchmap データ削除ツール

Researchmap上のデータを削除するcsvを作るコマンドです。


## 概要

Researchmapに登録したデータは一括削除をするのが大変です。本コマンドを利用すると、「一括削除用のcsvファイル」を作れます。このcsvをウェブ上からインポートすることで、データを一括削除できます。


### 使用方法
たとえばあなたのpermalink（researchmapにおけるID。[https://researchmap.jp/matsui528](https://researchmap.jp/matsui528)の場合は`matsui528`）が`matsui528`だとしましょう。その場合、下記を実行してください。
```bash
python delete_researchmap.py --permalink matsui528
```

## 出力ファイル

実行すると以下のファイルが生成されます：

1. **削除用CSVファイル**: `delete_{データタイプ}.csv`
   - ResearchMapの一括削除機能で使用可能な形式
   - 各ファイルには対応するデータタイプ（論文、プロジェクトなど）の削除コマンドが含まれます

2. **デバッグ用JSONファイル**: `researchmap_{パーマリンク}_debug.json`
   - APIから取得した生データ
   - トラブルシューティング用
