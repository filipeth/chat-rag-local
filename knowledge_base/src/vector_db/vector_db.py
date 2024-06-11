from qdrant_client import QdrantClient


client = QdrantClient(url="http://qdrant:6333")
client.set_model("sentence-transformers/all-MiniLM-L6-v2")

def add_documents(
    collection_name: str,
    documents: list[str],
    metadata: list[dict] = None,
    ids: list = None
):
    print(f"Adding {len(documents)} documents into {collection_name}")
    client.add(
        collection_name=collection_name,
        documents=documents,
        metadata=metadata,
        ids=ids,
        parallel=0
    )
    print("Finished adding documents")

def search(text: str, collection_name: str, limit: int = 10):
    print(f"Searching {text} in {collection_name}")
    search_result = client.query(
        collection_name=collection_name,
        query_text=text,
        limit=limit
    )
    return search_result

if __name__ == "__main__":
    print("oi")