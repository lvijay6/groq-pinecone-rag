import json
from pinecone import Pinecone
from groq import Groq
from sentence_transformers import SentenceTransformer
from config_secrets import get_secret

_pinecone_index = None
_groq_client = None
_embedding_model = None

def _init():
    global _pinecone_index, _groq_client, _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        _groq_client = Groq(api_key=get_secret("GROQ_API_KEY"))
        pc = Pinecone(api_key=get_secret("PINECONE_API_KEY"))
        _pinecone_index = pc.Index(get_secret("PINECONE_INDEX_NAME"))

def handler(event, context):
    _init()
    body = json.loads(event.get("body") or "{}")
    user_query = body.get("query")
    if not user_query:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing 'query' in request body"})}

    query_vector = _embedding_model.encode(user_query).tolist()
    search_response = _pinecone_index.query(vector=query_vector, top_k=3, include_metadata=True)

    if search_response.get("matches"):
        retrieved_context = search_response["matches"][0].get("metadata", {}).get("text", "No text found.")
    else:
        retrieved_context = "No matching documents found."

    completion = _groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Answer strictly using the provided context. If not found, say 'I cannot find the answer.'"},
            {"role": "user", "content": f"Context:\n{retrieved_context}\n\nQuestion: {user_query}"}
        ],
        temperature=0.7
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"answer": completion.choices[0].message.content})
    }
