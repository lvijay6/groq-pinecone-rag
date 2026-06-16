from typing import List

def chunk_pages(pages: List[str], chunk_size: int = 1000, chunk_overlap: int = 150) -> List[str]:
    """
    Chunks the given pages into smaller pieces of specified size.

    Args:
        pages (List[str]): A list of page contents as strings.
        chunk_size (int): The maximum number of characters in each chunk.

    Returns:
        List[Tuple[int, str]]: A list of tuples where each tuple contains the page index and the chunked text.
    """
    chunks: List[str] = []
    fulltext = " ".join(pages)
    text_length = len(fulltext)
    
    if text_length == 0:
        return chunks
    start = 0
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = fulltext[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
        if end >= text_length:
            break
        start = end - chunk_overlap  # Move back by chunk_overlap for the next chunk
        print("starting new chunk from index:", start)

    return chunks