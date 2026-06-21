import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=(
        "In exactly 3 bullet points, list the 3 most important things"
        "and AI tool must do to be usefule in a contact center environment"
        ),
    config=types.GenerateContentConfig(
        system_instruction=(
            "you are a senior CCaaS Impelemtation engineer with 20 years"
            "of experience in delivery enterpruse contact center projects."
        )
    )
)
print(response.text)