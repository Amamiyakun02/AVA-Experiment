from pymongo.collection import Collection
from services.collection import contacts_col

def get_contact_by_name(name: str) -> dict | None:
    """
    Mengambil data kontak dari koleksi MongoDB berdasarkan nama,
    dengan pencocokan case-insensitive (tidak sensitif huruf besar/kecil).

    Args:
        collection (Collection): Objek koleksi MongoDB tempat menyimpan data kontak(Opsional).
        name (str): Nama kontak yang ingin dicari.

    Returns:
        dict | None: Dokumen kontak yang ditemukan, atau None jika tidak ditemukan.

    Contoh:
        contact = get_contact_by_name(name=rahman")
        if contact:
            print(contact["number_phone"])
    """
    if not name:
        return None

    # Pencarian menggunakan regex agar tidak case-sensitive dan cocok persis
    return contacts_col.find_one(
        {"name": {"$regex": f"^{name}$", "$options": "i"}},
        {"_id": 0}  # ini projection untuk menyembunyikan _id
    )
