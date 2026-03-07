import streamlit as st
import librosa
import numpy as np
import tempfile
from pydub import AudioSegment
import os
import time

st.title("🐱 猫翻訳AI")

st.write("猫の声をアップロードしてください")
st.write("※動画は解析に最大30秒ほどかかります")

uploaded_file = st.file_uploader(
    "音声または動画",
    type=["wav","mp3","m4a","mp4","mov"]
)

def analyze_meow(y, sr):

    pitch = np.mean(librosa.yin(y, fmin=50, fmax=500))
    energy = np.mean(librosa.feature.rms(y=y))

    if pitch > 350:
        return "🐱 甘えている"
    elif energy > 0.1:
        return "🐱 ごはん要求"
    else:
        return "🐱 警戒"

if uploaded_file:

    st.audio(uploaded_file)

    progress = st.progress(0)
    status = st.empty()

    status.write("ファイルを処理しています…")

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    try:

        progress.progress(20)
        status.write("音声を抽出しています…")

        audio = AudioSegment.from_file(temp_path)
        audio = audio[:10000]

        wav_path = temp_path + ".wav"

        progress.progress(40)
        status.write("音声を変換しています…")

        audio.export(wav_path, format="wav")

        progress.progress(70)
        status.write("猫語を解析しています…")

        y, sr = librosa.load(wav_path, sr=None)

        result = analyze_meow(y, sr)

        progress.progress(100)
        status.write("解析完了")

        st.success("翻訳結果： " + result)

    except Exception as e:
        st.error("音声処理エラー")
        st.text(e)

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)