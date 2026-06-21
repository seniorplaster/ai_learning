import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# New SDK uses a client object - similar to Anthropic pattern
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Generate content with system instruction
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=(
        "In exactly 3 bullet points, list the 3 most important things "
        "an AI tool must do to be useful in a contact center environment. "
        "Keep each bullet under 20 words."
    ),
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are a senior CCaaS implementation engineer with 20 years "
            "of experience delivering enterprise contact center projects "
            "across the GCC region. Be precise, professional, and concise."
        )
    )
)

# Extract the text - same as before
print(response.text)