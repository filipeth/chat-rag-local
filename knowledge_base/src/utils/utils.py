from unstructured.partition.html import partition_html

from typing import List, Literal, Any
import numpy as np
from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import BaseModel

from langchain_experimental.text_splitter import SemanticChunker
from src.vector_db.vector_db import client

def load_html(data: str = None, file = None):
    if file:
        elements = partition_html(file=file)
    else:
        try:
            elements = partition_html(filename=data)
        except:
            try:
                elements = partition_html(url=data)
            except:
                elements = partition_html(text=data)
    html_text = "\n".join(map(lambda x: x.text, elements))
    chunks = chunk_by_similarity(html_text)
    return [chunk.page_content for chunk in chunks]

class QdrantEmbeddings(BaseModel, Embeddings):
    doc_embed_type: Literal["default", "passage"] = "default"
    model: Any

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for documents using FastEmbed.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        embeddings: List[np.ndarray]
        if self.doc_embed_type == "passage":
            embeddings = self.model.passage_embed(texts)
        else:
            embeddings = self.model.embed(texts)
        return [e.tolist() for e in embeddings]

    def embed_query(self, text: str) -> List[float]:
        """Generate query embeddings using FastEmbed.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        query_embeddings: np.ndarray = next(self._model.query_embed(text))
        return query_embeddings.tolist()
    
embedding = QdrantEmbeddings(model=client.embedding_models['sentence-transformers/all-MiniLM-L6-v2'])

def chunk_by_similarity(text, breakpoint_threshold_type="percentile", breakpoint_threshold_amount: float = 85):
    text_splitter = SemanticChunker(
        embedding,
        breakpoint_threshold_type=breakpoint_threshold_type,
        breakpoint_threshold_amount=breakpoint_threshold_amount 
    )
    docs = text_splitter.create_documents([text])
    return docs