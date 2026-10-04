import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

_embeddings = None


def get_embeddings():

    global _embeddings

    if _embeddings is None:

        _embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    return _embeddings