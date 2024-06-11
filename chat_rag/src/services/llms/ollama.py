import os
import aiohttp
import asyncio
import re

LLM_API_URL = "https://api.openai.com/v1/chat/completions"
LLM_API_URL = "http://localhost:11434/api/chat"
LLM_API_URL = "http://ollama:11434/api/chat"


async def call_llm_stream(messages: list[dict], model: str = "phi3:mini"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('LLM_API_KEY', 'teste')}"
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
            async for line in response.content:
                token = re.search(r'(?<=content\":\").*?(?=\"},)', line.decode('utf-8'))
                if token:
                    yield token
                else:
                    print(line.decode('utf-8'))
    yield "\n"

async def call_llm(messages: list[dict], model: str = "phi3:mini"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('LLM_API_KEY', 'teste')}"
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
        async with session.post(LLM_API_URL, headers=headers, json=data) as response:
            resp = await response.json()
            print(resp)
            return resp
