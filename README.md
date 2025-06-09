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
# (TBD)
```

## License
MIT License