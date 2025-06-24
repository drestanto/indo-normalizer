import csv
import os

# --- Konfigurasi ---
csv_file = 'slangs.csv' # Nama file CSV Anda

# --- Memuat Peta Slang (Dilakukan sekali saat script dijalankan) ---
_slang_to_formal_map = {}

if os.path.exists(csv_file):
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) # Baca baris header

            # Temukan indeks kolom 'slang' dan 'formal'
            try:
                slang_idx = header.index('slang')
                formal_idx = header.index('formal')
            except ValueError:
                print(f"Peringatan: File CSV '{csv_file}' harus memiliki kolom 'slang' dan 'formal'. Map kosong.")
                # Tetap lanjutkan dengan map kosong
                slang_idx = -1
                formal_idx = -1

            if slang_idx != -1 and formal_idx != -1:
                for row in reader:
                    if len(row) > max(slang_idx, formal_idx): # Pastikan baris cukup panjang
                        slang_word = row[slang_idx].strip()
                        formal_word = row[formal_idx].strip()
                        if slang_word: # Pastikan slang tidak kosong
                            _slang_to_formal_map[slang_word] = formal_word
            else:
                 print(f"Peringatan: Kolom 'slang' atau 'formal' tidak ditemukan di '{csv_file}'. Map kosong.")
    except Exception as e:
        print(f"Error saat memuat '{csv_file}': {e}. Map kosong.")
else:
    print(f"Peringatan: File CSV '{csv_file}' tidak ditemukan. Map slang kosong.")

def slang_to_formal(word: str) -> str:
    """
    Mengubah sebuah kata slang menjadi bentuk formalnya berdasarkan map yang dimuat dari CSV.
    Jika kata tidak ditemukan di map, kata aslinya akan dikembalikan.
    """
    return _slang_to_formal_map.get(word, word)

print(f"Mengkonversi 'netaas': {slang_to_formal('netaas')}")
print(f"Mengkonversi 'nyenengin': {slang_to_formal('nyenengin')}")
print(f"Mengkonversi 'ngikutin': {slang_to_formal('ngikutin')}")
print(f"Mengkonversi 'semangat': {slang_to_formal('semangat')}")
print(f"Mengkonversi 'nemuin': {slang_to_formal('nemuin')}")
print(f"Mengkonversi 'nemuken': {slang_to_formal('nemuken')}")
print(f"Mengkonversi 'nyebur': {slang_to_formal('nyebur')}")
print(f"Mengkonversi 'halooo': {slang_to_formal('halo')}")
print(f"Mengkonversi 'GEMESIIN': {slang_to_formal('GEMESIIN')}")
print(f"Mengkonversi 'SARANIN': {slang_to_formal('saranin')}")
print(f"Mengkonversi 'nyamain': {slang_to_formal('nyamain')}")
print(f"Mengkonversi 'nyangka': {slang_to_formal('nyangka')}")