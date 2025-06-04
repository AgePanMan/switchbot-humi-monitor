# 📊 SwitchBot ダッシュボード

SwitchBot の「温湿度計」や「スマートプラグ」のデータを収集してグラフ表示するダッシュボードです。  
**Python + GitHub Actions + GitHub Pages** を使って、無料で自動取得・グラフ化が可能です。

---

## 🔧 セットアップ手順（ローカル）

### 1. GitHubからクローン

```bash
git clone https://github.com/あなたのユーザー名/switchbot-dashboard.git
cd switchbot-dashboard
```

### 2. 仮想環境の作成（初回のみ）

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🔑 3. `.env` ファイルの作成

SwitchBot の APIトークンを保存する `.env` ファイルを作ります：

```
SWITCHBOT_TOKEN=ここにあなたのトークン
```

※ `.env` は `.gitignore` に含まれており、Gitにはアップロードされません。

---

## 🧪 4. データ取得を実行（ローカルテスト）

```bash
python app.py
```

データが `db.sqlite3` に保存され、`data.json` に出力されます。

---

## 🚀 GitHub Actions（自動データ取得）の設定

### `.github/workflows/fetch_and_commit.yml` の内容

```yaml
name: Fetch SwitchBot Data

on:
  schedule:
    - cron: '*/15 * * * *'  # 15分ごと
  workflow_dispatch:

jobs:
  fetch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - name: 実行
        env:
          SWITCHBOT_TOKEN: ${{ secrets.SWITCHBOT_TOKEN }}
        run: python app.py
      - name: Commit更新
        run: |
          git config --global user.email "actions@github.com"
          git config --global user.name "GitHub Actions"
          git add data.json db.sqlite3
          git commit -m "Update sensor data" || echo "No changes"
          git push
```

### 🔐 シークレットの登録

1. GitHub → [Settings] → [Secrets and variables] → [Actions]
2. `SWITCHBOT_TOKEN` という名前で、トークンを登録します

---

## 🌐 GitHub Pages でダッシュボード公開

### `gh-pages` ブランチを作って index.html を配置

```bash
git checkout --orphan gh-pages
git rm -rf .
cp index.html .
git add index.html
git commit -m "Init GitHub Pages"
git push origin gh-pages
```

### GitHub の Pages 設定

1. リポジトリ Settings → Pages
2. Branch を `gh-pages` に設定
3. 公開URL（例）: `https://yourname.github.io/switchbot-dashboard`

---

## 📁 プロジェクト構成（例）

```
switchbot-dashboard/
├── app.py                # データ取得スクリプト
├── sensor_calculations.py  # 絶対湿度などの計算
├── db.sqlite3            # SQLiteデータベース
├── data.json             # フロントエンド用データ
├── index.html            # ダッシュボードUI
├── .env                  # APIトークン（git管理外）
├── requirements.txt      # Python依存ライブラリ
└── .github/workflows/
    └── fetch_and_commit.yml
```

---

## 💡 ヒント

- GitHub Actions は **無料で毎月2,000分まで** 利用できます
- GitHub Pages は **無料で静的Webサイトをホスト**できます
- SQLiteのファイルは `.gitignore` で除外してもOKです

---

## 🙋 サポート・貢献

質問や要望は Issue でどうぞ！Pull Request も歓迎します。
