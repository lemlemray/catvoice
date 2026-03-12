import streamlit as st
import librosa
import numpy as np
import tempfile

st.title("🐈 猫翻訳AI")

st.write("猫の声をアップロードしてください")

uploaded_file = st.file_uploader(
    "音声ファイル",
    type=["wav","mp3","m4a"]
)

def analyze_cat_voice(audio_path):

    y, sr = librosa.load(audio_path)

    pitch = np.mean(librosa.yin(y, fmin=50, fmax=500))
    energy = np.mean(librosa.feature.rms(y=y))

    if pitch > 300:
        emotion = "甘えている"
    elif energy > 0.1:
        emotion = "何か要求している"
    else:
        emotion = "リラックスしている"

    return emotion, pitch, energy


if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    emotion, pitch, energy = analyze_cat_voice(path)

    st.success("解析結果")

    st.write("感情:", emotion)
    st.write("声の高さ:", float(pitch))
    st.write("声の強さ:", float(energy))
