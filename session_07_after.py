# session_07.py
# The LANGCHAIN approach - same result as session_07_before.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# This replaces the ask_gemini() function AND the client setup from File 1
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

try:
    response = llm.invoke("In one sentence, what is a contact center?")
    print(response.content)
except Exception as e:
    print(f"Error calling the model: {e}")