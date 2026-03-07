from pydub import AudioSegment
import librosa
import tempfile

uploaded_file = st.file_uploader("猫の声をアップロード", type=["wav","mp3","m4a","mp4","mov"])

if uploaded_file:

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    audio = AudioSegment.from_file(tmp_path)
    wav_path = tmp_path + ".wav"
    audio.export(wav_path, format="wav")

    y, sr = librosa.load(wav_path, sr=None)