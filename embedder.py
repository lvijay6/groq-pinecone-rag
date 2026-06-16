from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings

_embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def chunk_embeddings(chunks: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of text chunks.

    Args:
        chunks (List[str]): A list of text chunks to be embedded."""
    embeddings = []
    for chunk in chunks:
        response = _embeddings_model.embed_documents([chunk])
        embeddings.append(response)
        
    return embeddings

