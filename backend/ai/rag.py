from ai.vector_db import get_vector_db


def retrieve_context(query: str, k: int = 2):
    vector_db = get_vector_db()

    results = vector_db.similarity_search(
        query,
        k=k
    )

    context = "\n\n".join(
        document.page_content
        for document in results
    )

    return context