import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Pastikan kunci API sudah dimuat
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError(" tidak ditemukan. Pastikan Anda sudah mengaturnya di file .env atau variabel lingkungan.")

# 2. Inisialisasi Model Google Generative AI (Gemini)
# Kita akan menggunakan model 'gemini-pro' untuk text-based tasks
# Anda bisa mengatur 'temperature' untuk mengontrol kreativitas respons (0.0 sangat fokus, 1.0 lebih kreatif)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# 3. Buat Prompt Template
# Prompt Template membantu kita mendefinisikan struktur input untuk LLM.
# Di sini, kita mendefinisikan prompt yang mengambil satu variabel: 'topik'
prompt = ChatPromptTemplate.from_messages([
    ("system", "Anda adalah asisten AI yang sangat informatif dan membantu."),
    ("user", "Jelaskan konsep {topik} secara singkat dan mudah dimengerti.")
])

# 4. Buat Output Parser
# Output Parser mengubah output mentah dari LLM menjadi format yang lebih berguna.
# StrOutputParser akan mengonversi output menjadi string biasa.
output_parser = StrOutputParser()

# 5. Gabungkan komponen menjadi sebuah Chain
# Chain menggabungkan Prompt Template, LLM, dan Output Parser secara berurutan.
# operator '|' adalah cara yang disarankan di LangChain Expression Language (LCEL)
# untuk merangkai komponen.
chain = prompt | llm | output_parser

# 6. Jalankan Chain dengan input
print("--- Contoh 1: Menanyakan tentang Machine Learning ---")
response1 = chain.invoke({"topik": "Machine Learning"})
print(response1)

print("\n--- Contoh 2: Menanyakan tentang Energi Terbarukan ---")
response2 = chain.invoke({"topik": "Energi Terbarukan"})
print(response2)