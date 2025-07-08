import sys
import streamlit as st
import os
import numpy as np
import pandas as pd
import cv2
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from tensorflow.keras.models import load_model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from chatbot.mental_chatbot import get_empathetic_reply
from chatbot.chatbot import get_empathetic_reply
from emotion_detection.face_live_stream import detect_live_face_emotion
from voice_stream import predict_voice_emotion_live
from voice_feedback import speak_response
from utils.logger import log_mood_entry
from utils.logger import check_sos_trigger


st.set_page_config(page_title="AI Mental Health Companion", layout="wide")
st.title("🧠 AI Mental Health Companion")
st.markdown("Helping you feel better — one moment at a time 💙")

# Sidebar for selecting mode
option = st.sidebar.radio("Select Mode", ["Text Chat", "Face Emotion", "Voice Emotion", "Breathing Exercise", "Mood Journal"])

    
# 💬 Text Chat
if option == "Text Chat":
    user_input = st.text_input("💬 How are you feeling today?", "")
    if user_input:
        result = get_empathetic_reply(user_input)
        log_mood_entry("text", user_input, result['mood'], result['score'])
        st.markdown(f"**🤖 Buddy:** {result['reply']}")
        st.markdown(f"**🧠 Detected Emotion:** `{result['mood'].capitalize()}`")

        if result['mood'] in ["sadness", "fear"]:
            st.video("https://youtu.be/ZWuzH0fW8l0?si=ISZHViwzveNN30d_")
            st.success("Try a calming song 💙")
        if result['mood'] in ["anger"]:
            st.video("https://www.youtube.com/live/eI6ISUNjnt4?si=rgXwo9IwEq6vTXbT")
            st.success("Try a calming song 💙")            
            
# 👁️ Live Face Emotion Detection
elif option == "Face Emotion":
    st.markdown("### 👁️ Live Webcam Emotion Detection")
    st.info("😊 Look at the camera — your emotions will be shown in real-time!")
    emotion = detect_live_face_emotion()
    st.markdown(f"**😶 Detected Emotion:** `{emotion}`")

# 🎙️ Voice Emotion Detection (Live)
elif option == "Voice Emotion":
    st.markdown("### 🎙️ Record and Detect Your Voice Emotion")
    lang = st.selectbox("🔤 Choose Voice Feedback Language", ["English", "Tamil"])
    lang_code = 'en' if lang == 'English' else 'ta'
    
    if st.button("🎙️ Record & Detect"):
        emotion = predict_voice_emotion_live()
        st.markdown(f"**🗣️ Detected Voice Emotion:** `{emotion}`")

        # Response message
        msg = {
            "sad": "I'm here for you. Try breathing deeply and know that things will get better.",
            "angry": "It’s okay to feel this way. Let’s take a moment to calm down.",
            "fearful": "You're safe. Try focusing on your breath and relax.",
            "happy": "I’m glad you're feeling happy! Keep smiling!",
            "neutral": "Thanks for checking in. How are you feeling now?"
        }.get(emotion, "You're doing great!")

        # 💬 Voice response
        speak_response(msg, lang=lang_code)

        # 🎥 Activity suggestion
        if emotion in ["sad", "angry", "fearful"]:
            st.video("https://youtu.be/3sCGysVB41k?si=EcXXHG5VJUG2XzdE")
            st.success("Try this calming song 💙")
            
elif option == "Breathing Exercise":
    st.markdown("### 🌬️ Guided Breathing Session")
    st.info("Let’s calm down with a simple 4-7-8 breathing technique.")

    st.video("https://youtu.be/j-1n3KJR1I8?si=Xu6muhU6rr7XJZ2_")
    st.markdown("✅ Inhale for 4 seconds\n✅ Hold for 7 seconds\n✅ Exhale for 8 seconds\n\nRepeat for a few cycles 💙")
    
elif option == "Mood Journal":
    st.markdown("### 📓 Your Mood Journal & Emotional Tracker")
    # Clear Mood Journal Button
    if st.button("🧹 Clear Mood Journal (Reset)", key="clear_mood"):
        try:
            with open("mood_journal.csv", "w") as f:
                f.write("timestamp,source,input,mood,score\n")  # Write required headers
            st.session_state["sos_shown"] = False
            st.success("✅ Mood journal cleared and header re-added.")
        except Exception as e:
            st.error(f"❌ Failed to clear journal: {e}")

    # Load and show the journal
    if os.path.exists("mood_journal.csv") and os.path.getsize("mood_journal.csv") > 0:
        try:
            df = pd.read_csv("mood_journal.csv", parse_dates=["timestamp"])
            st.subheader("📝 Recent Entries")
            st.dataframe(df.tail(10), use_container_width=True)
            
            # Plot mood trend
            df['day'] = df['timestamp'].dt.date
            mood_map = {'negative': -1, 'neutral': 0, 'positive': 1}
            df['mood_score'] = df['mood'].map(mood_map)

            mood_trend = df.groupby('day')['mood_score'].mean().reset_index()
            st.subheader("📈 Weekly Mood Trend")
            st.line_chart(mood_trend.rename(columns={"day": "index"}).set_index("index"))
            
        except ValueError as e:
            st.error(f"⚠️ Failed to load mood journal: {e}")
    else:
        st.info("📭 No mood entries yet. Try chatting or detecting an emotion first.")

# Initialize the session state flag once
if "sos_shown" not in st.session_state:
    st.session_state["sos_shown"] = False
    
# show alert if triggered 
if check_sos_trigger() and not st.session_state["sos_shown"]:
    st.error("🚨 You seem emotionally distressed. Please talk to someone you trust or seek professional help.")
    st.markdown("**📞 Emergency Help:** [Mental Health Helpline](https://www.who.int/campaigns/world-mental-health-day/2020/information-resources)")
    st.session_state["sos_shown"] = True

