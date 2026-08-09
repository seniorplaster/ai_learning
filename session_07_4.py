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

from pydantic import BaseModel, Field

# Define the EXACT shape you want - this replaces writing a JSON schema as prompt text
class QMAnalysis(BaseModel):
    strength: str = Field(description="One short bullet, under 15 words")
    improvement: str = Field(description="One short bullet, under 15 words")
    risk_flag: str = Field(description='Exactly one of: "Compliance Risk", "Churn Risk", "None"')

# Wrap your model so its output ALWAYS matches QMAnalysis - guaranteed, not requested
structured_llm = llm.with_structured_output(QMAnalysis)

result = structured_llm.invoke(
    "Call summary: Customer reported unauthorized transaction. Agent took 8 "
    "minutes to locate it, asked customer to repeat details twice, gave no "
    "interim resolution timeline."
)

print(result.strength)     # direct attribute access - no json.loads(), no .get()
print(result.improvement)
print(result.risk_flag)


qm_chain = qm_prompt | structured_llm   # prompt template → guaranteed-structured model

result = qm_chain.invoke({
    "transcript_summary": "Customer asked about credit limit increase. Agent "
                           "verified identity, explained criteria, submitted request."
})

print(f"Strength: {result.strength}")
print(f"Improvement: {result.improvement}")
print(f"Risk: {result.risk_flag}")