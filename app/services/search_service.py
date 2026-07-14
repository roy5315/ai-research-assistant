import numpy as np


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    a = np.array(vector_a)
    b = np.array(vector_b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def semantic_search(
    query_embedding: list[float],
    chunks: list[str],
    chunk_embeddings: list[list[float]],
    top_k: int = 3,
) -> list[dict]:
    results = []

    for chunk, embedding in zip(chunks, chunk_embeddings):
        score = cosine_similarity(
            query_embedding,
            embedding,
        )

        results.append(
            {
                "text": chunk,
                "score": score,
            }
        )

    results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return results[:top_k]