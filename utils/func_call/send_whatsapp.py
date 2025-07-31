import requests
import json
from dotenv import load_dotenv
import os
from typing import List, Optional, TypedDict

from pathlib import Path  # Masih bisa digunakan jika perlu validasi jalur gambar

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
