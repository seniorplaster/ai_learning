# session_07_before.py
# The RAW API approach - everything LangChain will replace in File 2

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_gemini(question):
    """Sends a question to Gemini and returns the text response."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful contact center expert."
        )
    )
    return response.text


# Call it
answer = ask_gemini("In one sentence, what is a contact center?")
print(answer)