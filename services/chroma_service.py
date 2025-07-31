import chromadb
from chromadb.config import Settings
from google import genai
from typing import List, Optional
from uuid import uuid4

# Inisialisasi Gemini client (pastikan sudah dikonfigurasi sebelumnya)
gemini_client = genai.Client()

# Inisialisasi client ChromaDB (pastikan path bisa ditulis)
CHROMA_PATH = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# --- Fungsi Collection ---

def get_or_create_collection(name: str):
    """Mendapatkan atau membuat koleksi berbasis user_id"""
    return chroma_client.get_or_create_collection(name=name)

# --- Fungsi Embed ---

def embed_texts(texts: List[str]) -> List[List[float]]:
    """Gunakan Gemini untuk mengubah teks jadi embedding vektor"""
    if not texts:
        return []

    response = gemini_client.models.embed_content(
        model="models/embedding-001",
        contents=texts
    )
    return [embedding.values for embedding in response.embeddings]


# --- Simpan ke Chroma ---

def add_documents(collection_name: str, texts: List[str], ids: Optional[List[str]] = None):
    """Simpan teks + embedding ke Chroma"""
    if not texts:
        return []

    collection = get_or_create_collection(collection_name)

    if ids is None:
        ids = [str(uuid4()) for _ in texts]

    embeddings = embed_texts(texts)

    collection.add(
        documents=texts,
        ids=ids,
        embeddings=embeddings
    )
    return ids

# --- Query ke Chroma ---
def query_documents(collection_name: str, query: str, top_k: int = 3) -> List[str]:
    """Query dokumen yang relevan berdasarkan embedding"""
    collection = get_or_create_collection(collection_name)
    embedding = embed_texts([query])[0]
    results = collection.query(query_embeddings=[embedding], n_results=top_k)

    return results.get('documents', [])[0] if results.get('documents') else []