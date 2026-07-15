import os
from uuid import uuid4


from qdrant_client import QdrantClient
from qdrant_client import models
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)


QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://127.0.0.1:6333",
)
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "research_documents"
VECTOR_SIZE = 384


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)


def create_collection() -> None:
    if not client.collection_exists(
        collection_name=COLLECTION_NAME
    ):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def store_document_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    filename: str,
) -> str:
    document_id = str(uuid4())

    points = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        point = PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "document_id": document_id,
                "filename": filename,
                "chunk_index": index,
            },
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    return document_id


def search_similar_chunks(
    query_embedding: list[float],
    document_id: str,
    top_k: int = 3,
) -> list[dict]:
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="document_id",
                    match=models.MatchValue(
                        value=document_id
                    ),
                )
            ]
        ),
        limit=top_k,
        with_payload=True,
    )

    results = []

    for point in response.points:
        results.append(
            {
                "text": point.payload["text"],
                "score": point.score,
                "document_id": point.payload["document_id"],
                "filename": point.payload["filename"],
                "chunk_index": point.payload["chunk_index"],
            }
        )

    return results
    def list_documents() -> list[dict]:
     points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )
    return results


def list_documents() -> list[dict]:
    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    documents = {}

    for point in points:
        payload = point.payload or {}

        document_id = payload.get("document_id")
        filename = payload.get("filename")

        if document_id and document_id not in documents:
            documents[document_id] = {
                "document_id": document_id,
                "filename": filename,
            }

    return list(documents.values())


def delete_document(document_id: str) -> None:
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id),
                    )
                ]
            )
        ),
    )