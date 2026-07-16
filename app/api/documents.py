from pathlib import Path

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
        while chunk := await file.read(1024 * 1024):  # Read 1 MB at a time
            f.write(chunk)

    extracted_text = extract_text_from_pdf(file_path)
    chunks = chunk_text(extracted_text)
    embeddings = create_embeddings(chunks)

    document_id = store_document_chunks(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename,
    )

    return {
        "message": "Document uploaded and processed successfully",
        "filename": file.filename,
        "characters_extracted": len(extracted_text),
        "chunks_created": len(chunks),
        "embeddings_created": len(embeddings),
        "embedding_dimensions": len(embeddings[0]) if embeddings else 0,
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