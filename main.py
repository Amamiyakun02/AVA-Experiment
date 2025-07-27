import os
import asyncio
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY tidak ditemukan di environment variables.")

genai.configure(api_key=api_key)

# Inisialisasi model
model = genai.GenerativeModel('gemini-2.5-flash')

# Inisialisasi FastAPI
app = FastAPI()

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User experience
EXPERIENCE = {
    "user_id": "amamiya",   
    "name": "Cristina",
    "personality": {
        "role": "Asisten Virtual",
        "style": "ramah, informatif, dingin, sedikit jenaka",
        "language": "Bahasa Indonesia"
    },
    "memory": []
}

def build_prompt(user_profile, user_input):
    """Bangun system prompt berdasarkan pengalaman dan input user."""
    return f"""
        Kamu adalah {user_profile["name"]}, seorang {user_profile["personality"]["role"]}.
        Gaya bicaramu: {user_profile["personality"]["style"]}.
        Gunakan {user_profile["personality"]["language"]}.
        Jawablah dengan cara alami dan sesuai konteks, tanpa mengulang perkenalan jika tidak diminta.
        
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
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        yield f"data: {json.dumps({'text': chunk.text})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(stream_gen(), media_type="text/event-stream")

    except Exception as e:
        return StreamingResponse(
            iter([f"data: {json.dumps({'error': str(e)})}\n\n"]),
            media_type="text/event-stream",
            status_code=400
        )
