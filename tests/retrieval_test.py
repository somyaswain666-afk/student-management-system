import os

import chromadb
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# Connect to our existing ChromaDB
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_collection(
    name="student_knowledge"
)


# User's question
question = "What is the GPA scale?"


# Convert the question into an embedding
response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question
)

question_embedding = response.embeddings[0].values


# Search ChromaDB
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=2
)


# Display the retrieved chunks
print("\nQuestion:")
print(question)

print("\nRetrieved chunks:")

for i, document in enumerate(results["documents"][0], start=1):
    print(f"\n--- Result {i} ---")
    print(document)