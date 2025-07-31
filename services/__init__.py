from .ai_engine import AIEngine

# method
from .chroma_service import get_or_create_collection, embed_texts, add_documents
from .mongo_service import get_all_memories, get_recent_memories, get_chat_history, get_user_by_id, save_memory, save_chat_message


# client
from .chroma_service import chroma_client
from .mongo_service import db

# collection
from .mongo_service import contacts_col, users_col, memory_col, chat_sessions_col, chat_messages_col