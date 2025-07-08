from gtts import gTTS
import os
import streamlit as st
import tempfile
import time
import pygame  # for audio playback
from playsound import playsound

def speak_response(text, lang='en'):
    try:
        # ✅ Use delete=False to keep file for gTTS and playsound
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name

        tts = gTTS(text=text, lang=lang)
        tts.save(temp_path)  # ✅ Save AFTER the file is closed

        playsound(temp_path)

    except Exception as e:
        print("❌ Error in speak_response():", e)

    finally:
        # ✅ Ensure cleanup
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                print(f"⚠️ Could not delete temp file: {e}")

