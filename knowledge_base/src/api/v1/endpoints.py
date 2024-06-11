from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

from src.vector_db import vector_db
from src.utils.utils import load_html

router = APIRouter()

@router.post("/vectorize")
def vectorize(collection_name: str, file: UploadFile = None):

    if file:
        try:
            docs = load_html(file=file.file)
        except:
            return "error"
    else:
        return "error"
        docs = load_html(data=request.text)

    vector_db.add_documents(
        collection_name=collection_name,
        documents=docs
    )

    return {"message": "Document vectorized and added to database"}

@router.get("/search")
def search(query: str, collection_name: str, limit: int = 10):
    return vector_db.search(
        text=query,
        collection_name=collection_name,
        limit=limit
    )