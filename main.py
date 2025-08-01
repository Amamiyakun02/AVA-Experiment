import os
import json
from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from services import AIEngine
from memory import MemoryManager
from utils import  build_prompt

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

        # === Ambil memory dari Mongo (user + assistant) ===
        context_memories = memory.recall_mongo(top_k=6)
        print("[MEMORY CONTEXT]", context_memories)

        # === Gabungkan memory + pesan baru dari user ===
        prompt_blocks = []

        # Tambahkan dari MongoDB memory
        prompt_blocks += context_memories

        # Tambahkan dari pesan baru
        for msg in messages:
            role = msg.role.lower()
            label = "User" if role == "user" else ASSISTANT["name"]
            prompt_blocks.append(f"{label}:\n{msg.content}")

        # Gabungkan semua blok menjadi input untuk prompt
        full_input = "\n\n".join(prompt_blocks)
        prompt = build_prompt(ASSISTANT, full_input)

        print("[FINAL PROMPT]")
        print(prompt)

        # === Streaming ke LLM ===
        async def streaming_wrapper():
            full_response = ""
            try:
                async for chunk in ai.stream_generate_text(prompt):
                    # Ekstrak teks dari chunk
                    if chunk.startswith("data:"):
                        try:
                            payload = json.loads(chunk.replace("data: ", "").strip())
                            text_part = payload.get("text", "")
                        except json.JSONDecodeError:
                            text_part = chunk  # fallback
                    else:
                        text_part = chunk  # fallback

                    full_response += text_part
                    yield chunk  # tetap kirim streaming mentah ke klien
            finally:
                # Simpan semua pesan input user
                for msg in messages:
                    memory.store_memory(msg.content, source=msg.role)

                # Simpan output dari asisten (sudah dibersihkan)
                memory.store_memory(full_response.strip(), source="assistant")

        return StreamingResponse(streaming_wrapper(), media_type="text/event-stream")

    except Exception as e:
        return {"error": str(e)}

@app.post("/streamer")
async def stream_responsesss(user_input: str):
    prompt = build_prompt(ASSISTANT, user_input)

    return StreamingResponse(ai.stream_generate_text(prompt), media_type="text/plain")