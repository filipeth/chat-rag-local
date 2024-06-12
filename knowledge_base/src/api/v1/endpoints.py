from fastapi import APIRouter, UploadFile
from src.api.v1.helpers import call_vectorize, call_search

router = APIRouter()

@router.post("/vectorize")
async def vectorize(collection_name: str, file: UploadFile = None):
    await call_vectorize(collection_name, file)
    
    return {"message": "Document vectorized and added to database"}

@router.get("/search")
def search(query: str, collection_name: str, limit: int = 10):
    return call_search(
        text=query,
        collection_name=collection_name,
        limit=limit
    )