import streamlit as st
import librosa
import numpy as np
import tempfile
from pydub import AudioSegment

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

st.title("🐈 猫翻訳AI")

st.write("iPhoneボイスメモなどの猫の鳴き声をアップロードしてください")

uploaded_file = st.file_uploader(
    "📱 音声アップロード",
    type=["wav", "mp3", "m4a"]
)


# 音声をWAVに変換
def convert_to_wav(file_path):

    audio = AudioSegment.from_file(file_path)
    wav_path = file_path + ".wav"
    audio.export(wav_path, format="wav")

    return wav_path


# 猫声解析
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
        temp_path = tmp.name


    wav_path = convert_to_wav(temp_path)

    st.info("🧠 猫語を解析中...")

    emotion, message, pitch, energy = analyze_cat_voice(wav_path)

    st.success("解析結果")


    col1, col2 = st.columns(2)

    with col1:
        st.metric("🐾 感情", emotion)

    with col2:
        st.metric("💬 猫語翻訳", message)

    st.divider()

    st.metric("🎵 声の高さ", round(float(pitch),2))
    st.metric("🔊 声の強さ", round(float(energy),3))
