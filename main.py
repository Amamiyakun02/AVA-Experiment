import os
import json
from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from services import AIEngine
from memory import MemoryManager
from utils import  build_prompt, get_embedding
from services import db, chroma_client
with open("utils/func_call/func_instruction.json", "r") as f:
    FUNCTION_INSTRUCTION = json.load(f)
with open("assistants/cristina.json", "r") as c:
    ASSISTANT = json.load(c)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY tidak ditemukan di environment variables.")

ai = AIEngine(api_key=api_key)
memory = MemoryManager(
    user_id="amamiya",
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXPERIENCE = {
    "user_id": "amamiya",
    "name": "Cristina",
    "personality": {
        "role": "Asisten Virtual",
        "style": "ramah, informatif, dingin, sedikit jenaka",
        "language": "Bahasa Indonesia, Bahasa Jepang"
    },
    "memory": []
}

from typing import List, Literal
from pydantic import BaseModel, Field
class CodeProgram(BaseModel):
    narasi: str = Field(description="Penjelasan singkat mengenai tujuan atau fungsi dari kode program ini.")
    nama_bahasa: str = Field(
        description="Nama bahasa pemrograman yang digunakan, contoh: Python, JavaScript, Java.")
    isi_program: str = Field(description="Seluruh isi kode program dalam bentuk string mentah.")
    perintah_lain: List[str] = Field(description="Daftar perintah atau instruksi tambahan untuk menjalankan kode.")


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.post("/streamtext")
async def index(payload: ChatRequest = Body(...)):
    try:
        messages = payload.messages
        if not messages:
            raise ValueError("Tidak ada pesan dalam permintaan.")
        user_input = messages[0].content
        if not user_input:
            raise ValueError("Konten pesan kosong.")

        # === Memory Recall ===
        context_memories = memory.recall(user_input, top_k=3)
        context = "\n".join(context_memories)

        # === Bangun Prompt dengan Memori ===
        full_input = f"{context}\n\nUser:\n{user_input}" if context else user_input
        prompt = build_prompt(ASSISTANT, full_input)
        print(prompt)
        # === Streaming ke LLM ===
        async def streaming_wrapper():
            full_response = ""
            async for chunk in ai.stream_generate_text(prompt):
                full_response += chunk
                yield chunk
            # Simpan memori setelah selesai stream
            memory.store_memory(user_input, source="user")
            memory.store_memory(full_response, source="assistant")

        return StreamingResponse(streaming_wrapper(), media_type="text/event-stream")

    except Exception as e:
        print("❌ Error global /streamtext:", e)

        async def error_stream():
            yield f"❌ Gagal memproses permintaan: {str(e)}\n"

        return StreamingResponse(error_stream(), media_type="text/plain", status_code=400)

@app.post("/streamer")
async def stream_responsesss(user_input: str):
    prompt = build_prompt(EXPERIENCE, user_input)

    return StreamingResponse(ai.stream_generate_text(prompt), media_type="text/plain")