from pathlib import Path

from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# Read the document
text = Path("student_handbook.txt").read_text()


# Split document into chunks
chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]


# Create an embedding for every chunk
for i, chunk in enumerate(chunks, start=1):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )

    embedding = response.embeddings[0].values

    print(f"\nChunk {i}:")
    print(chunk)
    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")