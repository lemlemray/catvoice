import streamlit as st
import librosa
import numpy as np
import tempfile
import random
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
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)

    return audio_path


def analyze_cat_voice(audio_path):

    y, sr = librosa.load(audio_path)

    pitch = np.mean(librosa.yin(y, fmin=50, fmax=500))
    energy = np.mean(librosa.feature.rms(y=y))

    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13))

    score = pitch * 0.4 + energy * 100 + mfcc * 2

    if score > 220:
        emotion = "甘え（かまって）"
    elif score > 160:
        emotion = "要求（なにか欲しい）"
    else:
        emotion = "落ち着いている"

    return emotion, pitch, energy


def translate_cat(emotion, pitch, energy):

    if "甘え" in emotion:

        phrases = [
            "ねえ、こっち来てよ",
            "撫でてほしいんだけど",
            "見てる？ぼくのこと",
            "かまってくれないと拗ねるよ"
        ]

    elif "要求" in emotion:

        phrases = [
            "ごはんまだ？",
            "ドア開けて",
            "トイレ掃除してほしい",
            "今すぐ来て"
        ]

    else:

        phrases = [
            "今日は悪くない日",
            "ここ居心地いい",
            "特に用はないけど鳴いただけ",
            "のんびりしてる"
        ]

    return random.choice(phrases)


if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(delete=False) as tmp:

        tmp.write(uploaded_file.read())
        tmp_path = tmp.name


    if uploaded_file.type.startswith("video"):

        st.write("🎥 動画から音声抽出中...")
        audio_path = extract_audio_from_video(tmp_path)

    else:

        audio_path = tmp_path


    st.write("🧠 猫語を解析中...")


    emotion, pitch, energy = analyze_cat_voice(audio_path)

    translation = translate_cat(emotion, pitch, energy)


    st.success("解析結果")


    st.write("🐈 感情:", emotion)

    st.write("声の高さ:", round(pitch,2))

    st.write("声の強さ:", round(energy,4))

    st.write("💬 猫語翻訳:", translation)
