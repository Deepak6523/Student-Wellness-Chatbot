import pandas as pd
from datetime import datetime
import os

DATA_DIR = "data"
JOURNAL_PATH = os.path.join(DATA_DIR, "journal_entries.csv")
MOOD_PATH = os.path.join(DATA_DIR, "mood_log.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# --- Journal Management ---
def save_journal_entry(text):
    entry = pd.DataFrame([{
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "text": text
    }])
    if os.path.exists(JOURNAL_PATH):
        old = pd.read_csv(JOURNAL_PATH)
        entry = pd.concat([old, entry], ignore_index=True)
    entry.to_csv(JOURNAL_PATH, index=False)

def load_journal_entries():
    if os.path.exists(JOURNAL_PATH):
        return pd.read_csv(JOURNAL_PATH).to_dict("records")
    return []

# --- Mood Management ---
def save_mood(mood):
    entry = pd.DataFrame([{
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mood": mood
    }])
    if os.path.exists(MOOD_PATH):
        old = pd.read_csv(MOOD_PATH)
        entry = pd.concat([old, entry], ignore_index=True)
    entry.to_csv(MOOD_PATH, index=False)

def load_mood_log():
    if os.path.exists(MOOD_PATH):
        return pd.read_csv(MOOD_PATH)
    return pd.DataFrame(columns=["date", "mood"])
