# indo-normalizer

**Indo-Normalizer** adalah library Python untuk *normalisasi kata-kata* dalam Bahasa Indonesia.  
Library ini mampu mengubah leetspeak menjadi kata asli, mengembangkan singkatan, dan memperbaiki kata tidak baku secara cerdas.

## Fitur

- Mengubah angka dan simbol dalam kata (leetspeak) ke bentuk huruf yang sesuai, contohnya:
  - `4l4y` → `alay`
  - `@ngk4` → `angka`
  - `3mpat` → `empat`
- Mengembangkan singkatan menjadi bentuk lengkap berdasarkan daftar kata umum, contohnya:
  - `blm` → `belum`
  - `yg` → `yang`
  - `dll` → `dan lain-lain`
- Memperbaiki kata tidak baku atau slang menjadi kata baku menggunakan *blacklist dictionary*, contohnya:
  - `belom` → `belum`
  - `telor` → `telur`
  - `gw` → `gua`
- Mempertahankan kapitalisasi sesuai konteks kalimat (awalan kalimat kapital, sisanya lowercase).

## Instalasi

```bash
pip install indo-normalizer
```

## Usage
```python
# usage_example.py
# Contoh Penggunaan Library Indo-Normalizer

# Mengimpor kelas Normalizer dari paket indo_normalizer.
# Pastikan Anda telah menginstal paket ini (pip install indo-normalizer)
# atau menjalankan skrip dari direktori root proyek Anda (python -m nama_paket.nama_modul).
from indo_normalizer import Normalizer

print("--- Memulai Demo Penggunaan Indo-Normalizer ---")

# 1. Inisialisasi Normalizer
# Objek Normalizer akan secara otomatis memuat data korpus dari folder 'corpus/'
# yang ada di dalam paket 'indo_normalizer' itu sendiri.
print("\n[Langkah 1] Menginisialisasi Normalizer...")
normalizer = Normalizer()
print("Normalizer berhasil diinisialisasi dan korpus telah dimuat.")

# 2. Contoh Teks untuk Normalisasi
# Kita akan menggunakan kalimat yang mengandung berbagai jenis anomali (slang, alay, pengulangan, singkatan, typo).
teks_asli = "H4loooo, akU k3ren bgt! g4j3 kyknya btw ini masssaaa aku s4raninnn kamu n4nti JEMpyUt aku yaa. pusinggg bgt!"
print(f"\n[Langkah 2] Teks Asli:\n'{teks_asli}'")

# 3. Normalisasi Teks
# Memanggil metode normalize_text untuk mengubah teks ke bentuk yang lebih standar.
# Metode ini juga mengembalikan jumlah perubahan yang terjadi untuk setiap kategori.
print("\n[Langkah 3] Melakukan Normalisasi Teks...")
teks_dinormalisasi, jumlah_perubahan = normalizer.normalize_text(teks_asli)

print(f"\n[Hasil Normalisasi] Teks Dinormalisasi:\n'{teks_dinormalisasi}'")
print("\n[Detail Perubahan] Jumlah Normalisasi Berdasarkan Kategori:")
for kategori, jumlah in jumlah_perubahan.items():
    print(f"- {kategori}: {jumlah} kali")

# 4. Menghitung Jumlah Kata Alay dan Slang
# Menggunakan fungsi count_alays dan count_slangs untuk mendapatkan total spesifik.
print("\n[Langkah 4] Menghitung Kata Alay dan Slang...")
total_alay = normalizer.count_alays(teks_asli)
total_slang = normalizer.count_slangs(teks_asli)

print(f"\n[Total Statistik] Total Kata Alay Terdeteksi: {total_alay}")
print(f"Total Kata Slang Terdeteksi: {total_slang}")

print("\n--- Demo Penggunaan Selesai ---")


```

## License
MIT License