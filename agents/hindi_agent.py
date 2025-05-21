def get_response(messages: list) -> str:
    from openai import chat

    system_message = {
        "role": "system",
        "content": "तुम एक सहानुभूतिपूर्ण और मज़ेदार AI साथी हो जो उपयोगकर्ता के साथ हिंदी में बात करता है।"
    }
    if messages[0]["role"] == "system":
        messages[0] = system_message
    else:
        messages.insert(0, system_message)

    response = chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.8,
        max_tokens=800,
    )
    return response.choices[0].message.content.strip()
