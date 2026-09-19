import os

from dotenv import load_dotenv
from google import genai
from langchain_core.embeddings import Embeddings


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


client = genai.Client(api_key=api_key)


class GeminiEmbeddings(Embeddings):

    def embed_documents(self, texts):
        embeddings = []

        for text in texts:
            response = client.models.embed_content(
                model="gemini-embedding-001",
                contents=text
            )

            embeddings.append(
                response.embeddings[0].values
            )

        return embeddings

    def embed_query(self, text):
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return response.embeddings[0].values