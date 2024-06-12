from typing import List, Literal, Any
import numpy as np
from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import BaseModel
from langchain_experimental.text_splitter import SemanticChunker
from unstructured.partition.html import partition_html
from src.services.vector_db.vector_db import client

# Constants
QDRANT_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SEMANTIC_CHUNKER_TYPE = "percentile"
SEMANTIC_CHUNKER_AMOUNT = 85


class QdrantEmbeddings(BaseModel, Embeddings):
    """
    A class for generating embeddings using the Qdrant embedding model.
    """
    doc_embed_type: Literal["default", "passage"] = "default"
    model: Any

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for documents using the Qdrant embedding model.

        Args:
            texts (List[str]): The list of texts to embed.

        Returns:
            List[List[float]]: A list of embeddings, one for each text.
        """
        embeddings: List[np.ndarray]
        if self.doc_embed_type == "passage":
            embeddings = self.model.passage_embed(texts)
        else:
            embeddings = self.model.embed(texts)
        return [e.tolist() for e in embeddings]

    def embed_query(self, text: str) -> List[float]:
        """
        Generate query embeddings using the Qdrant embedding model.

        Args:
            text (str): The text to embed.

        Returns:
            List[float]: Embeddings for the text.
        """
        query_embeddings: np.ndarray = next(self.model.query_embed(text))
        return query_embeddings.tolist()

# Initialize the embedding model
embedding = QdrantEmbeddings(model=client.embedding_models[QDRANT_EMBED_MODEL])


def load_html(data: str = None, file=None) -> List[str]:
    """
    Load HTML data from a file, URL, or text string.

    Args:
        data (str, optional): A URL or text string containing HTML data.
        file (str, optional): A file path to an HTML file.

    Returns:
        List[str]: A list of text chunks extracted from the HTML data.
    """
    if file:
        elements = partition_html(file=file)
    else:
        try:
            elements = partition_html(filename=data)
        except Exception:
            try:
                elements = partition_html(url=data)
            except Exception:
                elements = partition_html(text=data)

    html_text = "\n".join(element.text for element in elements)
    chunks = chunk_by_similarity(html_text)
    return [chunk.page_content for chunk in chunks]


def chunk_by_similarity(text: str, breakpoint_threshold_type=SEMANTIC_CHUNKER_TYPE,
                        breakpoint_threshold_amount: float = SEMANTIC_CHUNKER_AMOUNT) -> List[Any]:
    """
    Split a text into semantic chunks based on similarity.

    Args:
        text (str): The text to be split into chunks.
        breakpoint_threshold_type (str, optional): The type of threshold to use for splitting.
        breakpoint_threshold_amount (float, optional): The threshold amount for splitting.

    Returns:
        List[Any]: A list of semantic chunks.
    """
    text_splitter = SemanticChunker(
        embedding,
        breakpoint_threshold_type=breakpoint_threshold_type,
        breakpoint_threshold_amount=breakpoint_threshold_amount
    )
    docs = text_splitter.create_documents([text])
    return docs
