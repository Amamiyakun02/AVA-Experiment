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
    targets: List[Target],
    message: str,
    image_url: Optional[str] = None,
    filename: Optional[str] = None,
    schedule: int = 0,
    typing: bool = False,
    delay: str = "2",
    country_code: str = "62",
    followup: int = 0
) -> Optional[dict]:
    """
    Send WhatsApp message using Fonnte API (tanpa file lokal).

    Args:
        targets (List[Target]): List of target recipients
        message (str): Message to send
        image_url (Optional[str]): Image URL
        filename (Optional[str]): Optional filename (for URL-based file)
        schedule (int): Schedule timestamp
        typing (bool): Typing indicator
        delay (str): Delay in seconds
        country_code (str): Country code
        followup (int): Follow-up message ID

    Returns:
        dict: API response if successful, else None
    """

    url = 'https://api.fonnte.com/send'

    # Format target string
    target_str = ','.join([
        f"{t['phone']}|{t['name']}|{t.get('var1', '')}"
        for t in targets
    ])
    if not TOKEN:
        # Menambahkan penanganan jika token tidak ada
        print("Error: WHATSAPP_GATEWAY_TOKEN tidak ditemukan.")
        return {"status": False, "message": "Token otentikasi tidak dikonfigurasi."}

    payload = {
        'target': target_str,
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

    headers = {
        'Authorization': TOKEN
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Error sending message: {e}")
        return None
