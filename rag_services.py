import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma

from langchain_rag_proper import GeminiEmbeddings


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


# --------------------------------------------------
# 2. Embedding model
# --------------------------------------------------

embedding_model = GeminiEmbeddings()


# --------------------------------------------------
# 3. Connect to existing ChromaDB
# --------------------------------------------------

vector_store = Chroma(
    collection_name="student_knowledge_langchain",
    embedding_function=embedding_model,
    persist_directory="./langchain_chroma_db"
)


# --------------------------------------------------
# 4. Create retriever
# --------------------------------------------------

retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}
)


# --------------------------------------------------
# 5. Create Gemini model
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)


# --------------------------------------------------
# 6. Create RAG prompt
# --------------------------------------------------

prompt = ChatPromptTemplate.from_template(
    """
You are an AI assistant for a Student Management System.

Answer the user's question using only the context provided below.

Context:
{context}

Question:
{question}

Instructions:
- Answer clearly and concisely.
- Do not invent information.
- If the answer is not present in the context,
  say that the information is not available.
"""
)


# --------------------------------------------------
# 7. Convert documents into text
# --------------------------------------------------

def format_documents(documents):
    return "\n\n".join(
        document.page_content
        for document in documents
    )


# --------------------------------------------------
# 8. RAG function
# --------------------------------------------------

def ask_rag(question: str) -> str:

    documents = retriever.invoke(question)

    context = format_documents(documents)

    formatted_prompt = prompt.format(
        context=context,
        question=question
    )

    response = llm.invoke(formatted_prompt)

    if isinstance(response.content, list):

        for item in response.content:

            if (
                isinstance(item, dict)
                and item.get("type") == "text"
            ):
                return item.get("text", "")

        return ""

    return response.content