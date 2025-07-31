# from google import genai
# client = genai.Client()
#
# experience = {
#   "user_id": "amamiya",
#   "name": "Amamiya",
#   "personality": {
#     "role": "Assistant",
#     "style": "friendly, informative, slightly playful",
#     "language": "Indonesian"
#   },
#   "memory": [
#     "Pengguna sedang membangun proyek AVA (Anime Virtual Assistant)",
#     "AVA menggunakan whisper.cpp untuk STT dan akan digunakan di desktop dulu",
#     "Model LLM akan digunakan untuk text-generation berbasis karakter anime",
#     "Pengguna sangat menyukai teknologi open-source dan privasi lokal"
#   ]
# }
#
# def build_prompt(user_profile, memory, user_input):
#     system_prompt = f"""
#     Kamu adalah {user_profile["personality"]["role"]}.
#     Gaya kamu: {user_profile["personality"]["style"]}.
#     Gunakan Bahasa: {user_profile["personality"]["language"]}.
#
#     Berikut memori pengguna:
#     {chr(10).join(f"- {m}" for m in memory)}
#
#     ---
#     """
#     full_prompt = system_prompt + f"USER:\n{user_input}\n"
#     return full_prompt
#
# final_prompt = build_prompt(experience, experience["memory"], "apakah model gemini 2.5 pro ini dapat digunakan oleh pengembang lain melalui api secara gratis")
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=final_prompt,
# )
#
# print(response.text)
import os
from google import genai
from google.genai import types
import asyncio
import requests
import json
from dotenv import load_dotenv
import os
from typing import List, Optional, TypedDict

from pathlib import Path  # Masih bisa digunakan jika perlu validasi jalur gambar
client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

load_dotenv()
TOKEN = os.getenv("WHATSAPP_GATEWAY_TOKEN")

class Target(TypedDict):
    phone: str
    name: str
    var1: Optional[str]

def send_whatsapp_message(
    phone: str,
    name: str,
    message: str,
    var1: Optional[str] = "",
    image_url: Optional[str] = None,
    filename: Optional[str] = None,
    schedule: int = 0,
    typing: bool = False,
    delay: str = "2",
    country_code: str = "62",
    followup: int = 0
) -> str:
    """
    Kirim satu pesan WhatsApp ke 1 nomor.
    """

    if not TOKEN:
        return "Token tidak ditemukan."

    payload = {
        'target': f"{phone}|{name}|{var1}",
        'message': message,
        'schedule': schedule,
        'typing': typing,
        'delay': delay,
        'countryCode': country_code,
        'followup': followup
    }

    if image_url:
        payload['url'] = image_url
    if filename:
        payload['filename'] = filename

    try:
        response = requests.post(
            "https://api.fonnte.com/send",
            data=payload,
            headers={'Authorization': TOKEN}
        )
        response.raise_for_status()
        return f"Status: {response.status_code}, Response: {response.json()}"

    except requests.RequestException as e:
        return f"Error: {e}"
def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
      location: The city and state, e.g. San Francisco, CA
    """
    return 'sunny'


response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
    ),
)


async def main():
    async for chunk in await client.aio.models.generate_content_stream(
        model='gemini-2.5-flash',
        contents='kirimkan pesan ke kurdianto melalui nomor whatsapp berikut 082253558489 dengan pesan aku adalah sebuah asisten virtualnya amamiya, lalu kamu kirimkan saya info terkirim dan berikan saya kode program untuk perhitungan vektor dengan numpy',
        config=types.GenerateContentConfig(
            tools=[send_whatsapp_message],
        )):
        print(chunk.text, end='')


if __name__ == "__main__":
    asyncio.run(main())
