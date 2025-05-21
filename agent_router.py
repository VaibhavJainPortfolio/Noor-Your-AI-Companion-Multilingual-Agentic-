from agents.english_agent import get_response as english_bot
from agents.hindi_agent import get_response as hindi_bot
from agents.behavior_analyzer import analyze_behavior

def route(language: str, messages: list):
    if language.lower() == "hindi":
        return hindi_bot(messages)
    else:
        return english_bot(messages)

def get_behavior_summary(history: list):
    return analyze_behavior(history)
