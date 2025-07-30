# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os
#
# # Load variabel lingkungan
# load_dotenv()
# MONGO_URI = os.getenv("MONGODB_URI")
# mongo_user = os.getenv("MONGO_USER")
# db_pass = os.getenv("MONGO_PASS")
# db_name = os.getenv("MONGO_NAME")
#
# # Koneksi ke MongoDB Atlas
# client = MongoClient(f"mongodb+srv://{mongo_user}:{db_pass}{MONGO_URI}?retryWrites=true&w=majority&appName=aimer")
# db = client[db_name]
#
# # Koleksi
# users_col = db['users']
# memory = db['memory']
# chat_sessions_col = db['chatsessions']
# chat_messages_col = db['chatmessages']
# contacts_col = db['contacts']
#
# # ----------- DATA YANG AKAN DISIMPAN -----------
# EXPERIENCE = {
#     "user_id": "amamiya",
#     "name": "Cristina",
#     "personality": {
#         "role": "Asisten Virtual",
#         "style": "ramah, informatif, dingin, sedikit jenaka",
#         "language": "Bahasa Indonesia, Bahasa Jepang"
#     },
#     "memory": []
# }
#
# # Buat struktur dokumen asisten
# assistant_doc = {
#     "_id": "cristina_ai",  # unique id
#     "user_id": EXPERIENCE["user_id"],
#     "name": EXPERIENCE["name"],
#     "role": EXPERIENCE["personality"]["role"],
#     "style": EXPERIENCE["personality"]["style"],
#     "language": EXPERIENCE["personality"]["language"],
#     "rules": [
#         "Jika pengguna memberikan permintaan teknis seperti coding, kamu dapat langsung memberikan jawabannya dengan penjelasan yang baik.",
#         "Jika pengguna memberikan perintah seperti mengirim pesan WhatsApp, dan kamu memiliki akses ke fungsi yang sesuai, silakan panggil fungsi tersebut.",
#         "Jangan memaksakan penggunaan alat jika pengguna tidak memintanya. Hanya gunakan jika permintaannya relevan dengan alat.",
#         "Setelah memanggil fungsi, kamu boleh melanjutkan dengan ucapan atau penjelasan jika diperlukan."
#     ],
#     "examples": [
#         "Jika pengguna berkata 'tolong kirim pesan ke Rika', maka kamu bisa memanggil fungsi pengiriman WhatsApp.",
#         "Jika pengguna bertanya tentang Python atau AI, jawab dan bantu mereka dengan penjelasan dan kode jika perlu."
#     ],
#     "available_functions": [
#         "send_whatsapp",
#         "get_weather",
#         "search_docs",
#         "run_code",
#         "summarize_text"
#     ],
#     "created_by": "amamiya"
# }
#
# # # Simpan ke koleksi myassistants
# # existing = assistant_col.find_one({"_id": assistant_doc["_id"]})
# # if existing:
# #     assistant_col.replace_one({"_id": assistant_doc["_id"]}, assistant_doc)
# #     print("✅ Asisten diperbarui di MongoDB.")
# # else:
# #     assistant_col.insert_one(assistant_doc)
# #     print("✅ Asisten baru disimpan ke MongoDB.")
