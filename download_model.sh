#!/bin/bash
# chiVe 単語ベクトルモデル（1.2 mc90, gensim 形式）をダウンロード・展開します。
# 展開後の配置: model/chive-1.2-mc90_gensim/chive-1.2-mc90.kv
set -e
cd "$(dirname "$0")"

URL="https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc90_gensim.tar.gz"
DEST="model/chive-1.2-mc90_gensim/chive-1.2-mc90.kv"

if [ -f "$DEST" ]; then
  echo "✓ モデルは既にあります: $DEST"
  exit 0
fi

mkdir -p model
echo "chiVe モデルをダウンロードします（約 549MB）…"
curl -L -o model/chive.tar.gz "$URL"
echo "展開中…"
tar -xzf model/chive.tar.gz -C model
rm -f model/chive.tar.gz
echo "✓ 完了: $DEST"
