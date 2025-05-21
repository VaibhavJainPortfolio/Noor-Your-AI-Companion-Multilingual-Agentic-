def get_response(messages: list) -> str:
    from openai import chat

    response = chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.8,
        max_tokens=800,
    )
    return response.choices[0].message.content.strip()
