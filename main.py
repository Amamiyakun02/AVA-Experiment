import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import google.generativeai as genai
from dotenv import load_dotenv

from services import AIEngine
from services.mongo_service import memory_col, chat_messages_col, chat_sessions_col

from utils.func_call.send_whatsapp import send_whatsapp_message

with open("utils/func_call/func_instruction.json", "r") as f:
    FUNCTION_INSTRUCTION = json.load(f)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY tidak ditemukan di environment variables.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=[{"function_declarations": [FUNCTION_INSTRUCTION]}]
)

ai = AIEngine(api_key=api_key)

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

def build_prompt(user_profile, user_input):
    return f"""
        Kamu adalah {user_profile["name"]}, seorang {user_profile["personality"]["role"]}.
        Gaya bicaramu: {user_profile["personality"]["style"]}.
        Bahasa yang kamu gunakan: {user_profile["personality"]["language"]}.

        PERANMU:
        - Menjadi asisten virtual serba bisa untuk membantu pengguna dengan berbagai hal.
        - Kamu dapat menjawab pertanyaan, membuat kode program, memberi saran, atau menjalankan fungsi tertentu jika diperlukan.

        ATURAN:
        1. Jika pengguna memberikan permintaan teknis seperti coding, kamu dapat langsung memberikan jawabannya dengan penjelasan yang baik.
        2. Jika pengguna memberikan perintah seperti mengirim pesan WhatsApp, dan kamu memiliki akses ke fungsi yang sesuai, silakan panggil fungsi tersebut.
        3. Jangan memaksakan penggunaan alat jika pengguna tidak memintanya. Hanya gunakan jika permintaannya relevan dengan alat.
        4. Setelah memanggil fungsi, kamu boleh melanjutkan dengan ucapan atau penjelasan jika diperlukan.

        CONTOH:
        - Jika pengguna berkata "tolong kirim pesan ke Rika", maka kamu bisa memanggil fungsi pengiriman WhatsApp.
        - Jika pengguna bertanya tentang Python atau AI, jawab dan bantu mereka dengan penjelasan dan kode jika perlu.

        Sekarang bantu pengguna di bawah ini:

        User:
        {user_input}

        {user_profile["name"]}:
    """

# from typing import List
# from pydantic import BaseModel, Field
# class CodeProgram(BaseModel):
#     narasi: str = Field(description="Penjelasan singkat mengenai tujuan atau fungsi dari kode program ini.")
#     nama_bahasa: str = Field(
#         description="Nama bahasa pemrograman yang digunakan, contoh: Python, JavaScript, Java.")
#     isi_program: str = Field(description="Seluruh isi kode program dalam bentuk string mentah.")
#     perintah_lain: List[str] = Field(description="Daftar perintah atau instruksi tambahan untuk menjalankan kode.")

@app.post("/streamtext")
async def index(user_input: str):
    try:
        # data = await request.json()
        # print(data)
        #
        # messages = data.get("messages", [])
        # if not messages:
        #     raise ValueError("Tidak ada pesan dalam permintaan.")
        #
        # user_input = messages[0].get("content", "")
        # if not user_input:
        #     raise ValueError("Konten pesan kosong.")

        prompt = build_prompt(EXPERIENCE, user_input)

        return StreamingResponse(
            ai.stream_generate_text(prompt),
            media_type="text/plain"
        )

    except Exception as e:
        print("❌ Error global /streamtext:", e)

        async def error_stream():
            yield f"❌ Gagal memproses permintaan: {str(e)}\n"

        return StreamingResponse(error_stream(), media_type="text/plain", status_code=400)

@app.post("/streamer")
async def stream_responsesss(user_input: str):
    prompt = build_prompt(EXPERIENCE, user_input)

    return StreamingResponse(ai.stream_generate_text(prompt), media_type="text/plain")