import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.title("🐈 猫翻訳AI")

fs = 44100
seconds = 3

if st.button("猫の声を録音する"):

    st.write("録音中...")

    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()

    write("cat_test.wav", fs, recording)

    st.success("録音完了")

    y, sr = librosa.load("cat_test.wav")

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

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