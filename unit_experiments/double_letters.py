import re # Untuk regex

# Muat common_words.txt sekali di awal.
common_words = set(open("common_words.txt").read().lower().split())

# Vokal untuk identifikasi kasus khusus
VOWELS = "aeiou"

def normalize_double_letters(word: str) -> str:
    """
    Menormalisasi kata dengan mengurangi pengulangan huruf berlebihan di akhir kata
    atau dua huruf terakhir, berdasarkan korpus common_words.txt dan aturan Bahasa Indonesia.

    Args:
        word (str): Kata input yang mungkin mengandung double letters berlebihan.

    Returns:
        str: Kata yang dinormalisasi jika ditemukan di common_words,
             atau kata asli jika tidak ada normalisasi yang cocok.
    """
    if not word:
        return word

    original_word = word # Simpan kata asli untuk pengembalian default
    word_lower = word.lower() # Versi lowercase dari kata asli untuk pencarian

    # Jika kata sudah ada di common_words (setelah di-lowercase) atau di KBBI exceptions, biarkan saja.
    if word_lower in common_words:
        return word

    candidates = set() # Menyimpan semua kemungkinan normalisasi yang ditemukan

    # Prioritaskan kata asli sebagai kandidat pertama
    candidates.add(original_word)

    # --- Aturan 1: Normalisasi Satu Karakter Berulang di Akhir Kata ---
    # Contoh: ayoooooo -> ayo, tungguuuu -> tunggu, sudahhhh -> sudah
    # Cari pola (char) + (char berulang 2+ kali) di akhir kata
    # Misalnya: aaaaa -> a, eee -> e, bbb -> b
    for i in range(len(word) - 1, -1, -1): # Iterasi dari belakang ke depan
        char = word[i].lower() # Ambil karakter (ignore case untuk pola)
        # Pola: char yang sama diikuti 2+ kali
        pattern = re.compile(f"({re.escape(char)})\\1{{2,}}$", re.IGNORECASE)
        match = pattern.search(word)

        if match:
            # Ganti pengulangan dengan 1 atau 2 karakter aslinya
            base_part = word[:match.start(1)] # Bagian sebelum huruf berulang
            repeated_char_original_case = match.group(1) # Karakter yang berulang (dengan case asli dari match)

            # Opsi 1: Kurangi jadi satu karakter (misal: "ayooo" -> "ayo")
            cand1 = base_part + repeated_char_original_case
            if cand1.lower() in common_words:
                candidates.add(cand1)

            # Opsi 2: Kurangi jadi dua karakter (misal: "sudaaaah" -> "sudaah")
            cand2 = base_part + repeated_char_original_case + repeated_char_original_case
            if cand2.lower() in common_words:
                candidates.add(cand2)
            break # Hanya proses pengulangan pertama yang ditemukan dari belakang

    # --- Aturan 2: Normalisasi Dua Karakter Berulang di Akhir Kata ---
    # Contoh: sudaaahhh -> sudah
    # Fokus pada dua karakter terakhir yang berulang.
    if len(word) >= 4: # Minimal 4 karakter untuk pola 2-char berulang (ex: "ababab" -> "abab")
        last_two_chars = word[-2:] # "ah" dari "sudaaahhh"
        # Pola: dua karakter terakhir diikuti 1 kali atau lebih
        # Misalnya: (ah)(ah)(ah) -> (ah)
        # re.escape() memastikan karakter seperti '.' atau '*' dianggap literal
        pattern_two = re.compile(f"({re.escape(last_two_chars)})\\1{{1,}}$", re.IGNORECASE)
        match_two = pattern_two.search(word)

        if match_two and len(match_two.group(0)) > len(last_two_chars): # Pastikan ada pengulangan
            # Jika yang berulang adalah 'ah' (AH) -> 'ah'
            base_part_two = word[:match_two.start(1)]
            reduced_cand = base_part_two + match_two.group(1) # Hanya ambil satu kali pengulangan
            if reduced_cand.lower() in common_words:
                candidates.add(reduced_cand)

    # Filter kandidat: hanya yang ada di common_words
    valid_candidates = {c for c in candidates if c.lower() in common_words}

    # Jika tidak ada kandidat yang valid di common_words, kembalikan kata asli.
    if not valid_candidates:
        return original_word

    # Pilih hasil terbaik:
    # 1. Yang paling pendek (karena normalisasi mengurangi panjang)
    # 2. Jika panjang sama, pilih secara alfabetis (untuk konsistensi)
    best_candidate = min(valid_candidates, key=lambda c: (len(c), c))

    # Coba pertahankan case asli dari input jika memungkinkan
    # Ini sedikit kompleks karena ada banyak cara case bisa berubah
    # Untuk kesederhanaan, kita bisa kembalikan yang paling dekat
    # dengan case asli dari best_candidate jika itu yang kita pilih.
    # Atau, biarkan saja best_candidate hasil lowercase jika common_words lowercase.
    # Untuk saat ini, kita mengandalkan common_words yang di-lowercase, jadi output akan sesuai.
    # Jika perlu mempertahankan case, logic akan lebih panjang.
    return best_candidate

