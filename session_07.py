import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# This replaces your entire ask_gemini() function from Session 3
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

response = llm.invoke("In one sentence, what is a contact center?")
print(response.content)

