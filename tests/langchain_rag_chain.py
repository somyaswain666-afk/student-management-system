import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma

from langchain_rag_proper import GeminiEmbeddings


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


# --------------------------------------------------
# 1. Embedding model
# --------------------------------------------------

embedding_model = GeminiEmbeddings()


# --------------------------------------------------
# 2. Connect to our Chroma vector store
# --------------------------------------------------

vector_store = Chroma(
    collection_name="student_knowledge_langchain",
    embedding_function=embedding_model,
    persist_directory="./langchain_chroma_db"
)


# --------------------------------------------------
# 3. Create the retriever
# --------------------------------------------------

retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}
)


# --------------------------------------------------
# 4. Create Gemini LLM
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)


# --------------------------------------------------
# 5. Create the prompt
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
# 6. Convert retrieved documents into text
# --------------------------------------------------

def format_documents(documents):
    return "\n\n".join(
        document.page_content
        for document in documents
    )


# --------------------------------------------------
# 7. Build the LangChain RAG chain
# --------------------------------------------------

rag_chain = (
    {
        "context": retriever | format_documents,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
)


# --------------------------------------------------
# 8. Ask a question
# --------------------------------------------------

while True:
    question = input("\nAsk a question (type 'exit' to stop): ")

    if question.lower() == "exit":
        break

    response = rag_chain.invoke(question)

    print("\nAnswer:")

    if isinstance(response.content, list):
        for item in response.content:
            if isinstance(item, dict) and item.get("type") == "text":
                print(item.get("text"))
    else:
        print(response.content)