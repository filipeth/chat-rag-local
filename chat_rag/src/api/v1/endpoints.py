from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.api.v1.helpers import call_rag, call_rag_stream
from src.api.v1.models import ChatRequest


router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    if request.stream:
        return StreamingResponse(call_rag_stream(request), media_type="text/event-stream")
    else:
        resp = await call_rag(request)
        return resp
