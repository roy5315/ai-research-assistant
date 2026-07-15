import os
from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router

from app.services.vector_store import create_collection
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AI Research Assistant",
    description="Chat with your research papers using AI",
    version="0.1.0",
)

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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