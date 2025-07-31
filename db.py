import os
from services import CodeProgram, AIEngine

ai = AIEngine(api_key=os.getenv("GEMINI_API_KEY"))

result = ai.generate_structured(
    prompt="Buatkan saya kode program Python sederhana untuk menghitung faktorial sebuah angka.",
    schema=CodeProgram
)

if isinstance(result, CodeProgram):
    print(f"Narasi: {result.narasi}")
    print(f"Bahasa: {result.nama_bahasa}")
    print(f"Kode Program:\n{result.isi_program}")
    print(f"Instruksi Tambahan: {', '.join(result.perintah_lain)}")
else:
    print(result)  # error message or fallback text
