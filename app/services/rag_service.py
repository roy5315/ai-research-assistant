from app.services.embedding_service import create_embeddings
from app.services.vector_store import search_similar_chunks


def retrieve_context(
    query: str,
    document_id: str,
    top_k: int = 3,
) -> list[dict]:
    query_embeddings = create_embeddings([query])

    if not query_embeddings:
        return []

    query_embedding = query_embeddings[0]

    results = search_similar_chunks(
        query_embedding=query_embedding,
        document_id=document_id,
        top_k=top_k,
    )

    return results