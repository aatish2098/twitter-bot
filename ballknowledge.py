import os
from phi.vectordb.qdrant import Qdrant
from phi.document import Document


def store_with_embedding(doclist: list[Document]) -> Qdrant:
    api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    collection_name = "list_tweets"
    vector_db = Qdrant(
        collection=collection_name,
        url=qdrant_url,
        api_key=api_key
    )
    vector_db.insert(documents=doclist)
    return vector_db

def fetch_qdrant() -> Qdrant:
    api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    collection_name = "list_tweets"
    vector_db = Qdrant(
        collection=collection_name,
        url=qdrant_url,
        api_key=api_key)
    return vector_db


