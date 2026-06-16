from PyPDF2 import PdfReader
from typing import List
from chunker import chunk_pages
from embedder import chunk_embeddings
from vectorstore import store_in_pinecone
from typing import List

pdf_path = "./resources/sample.pdf"
def run():
    reader = PdfReader(pdf_path)
    pages = [page.extract_text() for page in reader.pages]
    chunks = chunk_pages(pages, chunk_size=1000, chunk_overlap=150)
    embeddings = chunk_embeddings(chunks)
    store_in_pinecone(chunks, embeddings, namespace="")

    # print("total chunks embedded:", len(embeddings))
    # print("first chunk embedding:", embeddings[0])
    # print("total chunks created:", len(chunks))
    # print("first chunk content:")
    # print(chunks[0])


    # print(f"Extracted {len(pages)} pages from the PDF.")
    # print("first page content:")
    # print(pages[0] if pages else "No content found.")

if __name__ == "__main__":
    run()