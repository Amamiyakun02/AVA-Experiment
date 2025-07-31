from uuid import uuid4
from datetime import datetime, timezone, timedelta
from summarizer import summarize_memory

class MemoryManager:
    def __init__(self, user_id, chroma_client, mongo_db, embedding_fn):
        self.user_id = user_id
        self.chroma = chroma_client
        self.mongo = mongo_db
        self.embed = embedding_fn  # contoh: Gemini embed API

    def store_memory(self, message, source="user"):
        vector = self.embed(message)
        # simpan embedding ke chromadb
        self.chroma.add(
            collection_name=self.user_id,
            ids=[str(uuid4())],
            documents=[message],
            embeddings=[vector]
        )
        # simpan metadata ke MongoDB
        self.mongo.memory.insert_one({
            "user_id": self.user_id,
            "text": message,
            "source": source,
            "timestamp": datetime.now(timezone.utc)
        })

    def recall(self, query, top_k=3):
        query_vector = self.embed(query)
        results = self.chroma.query(
            collection_name=self.user_id,
            query_embeddings=[query_vector],
            n_results=top_k
        )
        return results['documents'][0] if results['documents'] else []

    def summarize_old_memory(self, max_age_minutes=60):
        # Ambil memori lama dari Mongo
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=max_age_minutes)
        old_memories = list(self.mongo.memory.find({
            "user_id": self.user_id,
            "timestamp": {"$lt": cutoff}
        }))
        # Ringkas (opsional)
        summary = summarize_memory([m['text'] for m in old_memories])
        self.store_memory(summary, source="summary")
