import streamlit as st
import librosa
import numpy as np
import tempfile
import time
from audiorecorder import audiorecorder
import plotly.graph_objects as go

# ページ設定（一番最初に書く！）
st.set_page_config(
    page_title="猫翻訳AI",
    page_icon="🐈",
    layout="centered"
)

# スマホ用スタイル
st.markdown("""
<style>
.block-container {
    max-width: 500px;
    padding-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 🐱 猫声を分析する関数
# ----------------------------------------
def analyze_cat_voice(audio_path):
    y, sr = librosa.load(audio_path)

    # ピッチ（音の高さ）を調べる
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[magnitudes > np.median(magnitudes)]
    pitch = float(np.mean(pitch_values)) if len(pitch_values) > 0 else 0

    # 音量を調べる
    energy = float(np.mean(librosa.feature.rms(y=y)))

    # 音色を調べる（精度アップの秘密兵器）
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = mfcc.mean(axis=1)

    # 感情を判定する
    if pitch > 800:
        emotion = "😾 怒り・警戒"
        message = "「あっちいけ！」「触らないで！」"
        confidence = 0.85
    elif pitch > 500 and energy > 0.05:
        emotion = "😺 要求・お腹すいた"
        message = "「ごはんちょうだい！」「遊んで！」"
        confidence = 0.80
    elif pitch > 300 and energy < 0.03:
        emotion = "😸 甘え・満足"
        message = "「なでて〜」「気持ちいい〜」"
        confidence = 0.75
    elif energy < 0.02:
        emotion = "😴 眠い・リラックス"
        message = "「zzz...」「眠いにゃ」"
        confidence = 0.70
    else:
        emotion = "🐱 おしゃべり"
        message = "「にゃにゃにゃ〜」"
        confidence = 0.60

    return emotion, message, pitch, energy, confidence, y, sr

# ----------------------------------------
# 🖥️ 画面の表示
# ----------------------------------------
st.title("🐈 猫翻訳AI")
st.write("猫の声を録音またはアップロードして感情を解析します")

# 翻訳履歴を記憶する（ページを更新しても消えない）
if 'history' not in st.session_state:
    st.session_state.history = []

# ----------------------------------------
# タブで「録音」と「アップロード」を切り替え
# ----------------------------------------
tab1, tab2 = st.tabs(["🎙️ 録音する", "📁 ファイルをアップロード"])

audio_path = None  # 後で使う変数

# === タブ1：録音 ===
with tab1:
    st.write("ボタンを押して猫の声を録音してください")
    audio = audiorecorder("🎙 録音開始", "⏹ 録音停止")

    if len(audio) > 0:
        st.audio(audio.export().read())
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio.export(tmp.name, format="wav")
            audio_path = tmp.name

# === タブ2：ファイルアップロード ===
with tab2:
    st.write("iPhoneのボイスメモなどをアップロードしてください")
    uploaded_file = st.file_uploader("音声ファイル", type=["wav", "mp3", "m4a"])

    if uploaded_file is not None:
        st.audio(uploaded_file)
        suffix = "." + uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            audio_path = tmp.name

# ----------------------------------------
# 🔍 分析スタート（録音orアップロードされたら自動で動く）
# ----------------------------------------
if audio_path is not None:

    # 「分析中...」のアニメーション表示
    with st.spinner("🧠 猫語を解析中..."):
        time.sleep(0.5)  # ちょっと待つ（演出）
        try:
            emotion, message, pitch, energy, confidence, y, sr = analyze_cat_voice(audio_path)
        except Exception as e:
            st.error(f"エラーが出ました: {e}")
            st.stop()

    # ----------------------------------------
    # 📊 リアルタイムモニタリング表示
    # ----------------------------------------
    st.success("✅ 解析完了！")

    # 大きく感情を表示
    st.markdown(f"## {emotion}")
    st.markdown(f"### {message}")

    # 信頼度をバーで表示
    st.write("**解析の信頼度**")
    st.progress(confidence)
    st.write(f"{confidence*100:.0f}%")

    # 数値を2列で表示
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🎵 ピッチ（音の高さ）", f"{pitch:.0f} Hz")
    with col2:
        st.metric("🔊 音量", f"{energy:.4f}")

    # 波形グラフをリアルタイムで表示
    st.write("**🌊 音声波形**")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=y[:2000],
        mode='lines',
        line=dict(color='#FF6B6B', width=1),
        name='波形'
    ))
    fig.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------
    # 📝 翻訳履歴に追加して表示
    # ----------------------------------------
    st.session_state.history.append({
        'time': time.strftime('%H:%M:%S'),
        'emotion': emotion,
        'message': message,
        'confidence': confidence
    })

    st.write("---")
    st.write("**📋 翻訳履歴（新しい順）**")
    for h in reversed(st.session_state.history[-10:]):  # 最新10件
        st.write(f"`{h['time']}` {h['emotion']} → {h['message']} （信頼度{h['confidence']*100:.0f}%）")

    # 履歴をリセットするボタン
    if st.button("🗑️ 履歴をリセット"):
        st.session_state.history = []
        st.rerun()
        
