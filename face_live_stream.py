import cv2
import numpy as np
import os
import time
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "face_model.hdf5")
cascade_path = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

model = load_model(model_path)
face_cascade = cv2.CascadeClassifier(cascade_path)

class EmotionDetector(VideoTransformerBase):
    def __init__(self):
        self.last_emotion = "Neutral"
        
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y + h, x:x + w]
            roi = cv2.resize(roi, (64, 64))
            if np.sum(roi) != 0:
                roi = roi.astype("float") / 255.0
                roi = np.expand_dims(roi, axis=0)
                roi = np.expand_dims(roi, axis=-1)

                prediction = model.predict(roi, verbose=0)[0]
                label = emotion_labels[np.argmax(prediction)]
                self.last_emotion = label

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        return img

def detect_live_face_emotion():
    
    st.markdown("## 😶 Live Face Emotion Detection")
    emotion_placeholder = st.empty()
    suggestion_placeholder = st.empty()

    ctx = webrtc_streamer(
        key="emotion-detection",
        mode=WebRtcMode.SENDRECV,
        video_transformer_factory=EmotionDetector,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    while ctx.video_transformer:
        emotion = ctx.video_transformer.last_emotion
        emotion_placeholder.markdown(f"**🧠 Detected Emotion: {emotion}**")
        # Clear previous suggestion block
        suggestion_placeholder.empty()
        # Suggestions based on emotion
        with suggestion_placeholder.container():
            if emotion in ["Sad", "Angry", "Fear"]:
                st.video("https://www.youtube.com/watch?v=2OEL4P1Rz04")
                st.info("Take a deep breath 💙 Try this calming video or a breathing exercise.")
            elif emotion == "Happy":
                st.success("You seem happy! Keep shining 🌟 Want to hear some uplifting music?")
                st.video("https://www.youtube.com/watch?v=ZbZSe6N_BXs")
            elif emotion == "Surprise":
                st.info("Surprised? Try focusing your energy into something creative or playful 🎨")
            elif emotion == "Neutral":
                st.markdown("You're calm. Want to try a quick mindfulness session?")

        time.sleep(2)  # refresh every 2 seconds
