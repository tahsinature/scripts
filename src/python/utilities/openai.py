from typing import Any, Literal, Optional
import openai
import os


client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_gpt_3_with_chat_completions(system_message: str, user_message: str, response_type: Optional[Literal["json", "text"]] = None):
    rf: Any = openai._types.NOT_GIVEN

    if response_type == "json":
        rf = {"type": "json_object"}
    elif response_type == "text":
        rf = {"type": "text"}

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format=rf,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return e
