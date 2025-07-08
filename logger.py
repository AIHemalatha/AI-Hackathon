import os
import pandas as pd
from datetime import datetime, timedelta

MOOD_LOG_PATH = "mood_journal.csv"

def log_mood_entry(source, user_input, mood, score):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,  # "text", "face", "voice"
        "input": user_input,
        "mood": mood,
        "score": round(score, 2)
    }

    df = pd.DataFrame([entry])
    # Append to CSV file
    file_path = "mood_journal.csv"
    header_needed = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
    df.to_csv(file_path, mode='a', header=header_needed, index=False)
    
def check_sos_trigger():
    # 🛡️ Check if file exists and is not empty
    if not os.path.exists(MOOD_LOG_PATH) or os.path.getsize(MOOD_LOG_PATH) == 0:
        return False

    try:
        df = pd.read_csv(MOOD_LOG_PATH)
        if 'timestamp' not in df.columns:
            return False
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    except pd.errors.EmptyDataError:
        return False

    # Optional: filter by last 30 minutes
    recent_time = datetime.now() - timedelta(minutes=30)
    recent_df = df[df['timestamp'] >= recent_time]
    # ✅ Filter moods that are considered distress signals
    distress_moods = ['sadness', 'anger', 'fear']
    distress = recent_df[recent_df['mood'].isin(distress_moods)]
    return len(distress) >= 2   # trigger if 2+ are negative