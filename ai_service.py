import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def ask_gemini(question: str, student_data: str) -> str:
    prompt = f"""
You are an AI assistant for a Student Management System.

Use the student data provided below to answer the user's question.

Student Data:
{student_data}

User Question:
{question}

Instructions:
- Answer based on the student data when the question is about students.
- If the required information is not present in the student data, clearly say that it is not available.
- Do not invent student information.
- Give a clear and concise answer.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text