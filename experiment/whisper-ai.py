import whisper

# Load model (pilih dari tiny, base, small, medium, large)
model = whisper.load_model("base")

# Transkripsi audio
print("Hasil transkripsi:")
result = model.transcribe("data/audio/common_voice_id_41927493.mp3", language="id")
print(result["text"])
