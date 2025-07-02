# 📊 SwitchBot ダッシュボード（JSON出力連携）

SwitchBot の「温湿度計」「スマートプラグ」などのデバイス情報を取得し、  
**SQLiteに保存 → JSON形式で出力 → GitHub Pagesで可視化**できる仕組みです。

---

## 🔧 ローカルセットアップ手順

```bash
git clone https://github.com/yourname/switchbot-dashboard.git
cd switchbot-dashboard
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### `.env` を作成

```
SWITCHBOT_TOKEN=あなたのSwitchBotトークン
```

---

## 🧪 テスト実行（ローカル）

```bash
python app.py            # データ収集（DBに格納）
python export_json.py    # JSONとして出力（data.json）
```

---

## 🚀 GitHub Actions で自動取得・出力

`.github/workflows/fetch_and_export.yml` が自動実行します。

- デバイス情報を取得
- SQLiteに保存
- `export_json.py` で `data.json` を出力
- `git push` で GitHub Pages に反映可能

---

## 🔐 シークレットの設定

GitHubの [Settings] → [Secrets] → `SWITCHBOT_TOKEN` を登録。

---

## 🌐 GitHub Pages でグラフ表示（index.html）

別ブランチ（例: `gh-pages`）に `index.html` を配置し、  
GitHub Pages の設定から公開すれば Web可視化も無料で可能です。

URL例: `https://yourname.github.io/switchbot-dashboard`

---

## 📁 構成例

```
switchbot-dashboard/
├── app.py
├── export_json.py
├── db.sqlite3
├── data.json
├── requirements.txt
├── .env.example
├── README.md
└── .github/workflows/
    └── fetch_and_export.yml
```

---

## 🙋 お問い合わせ・貢献

Issue や Pull Request にてお待ちしています！
