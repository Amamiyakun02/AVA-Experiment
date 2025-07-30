import chromadb
from google import genai
from typing import List, Optional

gemini_client = genai.Client()

# Inisialisasi client Chroma
CHROMA_PATH = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)


# Ambil atau buat collection
def get_or_create_collection(name: str):
    return chroma_client.get_or_create_collection(name=name)


# Fungsi untuk embed teks dengan Gemini
def embed_texts(texts: List[str]) -> List[List[float]]:
    response = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        # task_type="retrieval_document"
    )
    return [embedding.values for embedding in response.embeddings]


# Simpan dokumen ke ChromaDB
def add_documents(collection_name: str, texts: List[str], ids: Optional[List[str]] = None):
    collection = get_or_create_collection(collection_name)
    if not ids:
        from uuid import uuid4
        ids = [str(uuid4()) for _ in texts]

    embeddings = embed_texts(texts)
    collection.add(documents=texts, ids=ids, embeddings=embeddings)
    return ids


# Query dokumen dari ChromaDB
def query_documents(collection_name: str, query: str, top_k: int = 3) -> List[str]:
    collection = get_or_create_collection(collection_name)
    embedding = embed_texts([query])[0]
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    return results['documents'][0] if results['documents'] else []
