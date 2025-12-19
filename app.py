import streamlit as st
import requests
import datetime

# -------------------------------
# 🌿 Setup
# -------------------------------
st.set_page_config(
    page_title="Student Wellness Chatbot",
    page_icon="🌱",
    layout="centered"
)

# -------------------------------
# 🔑 Gemini API Setup (FREE MODEL)
# -------------------------------
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ GEMINI_API_KEY not found in Streamlit secrets")
    st.stop()

API_KEY = "AIzaSyDt4Dm_F62DqHgIJiEaHyRwJv5EPc_VWYo"
MODEL = "models/gemini-1.5-flash"

API_URL = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent"

# -------------------------------
# 💬 Gemini Response Function
# -------------------------------
def get_gemini_response(user_input, mood):
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "You are a kind, empathetic student wellness chatbot. "
                            "Listen carefully and respond with emotional support. "
                            "Do not give medical advice.\n\n"
                            f"User mood: {mood}\n"
                            f"Message: {user_input}"
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 256
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"⚠️ Gemini Error {response.status_code}:\n{response.text}"

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

# -------------------------------
# 🧠 Session State
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []
if "mood" not in st.session_state:
    st.session_state.mood = "🙂 Normal"

# -------------------------------
# 🎭 Sidebar
# -------------------------------
st.sidebar.title("🌿 Navigation")
page = st.sidebar.radio("Go to:", ["💬 Chatbot", "📝 Personal Journal"])

st.sidebar.header("🧠 Mood Tracker")
mood = st.sidebar.radio(
    "How are you feeling today?",
    ["🙂 Normal", "😢 Sad", "😠 Angry", "😌 Calm", "😕 Upset", "😎 Cool"]
)
st.session_state.mood = mood

# -------------------------------
# 💬 Chatbot Page
# -------------------------------
if page == "💬 Chatbot":
    st.title("🌱 Student Wellness Chatbot (Gemini 1.5 Flash)")
    st.markdown("Hey 👋 I'm here to listen and support you 🌸")

    user_input = st.text_area("🧑 What's on your mind?")

    if st.button("Send 💌"):
        if user_input.strip():
            with st.spinner("Thinking... 💭"):
                reply = get_gemini_response(user_input, mood)
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", reply))
        else:
            st.warning("Please type something 💭")

    st.markdown("### 💬 Conversation History")
    for sender, msg in st.session_state.chat_history[-20:]:
        st.markdown(f"**{sender}:** {msg}")

# -------------------------------
# 📝 Journal Page
# -------------------------------
elif page == "📝 Personal Journal":
    st.title("📝 Personal Journal")
    journal_entry = st.text_area("Write your reflection ✍️")

    if st.button("Save Entry 📚") and journal_entry.strip():
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.journal_entries.append((ts, journal_entry))
        st.success("Journal entry saved 💾")

    for ts, entry in reversed(st.session_state.journal_entries):
        st.markdown(f"**{ts}:** {entry}")
