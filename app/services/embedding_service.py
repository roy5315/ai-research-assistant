from fastembed import TextEmbedding


MODEL_NAME = "BAAI/bge-small-en-v1.5"

embedding_model = TextEmbedding(
    model_name=MODEL_NAME,
)


def create_embeddings(chunks: list[str]) -> list[list[float]]:
    embeddings = embedding_model.embed(chunks)

    return [
        embedding.tolist()
        for embedding in embeddings
    ]


def create_query_embedding(query: str) -> list[float]:
    embeddings = embedding_model.query_embed(query)

    query_embedding = next(embeddings)

    return query_embedding.tolist()