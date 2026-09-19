import os

import chromadb
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_collection(
    name="student_knowledge"
)


# User question
question = "What information is required during enrollment?"


# Convert question into an embedding
response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question
)

question_embedding = response.embeddings[0].values


# Retrieve relevant chunks
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=2
)


# Combine retrieved chunks
retrieved_text = "\n\n".join(
    results["documents"][0]
)


# Give the retrieved information to Gemini
prompt = f"""
You are an AI assistant for a Student Management System.

Answer the user's question using only the information provided
in the retrieved knowledge.

Retrieved Knowledge:
{retrieved_text}

User Question:
{question}

Instructions:
- Answer clearly and concisely.
- Do not invent information.
- If the retrieved knowledge does not contain the answer,
  say that the information is not available.
"""

answer_response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)


print("\nQuestion:")
print(question)

print("\nRetrieved Knowledge:")
print(retrieved_text)

print("\nFinal Answer:")
print(answer_response.text)