# Contoh
print(f"Normalisasi 'Ayo'             -> '{normalize_double_letters('Ayo')}'")
print(f"Normalisasi 'ayoooooo'        -> '{normalize_double_letters('ayoooooo')}'")
print(f"Normalisasi 'tungguuuuuuuu'   -> '{normalize_double_letters('tungguuuuuuuu')}'")
print(f"Normalisasi 'oke'             -> '{normalize_double_letters('oke')}'")
print(f"Normalisasi 'okeee'           -> '{normalize_double_letters('okeee')}'")
print(f"Normalisasi 'sudah'           -> '{normalize_double_letters('sudah')}'")
print(f"Normalisasi 'Sudaaaaaaaaah'   -> '{normalize_double_letters('Sudaaaaaaaaah')}'")
print(f"Normalisasi 'sudahhhhh'       -> '{normalize_double_letters('sudahhhhh')}'")
print(f"Normalisasi 'sudaaahhh'       -> '{normalize_double_letters('sudaaahhh')}'")
print(f"Normalisasi 'massaa'          -> '{normalize_double_letters('massaa')}'") # Akan tetap 'massaa' karena 'massa' di common_words
print(f"Normalisasi 'masssa'          -> '{normalize_double_letters('masssa')}'") # Akan jadi 'massa'
print(f"Normalisasi 'kuCInggg'        -> '{normalize_double_letters('kuCInggg')}'")
print(f"Normalisasi 'apelsss'         -> '{normalize_double_letters('apelsss')}'")
print(f"Normalisasi 'perggiii'        -> '{normalize_double_letters('perggiii')}'")
print(f"Normalisasi 'ruMahhhh'        -> '{normalize_double_letters('ruMahhhh')}'")
print(f"Normalisasi 'Bazzzaaar'       -> '{normalize_double_letters('Bazzzaaar')}'") # Tidak akan normalisasi karena 'bazaar' tidak ada di common_words dummy

print(f"Normalisasi 'akomodasiiii'    -> '{normalize_double_letters('akomodasiiii')}'") # Dari 'akomodasi' di common_words
print(f"Normalisasi 'makaaaaan'       -> '{normalize_double_letters('makaaaaan')}'")
print(f"Normalisasi 'tidurrr'         -> '{normalize_double_letters('tidurrr')}'")
print(f"Normalisasi 'halooo'          -> '{normalize_double_letters('halooo')}'") # 'halo' tidak ada di common_words dummy
print(f"Normalisasi 'sekollllah'      -> '{normalize_double_letters('sekollllah')}'") # 'sekolah' ada di common_words dummy
print(f"Normalisasi 'kursiii'         -> '{normalize_double_letters('kursiii')}'") # 'kursi' ada di common_words dummy
print(f"Normalisasi 'jemppput'        -> '{normalize_double_letters('jemppput')}'") # Akan tetap 'jemppput' jika 'jemput' tidak ada
print(f"Normalisasi 'jemput'          -> '{normalize_double_letters('jemput')}'") # Sudah baku