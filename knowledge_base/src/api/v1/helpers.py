import os
import json
from datetime import datetime
from src.services.llms import ollama
from src.services.vector_db import vector_db
from src.utils.utils import load_html

QDRANT_SEARCH_LIMIT = int(os.getenv("QDRANT_SEARCH_LIMIT"))

PROMPT = os.getenv("PROMPT")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

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

async def call_vectorize(collection_name: str, file=None, generate_questions: bool = False):
    """
    Process the provided file to extract documents, format them, and add them to the vector database.

    Args:
        collection_name (str): The name of the collection in the vector database.
        file (File, optional): The file containing the documents. Defaults to None.

    Returns:
        str: "error" if an error occurs, otherwise None.
    """
    if not file:
        print("Error: No file provided.")
        return "error"

    try:
        print("Loading file")
        docs = load_html(file=file.file)
        if generate_questions:
            print("Sending file to generate questions.")
            docs_msgs = [format_prompt(x) for x in docs]
            questions = ollama.call_llm_batch(docs_msgs)
    except Exception as e:
        print(f"Error processing file: {e}")
        return "error"
    
    print("Adding chunks to vector db")
    vector_db.add_documents(
        collection_name=collection_name,
        documents=docs
    )
    print("Chunks added")
    if generate_questions:
        print("Waitting for questions")
        questions = await questions
        json_data = {
            "chunks": docs,
            "questions": questions,
        }

        timestamp = datetime.now().timestamp()
        print(f"Saving {timestamp}.json")
        with open(f"{timestamp}.json", "w") as fp:
            json.dump(json_data, fp, ensure_ascii=False)
        print("File saved")

def call_search(query: str, collection_name: str, limit: int = QDRANT_SEARCH_LIMIT):
    """
    Search the vector database for the given query.

    Args:
        query (str): The search query.
        collection_name (str): The name of the collection in the vector database.
        limit (int, optional): The maximum number of results to return. Defaults to QDRANT_SEARCH_LIMIT.

    Returns:
        list: The search results.
    """
    results = vector_db.search(
        text=query,
        collection_name=collection_name,
        limit=limit
    )
    return results
