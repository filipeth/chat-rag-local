from typing import Union, AsyncGenerator
from src.services.llms import ollama 
from src.services.retriever import retriever
from src.api.v1.models import ChatRequest

PROMPT = "DOCUMENTS:\n{DOCUMENTS}\n\nQUESTION:\n{QUESTION}"

def get_messages(documents: str, question: str) -> list:
    """
    Generate a list of messages for the LLM based on the provided documents and question.

    Args:
        documents (str): The retrieved documents.
        question (str): The user's question.

    Returns:
        list: A list of messages for the LLM.
    """
    return [
        {"role": "system", "content": ""},
        {"role": "user", "content": PROMPT.format(DOCUMENTS=documents, QUESTION=question)}
    ]

async def call_rag(request: ChatRequest) -> str:
    """
    Retrieve relevant documents and generate a response using the LLM.

    Args:
        request (ChatRequest): The user's chat request.

    Returns:
        str: The generated response from the LLM.
    """
    documents = await retriever.asearch(
        query=request.text,
        collection_name=request.collection_name,
    )
    messages = get_messages(documents, request.text)
    logger.info(f"Calling LLM")
    response = await ollama.call_llm(messages=messages)
    logger.info(f"Generated response: {response['message']['content']}")
    response['documents'] = documents
    return response

async def call_rag_stream(request: ChatRequest):
    """
    Retrieve relevant documents and generate a response stream using the LLM.

    Args:
        request (ChatRequest): The user's chat request.

    Yields:
        str: The generated response tokens from the LLM.
    """
    documents = await retriever.asearch(
        query=request.text,
        collection_name=request.collection_name,
    )
    yield "Documents:\n"
    for d in documents:
        yield json.dumps(d) + "\n\n"

    messages = get_messages(documents, request.text)
    logger.info(f"Calling LLM stream")
    async for token in ollama.call_llm_stream(messages=messages):
        yield token
