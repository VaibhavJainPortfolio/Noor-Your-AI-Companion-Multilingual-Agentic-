import os
import json
from typing import List, Dict

MEMORY_DIR = "data/user_sessions"
os.makedirs(MEMORY_DIR, exist_ok=True)

def get_user_filepath(user_id: str) -> str:
    return os.path.join(MEMORY_DIR, f"{user_id}.json")

def save_conversation(user_id: str, messages: List[Dict]):
    """
    Save the conversation history to a file.
    """
    filepath = get_user_filepath(user_id)
    with open(filepath, 'w') as f:
        json.dump(messages, f, indent=2)

def load_conversation(user_id: str) -> List[Dict]:
    """
    Load the user's conversation history from file.
    """
    filepath = get_user_filepath(user_id)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def append_to_conversation(user_id: str, message: Dict):
    """
    Append a new message to the user's history.
    """
    history = load_conversation(user_id)
    history.append(message)
    save_conversation(user_id, history)

def summarize_conversation(messages: List[Dict]) -> str:
    """
    (Optional) Summarize the user's personality traits from messages.
    You can expand this using GPT or heuristics.
    """
    user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
    summary = "User seems emotionally expressive and seeks a companion for comfort."
    if any("sad" in m.lower() or "alone" in m.lower() for m in user_messages):
        summary += " They might be dealing with loneliness or sadness."
    if any("happy" in m.lower() or "grateful" in m.lower() for m in user_messages):
        summary += " They also show signs of emotional awareness and positivity."
    return summary
