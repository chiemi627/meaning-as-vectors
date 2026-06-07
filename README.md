# 意味をベクトルで考える 🧭

線形代数学の授業「**意味をベクトルで考える**」で使う、**単語ベクトル（単語埋め込み）のリアルタイム演習アプリ**です。
高精度な日本語モデル **[chiVe](https://github.com/WorksApplications/chiVe)**（約 48 万語・300 次元）を使い、ブラウザ上で次の3つを体験できます。

| タブ | 内容 | 例 |
|---|---|---|
| ① 近い言葉をさがす | 意味が近い単語を検索（類似語） | 学校 → 中学校・小学校・授業・生徒 |
| ② 言葉の足し算・引き算 | ベクトル演算（アナロジー） | 王 − 男性 ＋ 女性 ＝ 王様・王女・女王 |
| ③ 2つの言葉の近さ | コサイン類似度を計算 | 犬 ↔ 猫 = 0.739 ／ 猫 ↔ 寿司 = 0.157 |

- ひらがな・カタカナで入力しても、Sudachi で自動正規化します（例: `りんご → 林檎`、`みかん → 蜜柑`）。
- 起動後はインターネット不要で動きます（モデルはローカルに保存されます）。

---

## 必要なもの

- **Python 3.9 以上**（macOS / Linux で動作確認）
- ディスク空き容量 **約 1.5GB**（モデル展開後）
- 初回セットアップ時のみネット接続（モデル約 549MB をダウンロード）

---

## セットアップ（初回のみ）

```bash
# 1. このリポジトリを取得
git clone https://github.com/chiemi627/meaning-as-vectors.git
cd meaning-as-vectors

# 2. まとめてセットアップ（仮想環境作成 + ライブラリ導入 + モデルDL）
bash setup.sh
```

`setup.sh` は次を自動で行います。

1. `venv/` に Python 仮想環境を作成
2. `requirements.txt` のライブラリをインストール
3. chiVe モデルをダウンロードして `model/` に展開

> 手動でやりたい場合は `setup.sh` の中身（数行）を参照してください。モデルだけ落とし直すときは `bash download_model.sh` です。

---

## 起動のしかた

```bash
./venv/bin/streamlit run app.py
```

ブラウザが自動で開きます（開かないときは `http://localhost:8501` にアクセス）。
初回起動だけモデル読み込みに十数秒かかります。2 回目以降は速くなります。

### macOS なら（おすすめ）

Finder で **`起動.command` をダブルクリック**するだけです。
※ 初回は「開発元を確認できません」と出ることがあります。その場合は `起動.command` を**右クリック →「開く」→「開く」**で一度許可してください。

### 終了のしかた

- ブラウザのタブを閉じる
- 起動時に開いたターミナルで **Control + C**（またはウィンドウを閉じる）

---

## ファイル構成

```
単語ベクトル演習/
├── app.py             … アプリ本体（Streamlit）
├── requirements.txt   … 必要なライブラリ
├── setup.sh           … 初回セットアップ（venv + ライブラリ + モデルDL）
├── download_model.sh  … モデルだけダウンロードする補助スクリプト
├── 起動.command       … macOS 用ワンクリック起動
└── model/             … モデル本体（Git には含めず各自DL）
```

---

## 授業での使い方メモ

- スライド5「演習1：近い言葉を探そう」→ タブ①
- スライド7「演習2：言葉の演算をしてみよう」→ タブ②
- スライド4「『近い』ってどういうこと？」の犬・猫・寿司 → タブ③
- 「スマホ − 電話 ＋ 写真」は `スマートフォン` で入れるときれいに出ます。

---

## ライセンス / クレジット

- 単語ベクトルモデル: **chiVe 1.2 mc90**
  Copyright (c) National Institute for Japanese Language and Linguistics and Works Applications Co., Ltd.
  [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) で配布されています。
  <https://github.com/WorksApplications/chiVe>
- 形態素解析: [Sudachi / SudachiPy](https://github.com/WorksApplications/SudachiPy)（Apache License 2.0）

作成: 渡辺知恵美（産業情報学科）／ 線形代数学 授業教材
