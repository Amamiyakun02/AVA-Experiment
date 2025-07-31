# services/chroma_service.py
import chromadb
from chromadb.config import Settings
from google import genai
from typing import List, Optional
from uuid import uuid4
import os

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY tidak ditemukan di environment variables.")

client = genai.Client(api_key=api_key)
# Chroma persistent client
CHROMA_PATH = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Fungsi: Ambil/buat collection
def get_or_create_collection(name: str):
    return chroma_client.get_or_create_collection(name=name)

# Fungsi: Embedding list teks
def embed_texts(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []
    response = client.models.embed_content(
        model="models/embedding-001",
        contents=texts,
    )
    return [embedding.values for embedding in response.embeddings]

# Fungsi: Single text
def embed_fn(text: str) -> List[float]:
    return embed_texts([text])[0]

# Fungsi: Tambah dokumen ke Chroma
def add_documents(collection_name: str, texts: List[str], ids: Optional[List[str]] = None):
    if not texts:
        return []
    collection = get_or_create_collection(collection_name)
    if ids is None:
        ids = [str(uuid4()) for _ in texts]
    embeddings = embed_texts(texts)
    collection.add(documents=texts, ids=ids, embeddings=embeddings)
    return ids

# Fungsi: Query dokumen dari Chroma
def query_documents(collection_name: str, query: str, top_k: int = 3) -> List[str]:
    collection = get_or_create_collection(collection_name)
    embedding = embed_texts([query])[0]
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    return results.get('documents', [])[0] if results.get('documents') else []
