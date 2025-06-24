# LEET_MAP baru dan lebih sederhana untuk fungsi normalisasi paksa.
# Setiap kunci hanya memiliki satu nilai pengganti untuk prioritas.
FORCED_LEET_MAP = {
    "!": "i",
    "1": "i",
    "@": "a",
    "4": "A",
    "2": "z",
    "3": "E",
    "$": "s",
    "5": "s",
    "6": "G",
    "7": "j",
    "8": "B",
    "9": "g",
    "0": "o"
}

def normalize_forced_leet(word):
    """
    Menormalisasi kata dengan mengganti angka/simbol menggunakan LEET_MAP paksa,
    tanpa memeriksa corpus. Jika ada banyak kemungkinan, akan memilih opsi pertama.
    Huruf alfabet dalam input akan mempertahankan casing aslinya.
    """
    normalized_chars = []
    for char in word:
        # Periksa apakah karakter ada di FORCED_LEET_MAP.
        # Pencarian dilakukan secara case-sensitive pada kunci map.
        if char in FORCED_LEET_MAP:
            # Gunakan substitusi langsung dari map.
            normalized_chars.append(FORCED_LEET_MAP[char])
        elif char.lower() in FORCED_LEET_MAP and char.isalpha():
            # Jika karakter alfabetik dan versi lowercase-nya ada di map,
            # contoh: jika 'A' dimasukkan dan 'a' ada di map, maka akan mencoba mengganti.
            # Namun, untuk 'forced_leet', kita umumnya hanya fokus pada angka/simbol yang di-leet.
            # Jika 'A' bukan kunci leet, ia tetap 'A'.
            normalized_chars.append(char)
        else:
            # Jika bukan kunci di map, pertahankan karakter aslinya (dengan casing aslinya).
            normalized_chars.append(char)
            
    return "".join(normalized_chars)

print("g4nt3ng (forced) -> " + normalize_forced_leet("g4nt3ng"))
print("g4nt3n62 (forced) -> " + normalize_forced_leet("g4nt3n62"))
print("aji7 (forced) -> " + normalize_forced_leet("aji7"))
print("aji72 (forced) -> " + normalize_forced_leet("aji72"))
print("tol0l (forced) -> " + normalize_forced_leet("tol0l"))
print("ra7in (forced) -> " + normalize_forced_leet("ra7in"))
print("8aik (forced) -> " + normalize_forced_leet("8aik"))
print("8a7ik (forced) -> " + normalize_forced_leet("8a7ik"))
print("G4NT3NG (forced) -> " + normalize_forced_leet("G4NT3NG"))
print("tOl0l (forced) -> " + normalize_forced_leet("tOl0l"))