from elevenlabs.client import ElevenLabs
import os
# Inisialisasi client
client = ElevenLabs(
    api_key=os.getenv("ELEVEN_API_KEY"),
)

# Konversi teks menjadi audio
audio_generator = client.text_to_speech.convert(
    text="Selamat Pagi Tuan Amamiya, Hari ini saya siap untuk menjalankan perintah anda.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Gabungkan hasil generator menjadi satu objek bytes
audio_bytes = b''.join(audio_generator)

# Simpan ke file MP3
with open("output/voice/ele.mp3", "wb") as f:
    f.write(audio_bytes)

print("✅ Audio berhasil disimpan sebagai ele.mp3")
