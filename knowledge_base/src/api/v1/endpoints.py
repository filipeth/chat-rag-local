import os
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from src.api.v1.helpers import call_vectorize, call_search

QDRANT_SEARCH_LIMIT = int(os.getenv("QDRANT_SEARCH_LIMIT"))

router = APIRouter()

@router.post("/vectorize")
async def vectorize(collection_name: str, file: UploadFile):
    """
    Vectorize a document and add it to the specified collection.

    Args:
        collection_name (str): The name of the collection to add the document to.
        file (UploadFile): The file to be vectorized.

    Returns:
        dict: A message indicating the success of the operation.

    Raises:
        HTTPException: If an error occurs during the vectorization process.
    """
    # Check if the file extension is supported
    supported_extensions = [".htm", ".html"]
    if not any(ext in file.filename for ext in supported_extensions):
        raise HTTPException(status_code=400, detail="File format not supported")
    try:
        await call_vectorize(collection_name, file)
        return JSONResponse({"message": "Document vectorized and added to database"})
    except Exception as e:
        print(f"Error during vectorization: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during vectorization")

@router.get("/search")
def search(query: str, collection_name: str, limit: int = QDRANT_SEARCH_LIMIT):
    """
    Search for similar documents in the specified collection based on a query.

    Args:
        query (str): The search query.
        collection_name (str): The name of the collection to search in.
        limit (int, optional): The maximum number of search results to return. Defaults to QDRANT_SEARCH_LIMIT.

    Returns:
        dict: The search results containing the similar documents.

    Raises:
        HTTPException: If an error occurs during the search process.
    """
    try:
        results = call_search(
            query=query,
            collection_name=collection_name,
            limit=limit
        )
        return results
    except Exception as e:
        print(f"Error during search: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during search")
