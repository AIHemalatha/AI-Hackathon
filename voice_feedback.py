import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
from playsound import playsound
import streamlit as st

def listen(lang='ta-IN'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language=lang)
        st.success(f"🗣️ You said: {text}")
        return text
    except Exception as e:
        st.error("❌ Could not recognize speech.")
        print(e)
        return ""

def speak_response(text, lang='en'):
    try:
        # Create temporary MP3 file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name

        # Generate speech
        tts = gTTS(text=text, lang=lang)
        tts.save(temp_path)

        # Play audio
        playsound(temp_path)

    except Exception as e:
        print("❌ Error in speak_response():", e)

    finally:
        # Cleanup
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                print(f"⚠️ Could not delete temp file: {e}")