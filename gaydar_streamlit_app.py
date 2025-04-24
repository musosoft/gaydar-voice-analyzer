
import streamlit as st
import librosa
import numpy as np
import soundfile as sf
import joblib

# Load the trained model
model = joblib.load("gaydar_model.pkl")

st.title("🏳️‍🌈 Gaydar Voice Analyzer (Demo)")
st.markdown("Upload a short **WAV** file (3–5 seconds) of your voice to see how your vocal features are interpreted by our model.")

uploaded_file = st.file_uploader("🎙️ Upload your voice recording (.wav only)", type=["wav"])

if uploaded_file is not None:
    try:
        # Read audio
        y, sr = sf.read(uploaded_file)
        if len(y.shape) > 1:
            y = y[:, 0]  # Mono only

        # Extract features
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        meanf0 = np.mean(librosa.yin(y, fmin=50, fmax=300, sr=sr))
        f0sd = np.std(librosa.yin(y, fmin=50, fmax=300, sr=sr))
        jitter = np.std(np.diff(librosa.zero_crossings(y, pad=False)))
        hnr = np.mean(librosa.feature.rms(y=y))

        features = np.array([[meanf0, f0sd, jitter, hnr]])

        # Predict
        pred = model.predict_proba(features)[0]
        gay_prob = round(pred[1] * 100, 2)
        straight_prob = round(pred[0] * 100, 2)

        # Show results
        st.subheader("🔮 Result")
        st.write(f"**💖 Gay Probability:** {gay_prob}%")
        st.write(f"**🧔 Straight Probability:** {straight_prob}%")

        if gay_prob > 75:
            st.success("🌈 Strong gay energy detected!")
        elif straight_prob > 75:
            st.info("🧔 Mostly straight vocal vibes.")
        else:
            st.warning("🎭 Ambiguous or neutral vocal tone.")
    except Exception as e:
        st.error(f"⚠️ Error processing audio: {e}")
