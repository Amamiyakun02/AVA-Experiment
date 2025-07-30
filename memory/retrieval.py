import chromadb

# Inisialisasi klien ke direktori penyimpanan ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Ambil koleksi atau buat baru jika belum ada
collection = client.get_or_create_collection(
    name="gemini_memory",
    metadata={"hnsw:space": "cosine"}  # gunakan cosine similarity
)

def add_memory_embedding(doc_id: str, text: str, embedding: list[float], metadata: dict = None):
    """
    Tambahkan dokumen baru ke ChromaDB dengan embedding.

    Args:
        doc_id (str): ID unik untuk dokumen ini.
        text (str): Konten asli dari dokumen.
        embedding (list): Vektor embedding dari konten.
        metadata (dict): Metadata opsional seperti {source: ..., tag: ...}
    """
    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata or {}]
    )


def query_memory(query_embedding: list[float], n_results: int = 3):
    """
    Melakukan pencarian dokumen yang mirip berdasarkan embedding.

    Args:
        query_embedding (list): Vektor embedding dari pertanyaan / input pengguna.
        n_results (int): Jumlah hasil kemiripan yang ingin diambil.

    Returns:
        List hasil dokumen yang mirip.
    """
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results
