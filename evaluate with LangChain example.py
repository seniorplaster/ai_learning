from langchain_core.prompts import ChatPromptTemplate

# A reusable template - the {placeholders} get filled in later
qm_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior Quality Management analyst with 20 years "
               "of contact center experience."),
    ("human", "Call summary: {transcript_summary}\n\n"
              "Give exactly one strength and one improvement area.")
])

# Fill the template and send it - notice you never wrote .format() or f-strings
chain = qm_prompt | llm   # the pipe | connects prompt output directly into the model
result = chain.invoke({"transcript_summary": "Agent resolved a billing dispute calmly."})
print(result.content)