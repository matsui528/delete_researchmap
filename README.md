# Researchmap データ削除ツール

Researchmap上のデータを削除するcsvを作るコマンドです。


## 概要

Researchmapに登録したデータは一括削除をするのが大変です。本コマンドを利用すると、「一括削除用のcsvファイル」を作れます。このcsvをウェブ上からインポートすることで、データを一括削除できます。


### 使用方法
たとえばあなたのpermalink（researchmapにおけるID。[https://researchmap.jp/matsui528](https://researchmap.jp/matsui528)の場合は`matsui528`）が`matsui528`だとしましょう。その場合、下記を実行してください。
```bash
python delete_researchmap.py --permalink matsui528
```
（上記のコマンドは以下のcsvファイルを生成するだけで、Researchmap上のデータを直接削除したりすることはありません）

## 出力ファイル

実行すると以下のファイルが生成されます：

1. **削除用CSVファイル**: 例：`delete_published_papers.csv`, `delete_presentations.csv`, などなど・・
   - ResearchMapの一括削除で使用可能な形式になっています。これを直接Researchmapにアップロード（インポート）してください。そうするとそれらのデータが全て消えます。
   - 各ファイルには対応するデータタイプ（論文、プロジェクトなど）の削除コマンドが含まれています。

2. **デバッグ用JSONファイル**: 例：`researchmap_matsui528_debug.json`
   - APIから取得した生データです。
   - トラブルシューティング用です。
