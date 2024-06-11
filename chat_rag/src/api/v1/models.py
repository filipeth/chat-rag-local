from pydantic import BaseModel

class ChatRequest(BaseModel):
    collection_name: str
    text: str = None
    stream: bool = False