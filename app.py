import streamlit as st
import openai
import os
from dotenv import load_dotenv

from agent_router import route, get_behavior_summary
from database import init_db
from memory_store import load_conversation, save_conversation

# Load environment variables
load_dotenv()

# Initialize DB
init_db()

# Streamlit setup
st.set_page_config(page_title="Noor - AI Companion", layout="wide")
st.title("💗 Noor – Your AI Companion (Multilingual & Agentic)")

# Sidebar Inputs
st.sidebar.title("🧠 Companion Settings")

api_key = st.sidebar.text_input("🔐 OpenAI API Key", type="password")
email = st.sidebar.text_input("📧 Email ID (used as unique ID)")
user_name = st.sidebar.text_input("👤 Your Name")
age = st.sidebar.number_input("🎂 Age", min_value=10, max_value=100, step=1)
gender = st.sidebar.selectbox("🧑 Gender", ["Prefer not to say", "Male", "Female", "Other"])
mood = st.sidebar.selectbox("🧘 Current Mood", ["Happy", "Sad", "Anxious", "Lonely", "Angry", "Neutral"])
feeling = st.sidebar.text_area("💬 How are you feeling?")
topic = st.sidebar.text_input("🎯 Topic to talk about")
language = st.sidebar.selectbox("🗣️ Language", ["English", "Hindi"])
naughty_mode = st.sidebar.checkbox("😈 Enable Naughty Mode", value=False)

if api_key:
    openai.api_key = api_key

if st.sidebar.button("Start Conversation") and email:
    st.session_state["email"] = email
    st.session_state["language"] = language
    st.session_state["messages"] = []

    # Load past memory
    history = load_conversation(email)
    summary = get_behavior_summary(history) if history else None

    system_intro = (
        f"You are Noor, an emotionally intelligent AI Companion. "
        f"The user’s name is {user_name}, age {age}, gender {gender}. "
        f"They are currently feeling '{mood}' and said: '{feeling}'. "
        f"Topic: {topic}.\n\n"
        f"Summary of past behavior: {summary if summary else 'No prior context.'}"
    )
    if naughty_mode:
        system_intro += "\nBe slightly flirtatious, charming, and witty — while remaining emotionally respectful."

    st.session_state["messages"].append({"role": "system", "content": system_intro})
    if history:
        st.session_state["messages"] += history
    else:
        st.session_state["messages"].append({"role": "user", "content": feeling or f"I want to talk about {topic}."})

    st.session_state["chat_started"] = True

# Main Chat Interface
if st.session_state.get("chat_started", False):
    messages = st.session_state["messages"]

    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"**🧍 You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**🤖 Noor:** {msg['content']}")

    user_input = st.text_input("💬 Your Message", key="input")
    if st.button("Send"):
        messages.append({"role": "user", "content": user_input})

        try:
            response = route(st.session_state["language"], messages)
            messages.append({"role": "assistant", "content": response})
            save_conversation(st.session_state["email"], messages)
        except Exception as e:
            st.error(f"❌ Error: {e}")

        st.rerun()

else:
    st.info("Please fill in your details and click 'Start Conversation' in the sidebar.")
