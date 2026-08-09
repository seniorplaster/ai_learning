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

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

conversation = [
    SystemMessage(content="You are a helpful banking assistant."),
    HumanMessage(content="What is my account balance?"),
]

response_1 = llm.invoke(conversation)
print(response_1.content)

# Add the AI's reply AND the next question - this is how memory works
conversation.append(AIMessage(content=response_1.content))
conversation.append(HumanMessage(content="Can I increase my credit limit?"))

response_2 = llm.invoke(conversation)
print(response_2.content)