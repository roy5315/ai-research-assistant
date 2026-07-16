from functools import lru_cache

from fastembed import TextEmbedding


MODEL_NAME = "BAAI/bge-small-en-v1.5"


@lru_cache(maxsize=1)
def get_embedding_model() -> TextEmbedding:
    return TextEmbedding(
        model_name=MODEL_NAME,
    )


def create_embeddings(chunks: list[str]) -> list[list[float]]:
    embedding_model = get_embedding_model()

    embeddings = embedding_model.embed(chunks)

    return [
        embedding.tolist()
        for embedding in embeddings
    ]


def create_query_embedding(query: str) -> list[float]:
    embedding_model = get_embedding_model()

    embeddings = embedding_model.query_embed(query)

    query_embedding = next(embeddings)

    return query_embedding.tolist()