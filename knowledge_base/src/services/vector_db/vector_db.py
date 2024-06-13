import os
from qdrant_client import QdrantClient

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_EMBED_MODEL = os.getenv("QDRANT_EMBED_MODEL")
QDRANT_SEARCH_LIMIT = int(os.getenv("QDRANT_SEARCH_LIMIT"))


# Initialize the Qdrant client
client = QdrantClient(url=QDRANT_URL)
client.set_model(QDRANT_EMBED_MODEL)


def add_documents(collection_name: str, documents: list[str], metadata: list[dict] = None, ids: list = None) -> None:
    """
    Add a list of documents to a Qdrant collection.

    Args:
        collection_name (str): The name of the Qdrant collection.
        documents (list[str]): A list of document texts to be added.
        metadata (list[dict], optional): A list of metadata dictionaries corresponding to each document.
        ids (list, optional): A list of unique identifiers for each document.

    Returns:
        None
    """
    document_count = len(documents)
    print(f"Adding {document_count} documents into {collection_name}")

    client.add(
        collection_name=collection_name,
        documents=documents,
        metadata=metadata,
        ids=ids,
        parallel=0  # Disable parallel processing for simplicity
    )

    print("Finished adding documents")


def search(text: str, collection_name: str, limit: int = QDRANT_SEARCH_LIMIT) -> list:
    """
    Search for similar documents in a Qdrant collection based on a text query.

    Args:
        text (str): The text query to search for.
        collection_name (str): The name of the Qdrant collection.
        limit (int, optional): The maximum number of search results to return. Defaults to QDRANT_SEARCH_LIMIT.

    Returns:
        list: A list of search results containing document IDs, scores, and metadata.
    """
    print(f"Searching '{text}' in {collection_name}")
    search_result = client.query(
        collection_name=collection_name,
        query_text=text,
        limit=limit
    )
    return search_result
