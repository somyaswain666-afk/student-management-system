from langchain_chroma import Chroma

from langchain_rag_proper import GeminiEmbeddings


# Create the same embedding model
embedding_model = GeminiEmbeddings()


# Connect to our existing ChromaDB
vector_store = Chroma(
    collection_name="student_knowledge_langchain",
    embedding_function=embedding_model,
    persist_directory="./langchain_chroma_db"
)


# Turn the vector store into a retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}
)


# User question
question = "What is the GPA scale?"


# Retrieve relevant documents
documents = retriever.invoke(question)


print("\nQuestion:")
print(question)

print("\nRetrieved documents:")

for i, document in enumerate(documents, start=1):
    print(f"\n--- Result {i} ---")
    print(document.page_content)