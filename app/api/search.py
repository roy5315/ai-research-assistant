from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.document_store import document_store
from app.services.embedding_service import create_query_embedding
from app.services.search_service import semantic_search


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


class SearchRequest(BaseModel):
    query: str
    top_k: int = 3


@router.post("")
def search_documents(request: SearchRequest):
    chunks = document_store["chunks"]
    embeddings = document_store["embeddings"]

    if not chunks or not embeddings:
        raise HTTPException(
            status_code=400,
            detail="Upload a document before searching",
        )

    query_embedding = create_query_embedding(
        request.query
    )

    results = semantic_search(
        query_embedding=query_embedding,
        chunks=chunks,
        chunk_embeddings=embeddings,
        top_k=request.top_k,
    )

    return {
        "query": request.query,
        "results": results,
    }