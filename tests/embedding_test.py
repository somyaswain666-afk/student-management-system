import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


text = "A student's GPA is measured on a scale from 0 to 10."

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text
)

print(response.embeddings[0].values[:10])
print("Embedding dimensions:", len(response.embeddings[0].values))