import json
from datetime import datetime
from src.services.llms import ollama
from src.services.vector_db import vector_db
from src.utils.utils import load_html


PROMPT = "DOCUMENT:\n{DOCUMENT}"
SYSTEM_PROMPT = "You are a Q&A assistant chatbot, your task is to given a DOCUMENT generate all questions along with the answer for all possible questions that can be answered with that given DOCUMENT. Follow the format:\nQ: the generated question\nA: the answer to the question."

def format_prompt(document_chunk: str) -> list:
    """
    Generate a list of messages for the LLM based on the provided data.

    Args:
        document_chunk (str): The retrieved documents.

    Returns:
        list: A list of messages for the LLM.
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": PROMPT.format(DOCUMENT=document_chunk)}
    ]

async def call_vectorize(collection_name: str, file = None):
    if file:
        try:
            docs = load_html(file=file.file)
            docs_msgs = [format_prompt(x) for x in docs]
            questions = ollama.call_llm_batch(docs_msgs)
        except:
            return "error"
    else:
        return "error"

    vector_db.add_documents(
        collection_name=collection_name,
        documents=docs
    )
    questions = await questions
    json_data = {
        "chunks": docs,
        "questions": questions,
    }
    with open(f"data/{datetime.now().timestamp()}.json", "w") as fp:
        json.dump(json_data, fp, ensure_ascii=False)


def call_search(query: str, collection_name: str, limit: int = 10):
    return vector_db.search(
        text=query,
        collection_name=collection_name,
        limit=limit
    )