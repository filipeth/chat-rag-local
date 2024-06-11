from src.services.llms import ollama 
from src.services.retriever import retriever
from src.api.v1.models import ChatRequest

PROMPT = "DOCUMENTS:\n{DOCUMENTS}\n\nQUESTION:\n{QUESTION}"

async def call_rag(request: ChatRequest):
    documents = await retriever.asearch(
        query=request.text,
        collection_name=request.collection_name,
        limit=5
    )
    messages = [
        {
            "role": "system",
            "content": "You are a RAG chatbot, only answer the QUESTION with the provided DOCUMENTS, else say you cant help in a polite away. You must never talk about religion, politics, or provide any harm. Answer in the same language as QUESTION."
        },
        {
            "role": "user",
            "content": PROMPT.format(DOCUMENTS=documents, QUESTION=request.text)
        }
    ]
    return ollama.call_llm(
        messages=messages,
        stream=request.stream
    )
