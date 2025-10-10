from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_response(user_message, mood):
    """Get an empathetic AI response based on mood and message"""
    prompt = f"""
    You are a kind, understanding student wellness assistant.
    The user feels {mood}. Respond with empathy, care, and reflection.

    User: {user_message}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"
