from dotenv import load_dotenv
from pinecone import Pinecone
# from langchain_groq import ChatGroq
# from langchain_pinecone import PineconeVectorStore
# from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq
from sentence_transformers import SentenceTransformer

import os

load_dotenv()

groq_api_key = Groq(api_key=os.getenv("GROQ_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
# index = pc.Index(index_name)

# embedding_engine = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

user_query = "Dec 2013 to Feb 2015 working company name and role"

query_vector = embedding_model.encode(user_query).tolist()

search_response = index_name.query(
    vector=query_vector,
    top_k=3,
    include_metadata=True
)
# Extract text content safely from the raw Pinecone metadata layout dictionary
if search_response.get("matches"):
    top_match = search_response["matches"][0]
    retrieved_context = top_match.get("metadata", {}).get("text", "No text found in metadata.")
    confidence_score = top_match.get("score", 0.0)
    print(f"-> Successfully retrieved text chunk (Match Confidence Score: {confidence_score:.4f})\n")
else:
    retrieved_context = "No matching reference documents discovered."
    print("-> No match found in the database index.")

# 5. Step C: Build Context-Grounded Prompt & Run Groq AI
system_instructions = (
    "You are a precise assistant. Answer the question strictly using the provided "
    "Reference Context. If the context does not contain the answer, say 'I cannot find the answer.'"
)

completion = groq_api_key.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": f"Reference Context:\n{retrieved_context}\n\nQuestion: {user_query}"}
    ],
    temperature=0.7 # Forces a factual, non-creative response
)


# result = llm.invoke(retrieved_context)

# print(result.content)

# 6. Display the Output
print("--- Groq AI Grounded Response ---")
print(completion.choices[0].message.content)