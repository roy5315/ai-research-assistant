import traceback
from app.services.chat_history import (
    get_chat_history,
    add_message,
)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag_service import retrieve_context
from app.services.llm_service import generate_answer


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    query: str
    document_id: str 
    top_k: int = 3
    session_id: str = "default"


@router.post("")
def chat_with_document(request: ChatRequest):
    try:
        sources = retrieve_context(
            query=request.query,
            document_id=request.document_id,
            top_k=request.top_k,
        )

        if not sources:
            raise HTTPException(
                status_code=400,
                detail="No relevant document context found",
            )

        context_chunks = [
            source["text"] for source in sources
        ]

        history = get_chat_history(request.session_id)

        answer = generate_answer(
            query=request.query,
            context_chunks=context_chunks,
            history=history,
        )

        add_message(
            session_id=request.session_id,
            role="user",
            content=request.query,
        )

        add_message(
            session_id=request.session_id,
            role="assistant",
            content=answer,
        )
        clean_sources = [
            {
                "filename": source.get("filename"),
                "chunk_index": source.get("chunk_index"),
                "score": round(source.get("score", 0), 4),
            }
            for source in sources
        ]

        return {
            "query": request.query,
            "answer": answer,
            "session_id": request.session_id,
            "sources": clean_sources,
        }

    except HTTPException:
        raise

    except Exception :
       traceback.print_exc()
       raise 