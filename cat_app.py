import streamlit as st
import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from moviepy.editor import VideoFileClip
import tempfile
import os

st.title("🐈 猫翻訳AI")

uploaded_file = st.file_uploader(
    "猫の鳴き声をアップロード",
    type=["wav","mp3","m4a","mov","mp4"]
)

if uploaded_file is not None:

    suffix = uploaded_file.name.split(".")[-1].lower()

    # 一時ファイル作成
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix="."+suffix)
    temp_file.write(uploaded_file.read())
    temp_file.close()

    audio_path = temp_file.name

    # 動画なら音声を抽出
    if suffix in ["mov","mp4"]:
        video = VideoFileClip(audio_path)
        audio_path = audio_path + ".wav"
        video.audio.write_audiofile(audio_path)

    try:
        y, sr = librosa.load(audio_path)

    except:
        st.error("音声の読み込みに失敗しました")
        st.stop()

    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    feature = np.mean(mfcc.T, axis=0)

    X = [
        feature,
        feature * 0.9,
        feature * 1.1,
        feature * 0.8,
        feature * 1.2
    ]

    y_labels = [
        "警戒",
        "お腹すいた",
        "甘え",
        "不満",
        "威嚇"
    ]

    model = RandomForestClassifier()
    model.fit(X, y_labels)

    prediction = model.predict([feature])

    messages = {
        "警戒":"🐈 何か警戒しています",
        "お腹すいた":"🐈 お腹が減っている可能性",
        "甘え":"🐈 甘えています",
        "不満":"🐈 少し不満がありそう",
        "威嚇":"🐈 威嚇しています"
    }

    st.subheader("猫の気持ち")
    st.success(messages[prediction[0]])