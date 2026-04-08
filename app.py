import streamlit as st
import os
from groq import Groq
from datetime import datetime

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Student Wellness Chatbot",
    page_icon="🌱",
    layout="centered"
)

# --------------------------------------------------
# Load API Key
# --------------------------------------------------
API_KEY = None
try:
    API_KEY = "6ce7c922-98a1-40bd-8b32-327c7427dccc"
except Exception:
    API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    st.error("GROQ_API_KEY not found")
    st.stop()

client = Groq(api_key=API_KEY)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🌱 Navigation")

    page = st.radio(
        "Go to:",
        ["💬 Chatbot", "📓 Personal Journal"]
    )

    st.markdown("---")
    st.markdown("## 🧠 Mood Tracker")

    mood = st.radio(
        "How are you feeling today?",
        ["😊 Normal", "😔 Sad", "😡 Angry", "😌 Calm", "😟 Upset", "😎 Cool"]
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

# --------------------------------------------------
# CHATBOT PAGE (MATCHES YOUR DESIGN)
# --------------------------------------------------
if page == "💬 Chatbot":

    st.markdown("# 🌱 Student Wellness Chatbot")
    st.markdown("### Hey 👋 I'm here to listen and support you 🌸")
    st.markdown("🧑‍🎓 **What's on your mind?**")

    user_input = st.text_area(
        "",
        placeholder="Type your feelings here...",
        height=150
    )

    if st.button("Send ❤️"):
        if user_input.strip():
            SYSTEM_PROMPT = (
                "You are a kind, empathetic student wellness chatbot. "
                f"The student is feeling {mood}. "
                "Provide emotional support. Do NOT give medical advice."
            )

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                reply = response.choices[0].message.content
            except Exception:
                reply = "Sorry, something went wrong. Please try again."

            st.session_state.chat_history.append({
                "user": user_input,
                "bot": reply
            })

        else:
            st.warning("Please type something before sending.")

    st.markdown("---")
    st.markdown("## 💬 Conversation History")

    if not st.session_state.chat_history:
        st.info("No messages yet. Start the conversation 💚")
    else:
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"**🙂 You:** {chat['user']}")
            st.markdown(f"**🤖 Bot:** {chat['bot']}")
            st.markdown("---")

# --------------------------------------------------
# PERSONAL JOURNAL PAGE
# --------------------------------------------------
if page == "📓 Personal Journal":

    st.markdown("# 📓 Personal Journal")
    st.markdown("Reflect on your thoughts and track your journey 🌻")

    journal_text = st.text_area(
        "Write your reflection ✍️",
        height=180,
        placeholder="Write how you're feeling today..."
    )

    if st.button("💾 Save Entry"):
        if journal_text.strip():
            st.session_state.journal_entries.append({
                "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "mood": mood,
                "text": journal_text
            })
            st.success("Journal entry saved 💚")
        else:
            st.warning("Please write something before saving.")

    st.markdown("---")
    st.markdown("## 📖 Your Past Entries")

    if not st.session_state.journal_entries:
        st.info("No journal entries yet.")
    else:
        for entry in reversed(st.session_state.journal_entries):
            with st.expander(f"🗓 {entry['date']} — {entry['mood']}"):
                st.write(entry["text"])
