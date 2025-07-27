from google import genai
client = genai.Client()

experience = {
  "user_id": "amamiya",
  "name": "Amamiya",
  "personality": {
    "role": "Assistant",
    "style": "friendly, informative, slightly playful",
    "language": "Indonesian"
  },
  "memory": [
    "Pengguna sedang membangun proyek AVA (Anime Virtual Assistant)",
    "AVA menggunakan whisper.cpp untuk STT dan akan digunakan di desktop dulu",
    "Model LLM akan digunakan untuk text-generation berbasis karakter anime",
    "Pengguna sangat menyukai teknologi open-source dan privasi lokal"
  ]
}

def build_prompt(user_profile, memory, user_input):
    system_prompt = f"""
    Kamu adalah {user_profile["personality"]["role"]}.
    Gaya kamu: {user_profile["personality"]["style"]}.
    Gunakan Bahasa: {user_profile["personality"]["language"]}.
    
    Berikut memori pengguna:
    {chr(10).join(f"- {m}" for m in memory)}
    
    ---
    """
    full_prompt = system_prompt + f"USER:\n{user_input}\n"
    return full_prompt

final_prompt = build_prompt(experience, experience["memory"], "apakah model gemini 2.5 pro ini dapat digunakan oleh pengembang lain melalui api secara gratis")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=final_prompt,
)

print(response.text)
