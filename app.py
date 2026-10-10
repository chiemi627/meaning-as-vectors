# -*- coding: utf-8 -*-
"""
意味をベクトルで考える ― 授業用 単語ベクトル演習アプリ
モデル: chiVe 1.2 mc90 (日本語単語埋め込み, 約48万語, 300次元)
起動:  ./venv/bin/streamlit run app.py
"""
import os
import streamlit as st
from gensim.models import KeyedVectors
from sudachipy import Dictionary, SplitMode

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model", "chive-1.2-mc90_gensim", "chive-1.2-mc90.kv",
)

st.set_page_config(page_title="意味をベクトルで考える", page_icon="🧭", layout="centered")

# ---- 授業プロジェクタ向けに文字を大きく ----
st.markdown(
    """
    <style>
      html, body, [class*="css"] { font-size: 20px; }
      .stTextInput input { font-size: 26px; }
      h1 { font-size: 40px !important; }
      .result-word { font-size: 30px; font-weight: 700; }
      .result-score { color: #1C7293; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="日本語モデルを読み込み中…（初回のみ少し時間がかかります）")
def load_model():
    return KeyedVectors.load(MODEL_PATH)


@st.cache_resource(show_spinner=False)
def load_tokenizer():
    return Dictionary().create()


kv = load_model()
tokenizer = load_tokenizer()


def normalize(word: str) -> str:
    """Sudachiでりんご→林檎のように正規化（chiVeの見出し語に合わせる）"""
    morphs = tokenizer.tokenize(word, SplitMode.C)
    return "".join(m.normalized_form() for m in morphs)


def reading(word: str) -> str:
    """読み（カタカナ）。同音・別表記の重複を見つけるのに使う。"""
    try:
        return "".join(m.reading_form() for m in tokenizer.tokenize(word, SplitMode.C))
    except Exception:
        return word


def is_noun(word: str) -> bool:
    """名詞を含むか（Web学習モデルの変なトークンを除外するため）"""
    return any(m.part_of_speech()[0] == "名詞"
               for m in tokenizer.tokenize(word, SplitMode.C))


def clean_similar(positive, negative=None, topn=8):
    """most_similar の結果からノイズを除いて返す。
    除外: 1文字 / 入力語や既出結果の断片 / 同音・別表記の重複 / 非名詞。"""
    negative = negative or []
    inputs = positive + negative
    raw = kv.most_similar(positive=positive, negative=negative, topn=80)
    seen_read = {reading(w) for w in inputs}
    accepted, out = [], []
    for w, s in raw:
        if len(w) < 2:
            continue
        if any(w in q for q in inputs):        # 入力語の断片（ロンドン→ンドン 等）
            continue
        if any(w in a for a in accepted):      # 既出結果の断片（イギリス→ギリス 等）
            continue
        r = reading(w)
        if r in seen_read:                     # 同音・別表記の重複（犬→椀子, イヌ 等）
            continue
        if not is_noun(w):
            continue
        seen_read.add(r)
        accepted.append(w)
        out.append((w, s))
        if len(out) >= topn:
            break
    # 万一すべて除外されたら、素の結果にフォールバック
    return out if out else raw[:topn]


def resolve(word: str):
    """(モデルで使う語 or None, 変換メモ or None) を返す。表記ゆれを自動で吸収。
    chiVeはSudachi正規化形が見出し語なので、まず正規化形を優先して引く。"""
    word = word.strip()
    if not word:
        return None, None
    n = normalize(word)
    if n in kv.key_to_index:
        return n, (f"{word} → {n}" if n != word else None)
    if word in kv.key_to_index:
        return word, None
    return None, None


def resolve_all(words):
    """[(使う語, メモ), ...] と 見つからなかった語のリスト を返す"""
    resolved, notes, missing = [], [], []
    for w in words:
        r, note = resolve(w)
        if r is None:
            missing.append(w)
        else:
            resolved.append(r)
            if note:
                notes.append(note)
    return resolved, notes, missing


def show_notes(notes):
    if notes:
        st.caption("自動でモデルの見出し語に変換しました：　" + "　／　".join(notes))


def show_results(pairs):
    """[(word, score), ...] を大きく表示"""
    for w, s in pairs:
        bar = int(round(s * 100))
        st.markdown(
            f'<div class="result-word">{w} '
            f'<span class="result-score">{s:.3f}</span></div>',
            unsafe_allow_html=True,
        )
        st.progress(max(0, min(100, bar)))


st.title("🧭 意味をベクトルで考える")
st.caption(f"日本語モデル chiVe（{len(kv.index_to_key):,} 語・{kv.vector_size}次元）でリアルタイムに計算します")

tab1, tab2, tab3 = st.tabs(["① 近い言葉をさがす", "② 言葉の足し算・引き算", "③ 2つの言葉の近さ"])

# ===== 演習1: 類似語検索 =====
with tab1:
    st.subheader("近い言葉をさがそう")
    st.write("言葉を1つ入力すると、意味が近い言葉を AI が探します。")
    word = st.text_input("言葉", value="学校", key="sim_word")
    topn = st.slider("いくつ表示する？", 3, 15, 8, key="sim_topn")
    if st.button("さがす", key="sim_btn", type="primary"):
        used, notes, miss = resolve_all([word])
        if miss:
            st.error(f"この言葉はモデルに入っていません: {', '.join(miss)}")
        else:
            show_notes(notes)
            show_results(clean_similar(positive=used, topn=topn))

# ===== 演習2: 単語の演算 =====
with tab2:
    st.subheader("言葉の足し算・引き算")
    st.write("例：　王 − 男性 ＋ 女性 ＝ ?")
    c1, c2, c3 = st.columns(3)
    a = c1.text_input("＋ たす（A）", value="王", key="an_a")
    b = c2.text_input("− ひく（B）", value="男性", key="an_b")
    c = c3.text_input("＋ たす（C）", value="女性", key="an_c")
    st.latex(r"A - B + C = \;?")
    topn2 = st.slider("いくつ表示する？", 3, 15, 8, key="an_topn")
    if st.button("計算する", key="an_btn", type="primary"):
        pos, pos_notes, pos_miss = resolve_all([w for w in [a, c] if w.strip()])
        neg, neg_notes, neg_miss = resolve_all([w for w in [b] if w.strip()])
        miss = pos_miss + neg_miss
        if miss:
            st.error(f"この言葉はモデルに入っていません: {', '.join(miss)}")
        else:
            show_notes(pos_notes + neg_notes)
            st.markdown(f"### {a} − {b} ＋ {c} ＝")
            show_results(clean_similar(positive=pos, negative=neg, topn=topn2))

    with st.expander("ほかの例を見る"):
        st.write("・日本 − 東京 ＋ ロンドン ＝ ?")
        st.write("・スマホ − 電話 ＋ 写真 ＝ ?（※スマホは『スマートフォン』で試すと良い）")
        st.write("・パリ − フランス ＋ 日本 ＝ ?")

# ===== 演習3: 2語の類似度 =====
with tab3:
    st.subheader("2つの言葉はどれくらい近い？")
    st.write("コサイン類似度（1に近いほど意味が近い）を計算します。")
    c1, c2 = st.columns(2)
    w1 = c1.text_input("言葉1", value="犬", key="d_w1")
    w2 = c2.text_input("言葉2", value="猫", key="d_w2")
    if st.button("くらべる", key="d_btn", type="primary"):
        used, notes, miss = resolve_all([w1, w2])
        if miss:
            st.error(f"この言葉はモデルに入っていません: {', '.join(miss)}")
        else:
            show_notes(notes)
            r1, r2 = used
            sim = float(kv.similarity(r1, r2))
            st.markdown(
                f'<div class="result-word">{r1} ↔ {r2} '
                f'<span class="result-score">{sim:.3f}</span></div>',
                unsafe_allow_html=True,
            )
            st.progress(max(0, min(100, int(round(sim * 100)))))
            if sim >= 0.5:
                st.success("意味がとても近いね！")
            elif sim >= 0.25:
                st.info("少し関係がありそう。")
            else:
                st.warning("あまり近くないみたい。")
