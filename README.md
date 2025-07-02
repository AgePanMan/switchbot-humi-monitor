# SwitchBot データ可視化ダッシュボード

SwitchBot デバイス（温湿度計・スマートプラグ等）からデータを取得し、GitHub Pages 上で可視化する構成です。

## 📁 リポジトリ構成

```
├── app.py               # SwitchBot APIからデータ取得・DB登録
├── export_json.py       # DBから30日分のデータをdata.jsonにエクスポート
├── db.sqlite3           # SQLite DB（GitHub Actionsでは毎回初期化）
├── data.json            # 可視化用データファイル
├── requirements.txt     # 必要なPythonパッケージ
├── .env.example         # 環境変数ファイル雛形
└── index.html           # GitHub Pages で表示するHTMLダッシュボード
```

---

## 🌐 GitHub Pages 構成（公開用）

- `gh-pages` ブランチ：`index.html` + `data.json` を配置（静的ホスティング）
- `main` ブランチ：ソースコードと GitHub Actions 実行

---

## 🚀 初期セットアップ手順

### ✅ 1. リポジトリを clone

```bash
git clone https://github.com/<your-account>/switchbot-humi-monitor.git
cd switchbot-humi-monitor
```

### ✅ 2. `.env` を作成

`.env.example` を `.env` にコピーし、SwitchBot トークンを記入：

```env
SWITCHBOT_TOKEN=xxxxxxxxxxxxxxxxxx
```

### ✅ 3. ライブラリをインストール

```bash
pip install -r requirements.txt
```

### ✅ 4. 初回データ取得（ローカル）

```bash
python app.py
python export_json.py
```

### ✅ 5. ローカルで画面確認

Flaskサーバを起動して http://127.0.0.1:5000 を開く：

```bash
python app.py
```

---

## 🔄 GitHub Actions による自動実行

`.github/workflows/fetch.yml` により、SwitchBot API からのデータ取得 → `data.json` の更新 → `gh-pages` 反映を自動化します。

**毎時自動更新**、または手動実行 (`workflow_dispatch`) に対応。

---

## 🔒 Secrets 設定（GitHub Actions用）

GitHub のリポジトリ設定から `SWITCHBOT_TOKEN` を以下のように登録してください：

```
Settings > Secrets > Actions > New repository secret
Name: SWITCHBOT_TOKEN
Value: xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📊 ダッシュボード表示

- GitHub Pages URL 例：  
  `https://<your-account>.github.io/switchbot-humi-monitor/`

---

## 📎 ライセンス

MIT License.
