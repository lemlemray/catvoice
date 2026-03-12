import streamlit as st
import librosa
import numpy as np
import tempfile

# ページ設定（スマホ対応）
st.set_page_config(
    page_title="猫翻訳AI",
    page_icon="🐈",
    layout="centered"
)

# スマホ用余白調整
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 500px;
}
</style>
""", unsafe_allow_html=True)


st.title("🐈 猫翻訳AI")

st.write("猫の鳴き声をアップロードすると感情を解析します。")


uploaded_file = st.file_uploader(
    "📱 猫の声をアップロード",
    type=["wav", "mp3", "m4a"]
)


def analyze_cat_voice(audio_path):

    y, sr = librosa.load(audio_path)

    pitch = np.mean(librosa.yin(y, fmin=50, fmax=500))
    energy = np.mean(librosa.feature.rms(y=y))

    if pitch > 320:
        emotion = "甘えている"
        message = "ねえ、こっち来てよ"
    elif energy > 0.12:
        emotion = "要求している"
        message = "ごはんまだ？"
    else:
        emotion = "落ち着いている"
        message = "今日はのんびりしてる"

    return emotion, message, pitch, energy


if uploaded_file is not None:

    st.audio(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    st.info("🧠 猫語を解析中...")

    emotion, message, pitch, energy = analyze_cat_voice(path)

    st.success("解析結果")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🐾 感情", emotion)

    with col2:
        st.metric("💬 猫語翻訳", message)

    st.divider()

    st.metric("🎵 声の高さ", round(float(pitch),2))
    st.metric("🔊 声の強さ", round(float(energy),3))
