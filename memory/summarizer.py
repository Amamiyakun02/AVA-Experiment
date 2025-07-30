from typing import List
from google import genai
client = genai.Client()

def summarize_memory(chunks: List[str]) -> str:
    """
    Meringkas daftar chat atau teks menjadi satu ringkasan pendek.
    """
    joined_text = "\n".join(f"- {line}" for line in chunks)

    prompt = f"""
    Berikut adalah potongan percakapan pengguna:
    {joined_text}

    Buat ringkasan singkat (1–2 kalimat) dari isi percakapan di atas.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()
