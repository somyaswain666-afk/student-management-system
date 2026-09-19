import os

from dotenv import load_dotenv
from google import genai

from langchain_core.documents import Document
from langchain_chroma import Chroma


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


# Google Gemini client
client = genai.Client(api_key=api_key)


# Read our knowledge document
with open("student_handbook.txt", "r") as file:
    text = file.read()


# Split into simple chunks
chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]


# Convert text chunks into LangChain Documents
documents = [
    Document(page_content=chunk)
    for chunk in chunks
]


# Generate embeddings
embeddings = []

for document in documents:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=document.page_content
    )

    embeddings.append(response.embeddings[0].values)


# Create Chroma vector store
vector_store = Chroma(
    collection_name="langchain_student_knowledge",
    embedding_function=None,
    persist_directory="./langchain_chroma_db"
)


# Store documents and their embeddings
vector_store._collection.add(
    ids=[f"chunk_{i}" for i in range(len(documents))],
    documents=[doc.page_content for doc in documents],
    embeddings=embeddings
)


# User question
question = "What is the GPA scale?"


# Create question embedding
response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question
)

question_embedding = response.embeddings[0].values


# Retrieve relevant documents
results = vector_store._collection.query(
    query_embeddings=[question_embedding],
    n_results=2
)


retrieved_text = "\n\n".join(
    results["documents"][0]
)


# Ask Gemini using retrieved information
prompt = f"""
You are an AI assistant for a Student Management System.

Use only the retrieved knowledge below to answer the question.

Retrieved Knowledge:
{retrieved_text}

Question:
{question}

Do not invent information.
"""

answer = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)


print("\nQuestion:")
print(question)

print("\nRetrieved Information:")
print(retrieved_text)

print("\nFinal Answer:")
print(answer.text)