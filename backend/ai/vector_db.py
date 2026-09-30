from langchain_chroma import Chroma
from ai.embeddings import get_embeddings

VECTOR_DB_PATH = "./vectorstore"

_vector_db = None


def get_vector_db():
    global _vector_db

    if _vector_db is None:
        embeddings = get_embeddings()

        _vector_db = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=embeddings
        )

    return _vector_db