import streamlit as st
import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.title("🐈 猫翻訳AI")

st.write("猫の鳴き声をアップロードしてください")

uploaded_file = st.file_uploader(
    "猫の鳴き声ファイル",
    type=["wav","mp3","m4a"]
)

if uploaded_file is not None:

    y, sr = librosa.load(uploaded_file)

    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    feature = np.mean(mfcc.T, axis=0)

    # 仮の学習データ（簡易AI）
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