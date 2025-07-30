import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from services.mongo_service import memory_col, chat_messages_col, chat_sessions_col
from utils.func_call.send_whatsapp import send_whatsapp_message
from services import AIEngine

# Load .env dan instruksi fungsi
load_dotenv()
with open("utils/func_call/func_instruction.json", "r") as f:
    FUNCTION_INSTRUCTION = json.load(f)

# Konfigurasi Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY tidak ditemukan di environment variables.")

model = AIEngine(api_key=api_key, tools=[{"function_declarations": [FUNCTION_INSTRUCTION]}])

# FastAPI App
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Profil Cristina
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
        - Jika pengguna berkata \"tolong kirim pesan ke Rika\", maka kamu bisa memanggil fungsi pengiriman WhatsApp.
        - Jika pengguna bertanya tentang Python atau AI, jawab dan bantu mereka dengan penjelasan dan kode jika perlu.

        Sekarang bantu pengguna di bawah ini:

        User:
        {user_input}

        {user_profile["name"]}:
    """

@app.post("/stream")
async def stream_response(request: Request):
    try:
        data = await request.json()
        messages = data.get("messages", [])
        if not messages:
            raise ValueError("messages tidak boleh kosong.")

        user_input = messages[-1]["content"]
        prompt = build_prompt(EXPERIENCE, user_input)

        def stream_gen():
            try:
                print("\n📨 Prompt terkirim ke model:")
                print(prompt)

                response = model.model.generate_content(prompt, stream=True)
                buffer = ""

                for chunk in response:
                    if hasattr(chunk, "parts") and chunk.parts:
                        part = chunk.parts[0]

                        if hasattr(part, "function_call") and part.function_call:
                            func_call = part.function_call
                            func_name = func_call.name
                            print("⚙️ Fungsi dipanggil:", func_name)

                            if func_call.args is None:
                                raise ValueError("Argumen function_call kosong.")
                            args = dict(func_call.args)

                            if func_name == "send_whatsapp_message":
                                try:
                                    result = send_whatsapp_message(**args)
                                    target_name = args.get("targets", [{}])[0].get("name", "pengguna")
                                    if result and result.get("status") is True:
                                        yield f"data: {json.dumps({'text': f'✅ Pesan berhasil dikirim ke {target_name}'})}\n\n"
                                    else:
                                        reason = result.get("message", "❌ Gagal mengirim pesan.")
                                        yield f"data: {json.dumps({'text': reason})}\n\n"
                                except Exception as func_err:
                                    yield f"data: {json.dumps({'text': f'❌ Gagal menjalankan fungsi: {str(func_err)}'})}\n\n"

                            post_response = model.model.generate_content([
                                {"role": "user", "parts": [user_input]},
                                {"role": "model", "parts": [part]}
                            ])
                            for post_part in post_response.parts:
                                if hasattr(post_part, "text"):
                                    yield f"data: {json.dumps({'text': post_part.text.strip()})}\n\n"
                            continue

                        elif hasattr(part, "text") and isinstance(part.text, str):
                            buffer += part.text

                    elif hasattr(chunk, "text") and isinstance(chunk.text, str):
                        buffer += chunk.text

                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if line.strip():
                            yield f"data: {json.dumps({'text': line.strip()})}\n\n"

                if buffer.strip():
                    yield f"data: {json.dumps({'text': buffer.strip()})}\n\n"

            except Exception as err:
                yield f"data: {json.dumps({'text': f'❌ Terjadi kesalahan dalam stream: {str(err)}'})}\n\n"

        return StreamingResponse(stream_gen(), media_type="text/event-stream")

    except Exception as e:
        print("❌ Error global /stream:", e)
        return StreamingResponse(
            iter([f"data: {json.dumps({'text': f'❌ Gagal memproses permintaan: {str(e)}'})}\n\n"]),
            media_type="text/event-stream",
            status_code=400
        )