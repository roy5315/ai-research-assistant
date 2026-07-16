from app.services.embedding_service import create_query_embedding
from app.services.vector_store import search_similar_chunks


def retrieve_context(
    query: str,
    document_id: str,
    top_k: int = 3,
) -> list[dict]:

    query_embedding = create_query_embedding(query)

    return search_similar_chunks(
        query_embedding=query_embedding,
        document_id=document_id,
        top_k=top_k,
    )