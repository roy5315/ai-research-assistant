from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.pdf_service import extract_text_from_pdf

from app.services.text_service import chunk_text

from app.services.embedding_service import create_embeddings
from app.services.vector_store import (
    store_document_chunks,
    list_documents,
    delete_document,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    existing_documents = list_documents()

    for document in existing_documents:
        if document["filename"] == file.filename:
            raise HTTPException(
                status_code=409,
                detail=f"Document '{file.filename}' already exists",
            )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    extracted_text = extract_text_from_pdf(file_path)
    chunks = list(chunk_text(extracted_text))

    BATCH_SIZE = 50

    document_id = str(uuid4())

    total_embeddings = 0
    embedding_dimensions = 0

    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start:start + BATCH_SIZE]

        embeddings = list(create_embeddings(batch))

        store_document_chunks(
            chunks=batch,
            embeddings=embeddings,
            filename=file.filename,
            document_id=document_id,
        )

        total_embeddings += len(embeddings)

        if embeddings and embedding_dimensions == 0:
            embedding_dimensions = len(embeddings[0])

    return {
        "message": "Document uploaded and processed successfully",
        "filename": file.filename,
        "characters_extracted": len(extracted_text) if extracted_text else 0,
        "chunks_created": len(chunks),
        "embeddings_created": total_embeddings,
        "embedding_dimensions": embedding_dimensions,
        "first_chunk_preview": chunks[0][:500] if chunks else "",
        "document_id": document_id,
    }


@router.get("")
def get_documents():
    documents = list_documents()

    return {
        "documents": documents,
        "total": len(documents),
    }


@router.delete("/{document_id}")
def remove_document(document_id: str):
    delete_document(document_id)

    return {
        "message": "Document deleted successfully",
        "document_id": document_id,
    }