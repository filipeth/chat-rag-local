import os
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
SEARCH_API_URL = os.getenv("SEARCH_API_URL")
DEFAULT_LIMIT = int(os.getenv("SEARCH_LIMIT"))

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
