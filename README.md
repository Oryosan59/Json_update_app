# JSON Updater App

JSON Updater Appは、GUIを使用してJSONファイルを簡単に更新および処理するためのツールです。このアプリを使用すると、JSONファイルからデータを読み取り、新しいJSONファイルに段階的に保存することができます。

## 特徴
- **JSONファイルの選択**: 元のJSONファイルと新規保存先のファイルをGUIで簡単に選択可能。
- **進捗管理**: 処理の進捗状況をプログレスバーで視覚的に確認。
- **操作性**: 処理の開始、停止、一時停止/再開をボタンで簡単に操作。
- **安全性**: 元のJSONファイルがリスト形式でない場合のエラーチェック機能。

## 必要条件
- Python 3.7以上
- 以下のPythonライブラリ:
  - `tkinter`
  - `json`
  - `os`
  - `threading`

## インストール方法
1. Pythonをインストールします。
2. このリポジトリをクローンまたはダウンロードします。
   ```bash
   git clone https://github.com/your-repo/json-updater-app.git
   cd json-updater-app
   ```
3. 必要なライブラリは標準ライブラリのみを使用しているため、追加インストールは不要です。

## 使用方法
1. アプリを実行します:
   ```bash
   python JsonUpdateApp.py
   ```
2. アプリのGUIが表示されます。
3. **元のJSONファイル**を選択します:
   - 「元のJSONファイル」欄の「選択」ボタンをクリックし、処理したいJSONファイルを選択します。
4. **新規JSONファイル**を指定します:
   - 「新規JSONファイル」欄の「選択」ボタンをクリックし、出力ファイルの保存場所と名前を指定します。
5. 「開始」ボタンを押して処理を開始します。

### 主な操作ボタン
- **開始**: 処理を開始します。
- **一時停止**: 処理を一時停止します。もう一度クリックすると再開します。
- **停止**: 処理を完全に停止します。

## 注意事項
- 元のJSONファイルは必ずリスト形式である必要があります。辞書形式やその他の形式の場合、エラーとなります。
- 処理中に停止すると、出力ファイルには中途半端な状態のデータが書き込まれる可能性があります。

## 開発者向け情報
このアプリは、`threading`モジュールを使用して非同期処理を実現しています。`tkinter`を使用したシンプルなGUIを備え、ユーザーフレンドリーな設計になっています。

## ライセンス
このプロジェクトはMITライセンスの下で公開されています。
