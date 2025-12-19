import streamlit as st
import requests
import datetime

# -------------------------------
# 🌿 1. Setup
# -------------------------------
st.set_page_config(page_title="Student Wellness Chatbot", page_icon="🌱", layout="centered")

# -------------------------------
# 🔑 2. Gemini API Setup
# -------------------------------
GEMINI_API_KEY = "AIzaSyDt4Dm_F62DqHgIJiEaHyRwJv5EPc_VWYo"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# -------------------------------
# 💬 3. Function to Get Response
# -------------------------------
def get_gemini_response(user_input, mood):
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"You are a kind, empathetic wellness chatbot. "
                                f"The user feels {mood}. Respond empathetically to: {user_input}"
                    }
                ]
            }
        ]
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload)
        res.raise_for_status()
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ Error: {e}"

# -------------------------------
# 🧠 4. Session State
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []
if "mood" not in st.session_state:
    st.session_state.mood = "🙂 Normal"

# -------------------------------
# 🎭 5. Sidebar Navigation
# -------------------------------
st.sidebar.title("🌿 Navigation")
page = st.sidebar.radio("Go to:", ["💬 Chatbot", "📝 Personal Journal"])

st.sidebar.header("🧠 Mood Tracker")
mood = st.sidebar.radio(
    "How are you feeling today?",
    ["🙂 Normal", "😢 Sad", "😠 Angry", "😌 Calm", "😕 Upset", "😎 Cool"],
)
st.session_state.mood = mood
st.sidebar.markdown(f"**Selected Mood:** {mood}")

# -------------------------------
# 💬 6. Chatbot Page
# -------------------------------
if page == "💬 Chatbot":
    st.title("🌱Student Wellness Chatbot")
    st.markdown("Hey 👋 I'm here to listen and support you 🌸")

    user_input = st.text_area("🧑 What's on your mind?", placeholder="Type your feelings here...")

    if st.button("Send 💌"):
        if user_input.strip():
            with st.spinner("Thinking... 💭"):
                bot_reply = get_gemini_response(user_input, mood)
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", bot_reply))

    st.markdown("### 💬 Conversation History")
    for sender, msg in st.session_state.chat_history[-20:]:
        color = "rgba(173,216,230,0.2)" if sender == "You" else "rgba(255,215,0,0.15)"
        border = "#ADD8E6" if sender == "You" else "#FFD700"
        st.markdown(f"""
        <div style="text-align:{'right' if sender == 'You' else 'left'};
        background-color:{color}; padding:10px;
        border-radius:10px; margin:5px; border:1px solid {border};">
            <b>{sender}:</b> {msg}
        </div>
        """, unsafe_allow_html=True)

# -------------------------------
# 📝 7. Journal Page
# -------------------------------
elif page == "📝 Personal Journal":
    st.title("📝 Personal Journal")
    st.markdown("Reflect on your thoughts and track your journey 🌼")

    journal_entry = st.text_area("Write your reflection ✍️")

    if st.button("Save Entry 📚"):
        if journal_entry.strip():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.journal_entries.append((timestamp, journal_entry))
            st.success("Journal entry saved successfully 💾")

    if st.session_state.journal_entries:
        st.markdown("### 🗂️ Your Saved Entries")
        for i, (ts, entry) in enumerate(reversed(st.session_state.journal_entries), 1):
            st.markdown(f"""
            <div style="background-color:rgba(144,238,144,0.2); padding:10px;
            border-radius:8px; margin:8px 0; border:1px solid #90EE90;">
                <b>Entry {i} ({ts}):</b><br>{entry}
            </div>
            """, unsafe_allow_html=True)
