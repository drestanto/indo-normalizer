import pandas as pd
import os

# File
csv_file = 'slangs.csv' # Nama file CSV Anda

# --- Memuat Peta Slang (Dilakukan sekali saat script dijalankan) ---
_slang_to_formal_map = {}
if os.path.exists(csv_file):
    try:
        df = pd.read_csv(csv_file)
        # Memastikan kolom 'slang' dan 'formal' ada sebelum membuat dictionary
        if 'slang' in df.columns and 'formal' in df.columns:
            _slang_to_formal_map = df.set_index('slang')['formal'].to_dict()
        else:
            # Peringatan jika kolom tidak ditemukan, tapi ini di luar fungsi slang_to_formal
            print(f"Peringatan: File CSV '{csv_file}' harus memiliki kolom 'slang' dan 'formal'. Map kosong.")
    except Exception as e:
        # Peringatan jika ada error saat memuat CSV, ini juga di luar fungsi
        print(f"Error saat memuat '{csv_file}': {e}. Map kosong.")
else:
    # Peringatan jika file CSV tidak ditemukan, ini juga di luar fungsi
    print(f"Peringatan: File CSV '{csv_file}' tidak ditemukan. Map slang kosong.")

def slang_to_formal(word):
    """
    Mengubah sebuah kata slang menjadi bentuk formalnya berdasarkan map yang dimuat dari CSV.
    Jika kata tidak ditemukan di map, kata aslinya akan dikembalikan.
    Fungsi ini TIDAK melakukan pencetakan output ke konsol.

    Args:
        word (str): Kata yang ingin dikonversi.

    Returns:
        str: Kata formal jika ditemukan, atau kata asli jika tidak.
    """
    # Menggunakan metode .get() dari dictionary
    # Jika 'word' ditemukan sebagai kunci, kembalikan nilainya (kata formal).
    # Jika tidak ditemukan, kembalikan 'word' itu sendiri (kata asli).
    return _slang_to_formal_map.get(word, word)

print(f"Mengkonversi 'netaas': {slang_to_formal('netaas')}")
print(f"Mengkonversi 'nyenengin': {slang_to_formal('nyenengin')}")
print(f"Mengkonversi 'ngikutin': {slang_to_formal('ngikutin')}")
print(f"Mengkonversi 'semangat': {slang_to_formal('semangat')}")
print(f"Mengkonversi 'nemuin': {slang_to_formal('nemuin')}")
print(f"Mengkonversi 'nemuken': {slang_to_formal('nemuken')}")
print(f"Mengkonversi 'nyebur': {slang_to_formal('nyebur')}")
print(f"Mengkonversi 'halo': {slang_to_formal('halo')}")
print(f"Mengkonversi 'GEMESIIN': {slang_to_formal('GEMESIIN')}")
print(f"Mengkonversi 'saranin': {slang_to_formal('saranin')}")
print(f"Mengkonversi 'nyamain': {slang_to_formal('nyamain')}")
print(f"Mengkonversi 'nyangka': {slang_to_formal('nyangka')}")