# from google import genai
# import whisper
# from elevenlabs.client import ElevenLabs
#
# # INITIAL MODEL
# client = genai.Client()
# # Inisialisasi client
# tts_client = ElevenLabs(
#     api_key="sk_a27535a4656f1a52007d41c701f1dad87c0f51ea061b328b"
# )
#
# # Load model (pilih dari tiny, base, small, medium, large)
# model = whisper.load_model("base")
#
# # SPEECH TO TEXT (STT)
# print("Hasil transkripsi:")
# result = model.transcribe("data/audio/common_voice_id_41927490.mp3", language="id")
# print(result["text"])
#
# # LLM GOOGLE GEMINI
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=result["text"],
# )
# print(response.text)
#
# # TEXT TO SPEECH (TTS)
# # Konversi teks menjadi audio
# audio_generator = tts_client.text_to_speech.convert(
#     text="Selamat Pagi Tuan Amamiya, Hari ini saya siap untuk menjalankan perintah anda.",
#     voice_id="JBFqnCBsd6RMkjVDRZzb",
#     model_id="eleven_multilingual_v2",
#     output_format="mp3_44100_128",
# )
#
# # Gabungkan hasil generator menjadi satu objek bytes
# audio_bytes = b''.join(audio_generator)
#
# # Simpan ke file MP3
# with open("output/voice/audio.mp3", "wb") as f:
#     f.write(audio_bytes)
#
# print("✅ Audio berhasil disimpan sebagai output.mp3")
from memory import MemoryManager

memory = MemoryManager(user_id="amamiya")
memory.store_memory("Hari ini aku pergi ke pasar membeli apel.")
print(memory.recall("belanja buah", top_k=2))
