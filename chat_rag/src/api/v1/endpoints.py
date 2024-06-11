from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.api.v1.helpers import call_rag
from src.api.v1.models import ChatRequest


router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    if request.stream:
        return StreamingResponse(call_rag(request), media_type="text/event-stream")
    resp = await call_rag(request)
    return resp
