import streamlit as st
import datetime
from openai import OpenAI

# -------------------------------
# 🌿 Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Student Wellness Chatbot",
    page_icon="🌱",
    layout="centered"
)

# -------------------------------
# 🔑 OpenAI Setup
# -------------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY not found in Streamlit secrets")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

MODEL = "gpt-4o-mini"  # fast, cheap, best for chatbots

# -------------------------------
# 💬 ChatGPT Response Function
# -------------------------------
def get_chatgpt_response(user_input, mood):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a kind, empathetic student wellness chatbot. "
                        "Listen carefully, validate emotions, and give gentle support. "
                        "Do NOT give medical or clinical diagnoses."
                    )
                },
                {
                    "role": "user",
                    "content": f"My mood is {mood}. {user_input}"
                }
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error communicating with ChatGPT: {e}"

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
# 🎭 Sidebar Navigation
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
    st.title("🌱 Student Wellness Chatbot")
    st.markdown("Hey 👋 I'm here to listen and support you 🌸")

    user_input = st.text_area(
        "🧑 What's on your mind?",
        placeholder="Type your feelings here..."
    )

    if st.button("Send 💌"):
        if user_input.strip():
            with st.spinner("Thinking... 💭"):
                reply = get_chatgpt_response(user_input, mood)
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", reply))
        else:
            st.warning("Please type something 💭")

    st.markdown("### 💬 Conversation History")
    for sender, msg in st.session_state.chat_history[-20:]:
        st.markdown(f"**{sender}:** {msg}")

# -------------------------------
# 📝 Personal Journal Page
# -------------------------------
elif page == "📝 Personal Journal":
    st.title("📝 Personal Journal")
    st.markdown("Reflect on your thoughts and track your journey 🌼")

    journal_entry = st.text_area("Write your reflection ✍️")

    if st.button("Save Entry 📚") and journal_entry.strip():
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.journal_entries.append((timestamp, journal_entry))
        st.success("Journal entry saved 💾")

    if st.session_state.journal_entries:
        st.markdown("### 🗂️ Your Saved Entries")
        for ts, entry in reversed(st.session_state.journal_entries):
            st.markdown(f"**{ts}:** {entry}")
