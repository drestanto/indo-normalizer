def normalize_repetitions(word):
    """
    Menormalisasi kata dengan mengurangi pengulangan huruf yang berlebihan.
    Jika sebuah karakter berulang 3 kali atau lebih berturut-turut,
    pengulangan tersebut akan dipotong menjadi hanya satu instance dari karakter tersebut.
    Pengulangan 2 kali atau kurang akan dibiarkan.

    Args:
        word (str): Kata input yang mungkin mengandung pengulangan huruf berlebihan.

    Returns:
        str: Kata yang telah dinormalisasi.
    """
    if not word:
        return word

    result_word = ""
    i = 0
    while i < len(word):
        result_word += word[i]  # Tambahkan karakter saat ini ke hasil
        count = 1
        # Hitung berapa kali karakter ini berulang (case-insensitive)
        while i + count < len(word) and word[i + count].lower() == word[i].lower():
            count += 1

        # Jika karakter berulang 3 kali atau lebih, lewati semua pengulangan
        # (karena kita sudah menambahkan 1 instance di awal loop)
        if count >= 3:
            i += count
        else:
            # Jika berulang 2 kali atau kurang, pindah ke karakter berikutnya
            # (kita hanya bergerak 1 karakter karena pengulangan <= 2 tetap dibiarkan)
            i += 1
    return result_word

# Contoh
print(f"Normalisasi 'Ayo'             -> '{normalize_repetitions('Ayo')}'")
print(f"Normalisasi 'ayoooooo'        -> '{normalize_repetitions('ayoooooo')}'")
print(f"Normalisasi 'tungguuuuuuuu'   -> '{normalize_repetitions('tungguuuuuuuu')}'")
print(f"Normalisasi 'oke'             -> '{normalize_repetitions('oke')}'")
print(f"Normalisasi 'okeee'           -> '{normalize_repetitions('okeee')}'")
print(f"Normalisasi 'sudah'           -> '{normalize_repetitions('sudah')}'")
print(f"Normalisasi 'sudaaaaaaaaah'   -> '{normalize_repetitions('sudaaaaaaaaah')}'")
print(f"Normalisasi 'sudahhhhh'       -> '{normalize_repetitions('sudahhhhh')}'")
print(f"Normalisasi 'sudaaahhh'       -> '{normalize_repetitions('sudaaahhh')}'")
print(f"Normalisasi 'massa'           -> '{normalize_repetitions('massa')}'")
print(f"Normalisasi 'masssa'          -> '{normalize_repetitions('masssa')}'")
print(f"Normalisasi 'masssaa'         -> '{normalize_repetitions('masssaa')}'")
print(f"Normalisasi 'kucinggg'        -> '{normalize_repetitions('kucinggg')}'")
print(f"Normalisasi 'apelsss'         -> '{normalize_repetitions('apelsss')}'")
print(f"Normalisasi 'perggiii'        -> '{normalize_repetitions('perggiii')}'")
print(f"Normalisasi 'ruMahhhh'        -> '{normalize_repetitions('ruMahhhh')}'")
print(f"Normalisasi 'Bazzzaaar'       -> '{normalize_repetitions('Bazzzaaar')}'")
print(f"Normalisasi 'akomodasiiii'    -> '{normalize_repetitions('akomodasiiii')}'")
print(f"Normalisasi 'makaaaaan'       -> '{normalize_repetitions('makaaaaan')}'")
print(f"Normalisasi 'tidurrr'         -> '{normalize_repetitions('tidurrr')}'")
print(f"Normalisasi 'halooo'          -> '{normalize_repetitions('halooo')}'")
print(f"Normalisasi 'sekollllah'      -> '{normalize_repetitions('sekollllah')}'")
print(f"Normalisasi 'kursiii'         -> '{normalize_repetitions('kursiii')}'")
print(f"Normalisasi 'jemppput'        -> '{normalize_repetitions('jemppput')}'")
print(f"Normalisasi 'jemput'          -> '{normalize_repetitions('jemput')}'")
print(f"Normalisasi 'Miiiiisssaaaaallll' -> '{normalize_repetitions('Miiiiisssaaaaallll')}'")
print(f"Normalisasi 'hahahahaaaaa' -> '{normalize_repetitions('hahahahaaaaa')}'")
print(f"Normalisasi 'wowowowooooo' -> '{normalize_repetitions('wowowowooooo')}'")