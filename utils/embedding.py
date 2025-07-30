import os
from google import generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY tidak ditemukan di environment variables.")

genai.configure(api_key=api_key)

def get_embedding(text: str, model_name: str = "gemini-embedding-001") -> list[float]:
    """
    Menghasilkan embedding vektor dari input teks.

    Args:
        text (str): Teks yang akan dikonversi menjadi embedding.
        model_name (str): Nama model Gemini untuk embedding (default: embedding-001).

    Returns:
        list: Vektor embedding dalam bentuk list float.
    """
    try:
        result = genai.embed_content(
            model=model_name,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']

    except Exception as e:
        print(f"❌ Error saat membuat embedding: {e}")
        return []
