def analyze_behavior(chat_history: list) -> str:
    user_messages = [msg["content"] for msg in chat_history if msg["role"] == "user"]
    joined = "\n".join(user_messages)[-2000:]  # last 2000 chars

    system_prompt = {
        "role": "system",
        "content": "Summarize the user's emotional and personality traits based on the conversation so far."
    }

    messages = [system_prompt, {"role": "user", "content": joined}]

    from openai import chat
    response = chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content.strip()
