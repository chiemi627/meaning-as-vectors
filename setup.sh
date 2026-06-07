#!/bin/bash
# 初回セットアップ: 仮想環境の作成 → ライブラリ導入 → モデルのダウンロード
# 使い方:  bash setup.sh
set -e
cd "$(dirname "$0")"

echo "==> Python 仮想環境を作成します (venv/)"
python3 -m venv venv

echo "==> ライブラリをインストールします"
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "==> 単語ベクトルモデルをダウンロードします"
bash download_model.sh

echo ""
echo "✓ セットアップ完了！ 次のコマンドで起動できます:"
echo "    ./venv/bin/streamlit run app.py"
echo "  （macOS なら 起動.command をダブルクリックでもOK）"
