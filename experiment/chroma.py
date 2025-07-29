import chromadb
from google import genai

client = genai.Client()
db_client = chromadb.PersistentClient(path="./chroma_db")  # folder bisa kamu atur
collection = db_client.get_or_create_collection(name="gemini_memory")

# # 3. Teks yang ingin kamu embed
# texts = [
#     "What is the meaning of life?",
#     "What is the purpose of existence?",
#     "How do I bake a cake?"
# ]
#
# # 4. Generate embedding dari Gemini
# result = client.models.embed_content(
#         model="gemini-embedding-001",
#         contents= texts
# )
#
# embeddings = [e.values for e in result.embeddings]
#
# # # 5. Simpan ke ChromaDB (tanpa embedding_function)
# # collection.add(
# #     ids=[f"doc{i}" for i in range(len(texts))],
# #     documents=texts,
# #     embeddings=embeddings
# # )
#
# print("✅ Embedding berhasil disimpan ke ChromaDB.")
#
# results = collection.query(
#     query_embeddings=[query_embedding],
#     n_results=2  # ambil top-2 hasil paling mirip
# )

# 1. Query teks
query_text = "How do I make a cake?"

# 2. Embedding-kan dengan Gemini#
query_result = client.models.embed_content(
    model="gemini-embedding-001",
    contents= "How do I bake a cake?",
)
query_embedding = query_result.embeddings
print(query_embedding)

# 3. Cari di ChromaDB
results = collection.query(
    query_embeddings=[query_embedding[0].values],
    n_results=2
)

# 4. Tampilkan hasil
print(f"\nQuery: {query_text}")
for i, doc in enumerate(results["documents"][0]):
    print(f"\nHasil #{i+1}:")
    print(f"Dokumen: {doc}")
    print(f"Metadata: {results['metadatas'][0][i] if results['metadatas'] else 'N/A'}")
    print(f"Distance: {results['distances'][0][i]:.4f}")
