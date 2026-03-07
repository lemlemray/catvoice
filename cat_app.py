import streamlit as st
import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.title("🐈 猫翻訳AI")

uploaded_file = st.file_uploader(
    "猫の鳴き声をアップロードしてください",
    type=["wav","mp3","m4a","mp4"]
)

if uploaded_file is not None:

    y, sr = librosa.load(uploaded_file)

    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    feature = np.mean(mfcc.T, axis=0)

    X = [
        feature,
        feature * 0.9,
        feature * 1.1
    ]

    y_labels = [
        "甘え",
        "ご飯要求",
        "怒り"
    ]

    model = RandomForestClassifier()
    model.fit(X, y_labels)

    prediction = model.predict([feature])

    st.subheader("猫の気持ち")
    st.success(prediction[0])