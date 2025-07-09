# 🧠 AI Mental Health Companion
A Streamlit-based AI-powered mental health companion that detects user emotions from **face**, **voice**, and **text**, and provides **empathetic replies**, **soothing voice feedback**, and **breathing suggestions**.

## 🌟 Features
- 🎭 **Face Emotion Detection** (via webcam)
- 🎙️ **Voice Emotion Detection** (via microphone)
- 💬 **Text Emotion Chatbot** with empathetic replies
- 🔊 **Multilingual Voice Feedback** (English & Tamil)
- 📈 Mood Score with Confidence
- 🎧 Relaxing music & breathing exercises
- 📓 Mood Journal & Trends 

## 🖥️ Run the App Locally
### 1. Clone the repository
git clone https://github.com/your-username/mental-health-companion.git
cd mental-health-companion

2. Create and activate environment
conda create -n new-env python=3.10 -y
conda activate new-env

3. Install dependencies
pip install -r requirements.txt

4. Run the Streamlit app
streamlit run main_app.py
App runs at: http://localhost:8502

📁 Project Structure
mental-health-companion/
│
├── main_app.py                    # Streamlit app entry point
├── face_live_stream.py            # Facial emotion recognition logic
├── voice_stream.py                # Voice emotion analysis (MFCC + model)
├── chatbot.py                     # Emotion-aware text chatbot
├── voice_feedback.py              # Multilingual voice response (gTTS)
├── logger.py                      # Mood Journal ana SOS trigger
├── face_model.hdf5                # Pretrained face emotion model
├── voice_modell.pt                # Pretrained voice emotion model
└── requirements.txt
   
🤖 Models Used
Text Emotion: j-hartmann/emotion-english-distilroberta-base
Face Emotion: Mini-XCEPTION (custom or from oarriaga repo)
Voice Emotion: Custom PyTorch model trained on MFCC features

🌐 Multilingual Support
Currently supports:
English
Tamil (via gTTS)

💡 Future Enhancements
SOS Alert Button
Color-based Breathing Game for Kids
Uplifting Music Recommendations
Mobile App with Notifications

📜 License
This project is licensed under the MIT License.
