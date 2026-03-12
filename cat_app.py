import streamlit as st
import librosa
import numpy as np
import tempfile
import soundfile as sf
from audiorecorder import audiorecorder

st.set_page_config(
    page_title="猫翻訳AI",
    page_icon="🐈",
    layout="centered"
)

# スマホ向けレイアウト
st.markdown("""
<style>
.block-container{
max-width:500px;
padding-top:1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🐈 猫翻訳AI")

st.write("🎙 猫の声を録音して感情を解析します")

# 録音UI
audio = audiorecorder(
    "🎙 録音開始",
    "⏹ 録音停止"
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


if len(audio) > 0:

    st.audio(audio.export().read())

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:

        audio.export(tmp.name, format="wav")

        emotion, message, pitch, energy = analyze_cat_voice(tmp.name)

    st.success("解析結果")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🐾 感情", emotion)

    with col2:
        st.metric("💬 猫語翻訳", message)

    st.divider()

    st.metric("🎵 声の高さ", round(float(pitch),2))
    st.metric("🔊 声の強さ", round(float(energy),3))
