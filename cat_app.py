import streamlit as st
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf
from moviepy.editor import VideoFileClip
import tempfile
import os

st.title("🐈 猫翻訳AI")

uploaded_file = st.file_uploader(
    "猫の声をアップロード",
    type=["wav","mp3","mp4","mov"]
)

def extract_audio_from_video(video_file):
    tmp_video = tempfile.NamedTemporaryFile(delete=False)
    tmp_video.write(video_file.read())

    clip = VideoFileClip(tmp_video.name)

    tmp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)

    clip.audio.write_audiofile(tmp_audio.name)

    return tmp_audio.name


def analyze_cat_voice(audio_path):

    y, sr = librosa.load(audio_path)

    duration = librosa.get_duration(y=y, sr=sr)

    pitch = np.mean(librosa.yin(y, fmin=50, fmax=1000))

    energy = np.mean(librosa.feature.rms(y=y))

    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr))

    return duration, pitch, energy, mfcc, y, sr


def cat_translate(pitch, energy):

    if pitch > 500 and energy > 0.05:
        return "ごはん！ごはん！"
    elif pitch > 400:
        return "かまってほしい"
    elif energy < 0.02:
        return "眠い…"
    elif pitch < 250:
        return "警戒している"
    else:
        return "なんとなく話してる"


if uploaded_file:

    st.audio(uploaded_file)

    file_type = uploaded_file.name.split(".")[-1]

    if file_type in ["mp4","mov"]:
        audio_path = extract_audio_from_video(uploaded_file)
    else:
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

    duration, pitch, energy, mfcc, y, sr = analyze_cat_voice(audio_path)

    st.write("### 解析結果")

    st.write("鳴き声の長さ:", duration)
    st.write("平均ピッチ:", pitch)
    st.write("音量:", energy)

    translation = cat_translate(pitch, energy)

    st.write("### 猫翻訳")

    st.success(translation)

    fig, ax = plt.subplots()

    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

    img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', ax=ax)

    plt.colorbar(img, ax=ax, format="%+2.f dB")

    st.pyplot(fig)