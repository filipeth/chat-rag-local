import aiohttp
import asyncio

SEARCH_API_URL = "http://knowledge-base:8000/v1/search"
DEFAULT_LIMIT = 5

async def asearch(query: str, collection_name: str, limit: int = DEFAULT_LIMIT) -> dict:
    """
    Perform a search query on the knowledge base.

    Args:
        query (str): The search query.
        collection_name (str): The name of the collection to search in.
        limit (int, optional): The maximum number of search results to return. Defaults to DEFAULT_LIMIT.

    Returns:
        dict: The search results as a dictionary.
    """
    params = {
        "query": query,
        "collection_name": collection_name,
        "limit": limit
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(SEARCH_API_URL, params=params) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Search query '{query}' returned {len(result)} results.")
                    return result
                else:
                    logger.error(f"Search query '{query}' failed with status code {response.status}.")
                    return {}
        except aiohttp.ClientError as e:
            logger.exception(f"An error occurred during the search query '{query}': {str(e)}")
            return {}
