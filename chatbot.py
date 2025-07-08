from transformers import pipeline

# Load emotion classification model
emotion_classifier = pipeline("text-classification", 
                              model="j-hartmann/emotion-english-distilroberta-base", 
                              return_all_scores=False)

# Emotion-based empathetic replies
emotion_responses = {
    "joy": "I'm so glad you're feeling joyful! Keep shining 🌟",
    "love": "You’re surrounded by love and care 💖 Keep spreading it!",
    "anger": "It’s okay to feel angry sometimes. Want to try a calming activity? 💆",
    "sadness": "I'm really sorry you're feeling this way. You're not alone 🫂",
    "fear": "That sounds scary. Let's breathe together for a moment 🧘",
    "surprise": "Wow, sounds unexpected! Want to talk more about it?",
    "neutral": "Thanks for sharing. I'm here to support you 🤗"
}

def get_empathetic_reply(user_input):
    result = emotion_classifier(user_input)[0]
    emotion = result['label'].lower()
    score = round(result['score'], 2)

    reply = emotion_responses.get(emotion, emotion_responses['neutral'])

    return {
        "reply": reply,
        "score": score,
        "mood": emotion
    }
