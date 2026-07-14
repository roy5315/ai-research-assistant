from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router

from app.services.vector_store import create_collection


app = FastAPI(
    title="AI Research Assistant",
    description="Chat with your research papers using AI",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "AI Research Assistant",
        "version": "0.1.0",
    }


create_collection()


app.include_router(documents_router)
app.include_router(chat_router)