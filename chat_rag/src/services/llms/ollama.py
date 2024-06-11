import os
import aiohttp
import asyncio
import re

LLM_API_URL = "https://api.openai.com/v1/chat/completions"
LLM_API_URL = "http://localhost:11434/api/chat"
LLM_API_URL = "http://ollama:11434/api/chat"


async def call_llm(messages: list[dict], model: str = "phi3:mini", stream: bool=True):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('LLM_API_KEY', 'teste')}"
    }
    data = {
        "model": model,
        "messages": messages,
        "stream": stream
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(LLM_API_URL, headers=headers, json=data) as response:
            if stream:
                async for line in response.content:
                    token = re.search(r'(?<=content\":\").*?(?=\"},)', line.decode('utf-8'))
                    if token:
                        print(token.group(), end="")
                    else:
                        print(line.decode('utf-8'))
            else:
                return await response.json()
            
if __name__ == "__main__":
    resp = asyncio.run(call_llm([
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Hello!"
            }
        ]))