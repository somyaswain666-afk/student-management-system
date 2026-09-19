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


### One important thing

The README deliberately describes **what we've actually built**. We're not claiming that the system is a fully autonomous natural-language SQL agent.
