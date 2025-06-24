# Normalize to lowercase and store as set
common_words = set(open("common_words.txt").read().lower().split())

LEET_MAP = {
    "!": ["i", "l"],
    "1": ["i", "l"],
    "@": ["a"],
    "4": ["A"], # Dipertahankan sebagai 'A' besar
    "2": ["z"],
    "3": ["E"], # Dipertahankan sebagai 'E' besar
    "$": ["s"],
    "5": ["s"],
    "6": ["G"], # Dipertahankan sebagai 'G' besar
    "7": ["j", "T"], # Dipertahankan sebagai 'T' besar
    "8": ["B"], # Dipertahankan sebagai 'B' besar
    "9": ["g"],
    "0": ["o", "O"] # Dipertahankan sebagai 'o' dan 'O'
}

def normalize_leet(word):
    # Jika kata sudah murni alfabet, kembalikan seperti aslinya (tidak diubah case-nya)
    if word.isalpha():
        return word

    has_trailing_2 = word.endswith("2")
    core_word = word[:-1] if has_trailing_2 else word

    results = set() # Untuk menyimpan hasil yang ditemukan, dengan case yang sudah terbentuk

    def backtrack(index, path):
        if index == len(core_word):
            candidate = ''.join(path)
            # Lakukan pemeriksaan case-insensitive terhadap common_words
            if candidate.lower() in common_words:
                results.add(candidate)
            return

        char = core_word[index]
        # Periksa apakah karakter saat ini adalah kunci di LEET_MAP (pencarian kunci peka kasus)
        if char in LEET_MAP:
            for sub in LEET_MAP[char]:
                # Gunakan substitusi dari LEET_MAP persis seperti adanya (termasuk case-nya)
                path.append(sub)
                backtrack(index + 1, path)
                path.pop()
        else:
            # Jika bukan kunci LEET_MAP, pertahankan karakter aslinya (dengan case aslinya)
            path.append(char)
            backtrack(index + 1, path)
            path.pop()

    backtrack(0, [])

    if not results:
        return word

    # Pilih hasil terbaik: yang terpendek, lalu secara alfabetis (untuk konsistensi)
    best = sorted(list(results), key=lambda w: (len(w), w))[0]
    return f"{best}-{best}" if has_trailing_2 else best

print("g4nt3ng -> " + normalize_leet("g4nt3ng"))
print("g4nt3n62 -> " + normalize_leet("g4nt3n62"))
print("aji7 -> " + normalize_leet("aji7"))
print("aji72 -> " + normalize_leet("aji72"))
print("tol0l -> " + normalize_leet("tol0l"))
print("ra7in -> " + normalize_leet("ra7in"))
print("8aik -> " + normalize_leet("8aik"))
print("8a7ik -> " + normalize_leet("8a7ik"))
print("G4NT3NG -> " + normalize_leet("G4NT3NG"))
print("tOl0l -> " + normalize_leet("tOl0l"))
print("coba -> " + normalize_leet("coba"))
print("APAkah -> " + normalize_leet("APAkah"))
print("aman1 -> " + normalize_leet("aman1"))