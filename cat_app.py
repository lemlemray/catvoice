import streamlit as st
import librosa
import numpy as np
import soundfile as sf
import tempfile
from moviepy.editor import VideoFileClip

st.title("🐈 猫翻訳AI")

st.write("猫の声（音声または動画）をアップロードしてください")

uploaded_file = st.file_uploader(
    "ファイルアップロード",
    type=["wav", "mp3", "m4a", "mp4", "mov"]
)

def extract_audio_from_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = video_path + ".wav"
    video.audio.write_audiofile(audio_path)
    return audio_path

def analyze_cat_voice(audio_path):

    y, sr = librosa.load(audio_path)

    pitch = np.mean(librosa.yin(y, fmin=50, fmax=500))
    energy = np.mean(librosa.feature.rms(y=y))

    if pitch > 300:
        emotion = "甘え"
    elif energy > 0.1:
        emotion = "要求"
    else:
        emotion = "リラックス"

    return emotion, pitch, energy


if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    if uploaded_file.type.startswith("video"):
        st.write("動画から音声抽出中...")
        audio_path = extract_audio_from_video(tmp_path)
    else:
        audio_path = tmp_path

    st.write("猫語を解析中...")

    emotion, pitch, energy = analyze_cat_voice(audio_path)

    st.success("解析結果")

    st.write("🐈 感情:", emotion)
    st.write("声の高さ:", pitch)
    st.write("声の強さ:", energy)
