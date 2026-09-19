from pathlib import Path

import chromadb
from dotenv import load_dotenv
from google import genai
import os


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# Create a local ChromaDB database
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)


# Create a collection
collection = chroma_client.get_or_create_collection(
    name="student_knowledge"
)


# Read the document
text = Path("student_handbook.txt").read_text()


# Split into chunks
chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]


# Generate embeddings and store them
for i, chunk in enumerate(chunks):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )

    embedding = response.embeddings[0].values

    collection.add(
        ids=[f"chunk_{i}"],
        documents=[chunk],
        embeddings=[embedding]
    )


print("Stored chunks:", collection.count())