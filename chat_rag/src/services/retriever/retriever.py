import aiohttp
import asyncio

SEARCH_API_URL = "http://knowledge-base:8000/v1/search"

async def asearch(query: str, collection_name: str, limit: int = 1):
    params = {
        "query": query,
        "collection_name": collection_name,
        "limit": limit
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(SEARCH_API_URL, params=params) as response:
            return await response.json()

if __name__ == "__main__":
    print(asyncio.run(asearch("melhor produto", "teste")))
