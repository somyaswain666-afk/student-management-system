# Student Management System

A backend Student Management System built with FastAPI, SQLite, SQLAlchemy, Pydantic, Gemini AI, RAG, ChromaDB, LangChain, and LangGraph.

## Features

- Create student records
- View all students
- View an individual student
- Update student records
- Delete student records
- Search student information
- Calculate average GPA
- Find the student with the highest GPA
- Count students by department
- AI-powered student questions
- Retrieval-Augmented Generation (RAG)
- Knowledge-base question answering
- LangGraph-based routing between database and RAG

## Technology Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Google Gemini
- LangChain
- ChromaDB
- LangGraph
- Uvicorn

## Project Architecture

```text
                         User
                           |
                           v
                    FastAPI /chat
                           |
                           v
                    Chat Service
                           |
                           v
                      LangGraph
                           |
                    +------+------+
                    |             |
                    v             v
               Database          RAG
                  Node            Node
                    |               |
                    v               v
               SQLite DB        ChromaDB
                    |               |
                    |               v
                    |           Knowledge Base
                    |               |
                    +-------+-------+
                            |
                            v
                       Final Answer


                       Final Answer
```

## Vector Database Selection

### Selected Vector Database: ChromaDB

ChromaDB was selected as the vector database for this project because it fits
the requirements of a small FastAPI-based RAG application and integrates well
with the LangChain-based retrieval pipeline used in this project.

### Why ChromaDB?

- **Easy integration:** ChromaDB integrates with the LangChain retrieval
  workflow used by this project.
- **Similarity search:** It supports vector similarity retrieval, which is
  required for finding relevant knowledge-base content.
- **Development simplicity:** ChromaDB is straightforward to set up for a
  local development project.
- **Cost:** The local setup avoids requiring a separate paid vector-database
  service for this internship project.
- **Architecture compatibility:** ChromaDB works with the project's Python,
  LangChain, Gemini embeddings, and RAG architecture.
- **Scalability considerations:** The current project is a small internship
  application, so a local vector store is appropriate. A managed or
  distributed vector database could be considered for a significantly larger
  production workload.

### Alternatives Considered

**FAISS**

FAISS is a library for efficient similarity search and clustering of dense
vectors. It is a strong option for vector similarity search, but ChromaDB
provides a more convenient vector-store approach for the RAG architecture used
in this project.

**Managed Vector Databases**

Managed vector-database services can provide hosted and scalable vector
infrastructure. However, they introduce additional external-service and cost
considerations that are unnecessary for the current small internship project.

### Conclusion

ChromaDB was selected because it provides the required vector similarity
retrieval functionality while keeping the project's development complexity
appropriate for its current scale.

## RAG
Retrieval-Augmented Generation (RAG) is used in this project to answer

questions about the Student Management System knowledge base.

The knowledge base is stored in:

```text

student_handbook.txt

```

The RAG pipeline works as follows:

```text

Student Handbook

       ↓

Document Chunking

       ↓

Gemini Embeddings

       ↓

ChromaDB

       ↓

Similarity Retrieval

       ↓

Relevant Context

       ↓

Gemini

       ↓

Natural-Language Answer

```

### RAG Process

1. The information from the student handbook is divided into smaller

   document chunks.

2. Gemini embeddings are generated for the document chunks.

3. The embeddings are stored in ChromaDB.

4. When a user asks a knowledge-base question, the question is converted

   into an embedding.

5. ChromaDB retrieves the most relevant document chunks.

6. The retrieved content is provided as context to Gemini.

7. Gemini generates the final answer using the retrieved context.

### Example Questions

The RAG system can answer questions such as:

```text

What is the GPA scale?

Can students belong to different departments?

What information is required for enrollment?

```

If the requested information is not present in the knowledge base, the

system is instructed not to invent an answer and instead indicate that the

information is not available.

## Docker Deployment

The application can be containerized and run using Docker.

### Build the Docker Image

From the project root:

```bash

docker build -t student-management-system .