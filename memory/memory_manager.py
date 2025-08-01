# memory_manager.py
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from .summarizer import summarize_memory  # pastikan ada file summarizer.py
from services import mongo_service, chroma_service

class MemoryManager:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.mongo = mongo_service
        self.embed = chroma_service.embed_fn
        self.chroma = chroma_service

    def store_memory(self, message: str, source="user"):
        vector = self.embed(message)
        # Simpan ke ChromaDB
        self.chroma.add_documents(
            collection_name=self.user_id,
            texts=[message],
            ids=[str(uuid4())]
        )
        # Simpan metadata ke Mongo
        self.mongo.save_memory(self.user_id, message, source)

    def recall(self, query: str, top_k=3):
        return self.chroma.query_documents(
            collection_name=self.user_id,
            query=query,
            top_k=top_k
        )

    def summarize_old_memory(self, max_age_minutes=60):
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=max_age_minutes)
        old_memories = self.mongo.get_old_memories(self.user_id, cutoff)
        if not old_memories:
            return
        texts = [m['text'] for m in old_memories]
        summary = summarize_memory(texts)
        self.store_memory(summary, source="summary")

    def recall_mongo(self, top_k: int = 6) -> list[str]:
        """
        Mengambil top_k memori terbaru dari MongoDB dari user dan assistant.
        Jumlah total hasil adalah top_k gabungan (bisa 3 user + 3 assistant, dll).

        Returns:
            List[str]: Daftar konten percakapan terakhir.
        """
        cursor = self.mongo.memory_col.find(
            {
                "user_id": self.user_id,
                "source": {"$in": ["user", "assistant"]}
            },
            {
                "_id": 0,
                "text": 1,
                "source": 1,
                "timestamp": 1
            }
        ).sort("timestamp", -1).limit(top_k)

        # Ambil isi teks saja (dan urutkan kembali secara kronologis)
        return [doc["text"] for doc in reversed(list(cursor)) if "text" in doc]
