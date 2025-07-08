import streamlit as st
import torch
import torchaudio
import numpy as np
import librosa
import tempfile
from scipy.io.wavfile import write
import sounddevice as sd


# Load voice model
voice_model = torch.jit.load("emotion_detection/voice_modell.pt", map_location=torch.device('cpu'))
voice_model.eval()

# Emotion labels (edit if yours are different)
labels = ['neutral', 'happy', 'sad', 'angry', 'fearful']

def record_audio(duration=4, sr=16000):
    st.info("🎤 Recording voice... Speak now")
    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1)
    sd.wait()
    return audio.flatten(), sr

def extract_mfcc(audio, sr, max_len=100):
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    if mfcc.shape[1] < max_len:
        pad_width = max_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, pad_width=((0,0),(0,pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :max_len]
    return mfcc

def predict_voice_emotion_live():
    audio, sr = record_audio()
    audio = audio / np.max(np.abs(audio))  # normalize

    mfcc = extract_mfcc(audio, sr)  # shape (40, 100)

    # ✅ Fix: average across time to get 40 features
    mfcc_mean = np.mean(mfcc, axis=1)  # (40,)
    mfcc_tensor = torch.tensor(mfcc_mean, dtype=torch.float32).unsqueeze(0)  # (1, 40)

    with torch.no_grad():
        output = voice_model(mfcc_tensor)
        pred = torch.argmax(output, dim=1).item()

    return labels[pred]
