# memory_manager.py
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from .summarizer import summarize_memory

class MemoryManager:
    def __init__(self, user_id, chroma_client, embedding_fn, mongo_service):
        self.user_id = user_id
        self.chroma = chroma_client
        self.embed = embedding_fn
        self.mongo = mongo_service  # <- Injected module, not raw `db`

    def store_memory(self, message, source="user"):
        vector = self.embed(message)

        # Simpan ke ChromaDB
        self.chroma.add(
            collection_name=self.user_id,
            ids=[str(uuid4())],
            documents=[message],
            embeddings=[vector]
        )

        # Simpan ke MongoDB via service
        self.mongo.save_memory(self.user_id, message, source=source)

    def recall(self, query, top_k=3):
        query_vector = self.embed(query)
        results = self.chroma.query(
            collection_name=self.user_id,
            query_embeddings=[query_vector],
            n_results=top_k
        )
        return results['documents'][0] if results['documents'] else []

    def summarize_old_memory(self, max_age_minutes=60):
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=max_age_minutes)
        old_memories = self.mongo.get_old_memories(self.user_id, cutoff)

        if not old_memories:
            return

        texts = [m['text'] for m in old_memories]
        summary = summarize_memory(texts)
        self.store_memory(summary, source="summary")
