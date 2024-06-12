import os
import aiohttp
import asyncio
import re

LLM_API_URL = "https://api.openai.com/v1/chat/completions"
LLM_API_URL = "http://localhost:11434/api/chat"
LLM_API_URL = "http://ollama:11434/api/chat"

LLM_MODEL = "phi3:mini"

async def call_llm_stream(messages: list[dict], model: str = LLM_MODEL):
    """
    Make a streaming API call to the LLM API.

    Args:
        messages (list[dict]): List of message dictionaries.
        model (str): The LLM model to use (default: LLM_MODEL).

    Yields:
        str: The generated token from the LLM API response.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": os.getenv('LLM_API_KEY', 'Bearer teste')
    }
    data = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": 0
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(LLM_API_URL, headers=headers, json=data) as response:
            logging.info(f"Making streaming API call to {LLM_API_URL} with model {model}")
            async for line in response.content:
                token = re.search(r'(?<=content\":\").*?(?=\"},)', line.decode('utf-8'))
                if token:
                    yield token.group(0)
                else:
                    logging.warning(f"Unexpected line in API response: {line.decode('utf-8')}")

    logging.info("Streaming API call completed")
    yield "\n"


async def call_llm(messages: list[dict], model: str = LLM_MODEL) -> dict:
    """
    Make a non-streaming API call to the LLM API.

    Args:
        messages (list[dict]): List of message dictionaries.
        model (str): The LLM model to use (default: LLM_MODEL).

    Returns:
        dict: The JSON response from the LLM API.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": os.getenv('LLM_API_KEY', 'Bearer teste')
    }
    data = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(LLM_API_URL, headers=headers, json=data) as response:
                logging.info(f"Making non-streaming API call to {LLM_API_URL} with model {model}")
                if response.status == 200:
                    resp = await response.json()
                    return resp
                else:
                    logging.error(f"An error occurred on ollama call: {response}")

        except aiohttp.ClientError as e:
            logging.error(f"An error occurred during ollama call: {str(e)}")

