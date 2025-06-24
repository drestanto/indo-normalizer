from rapidfuzz.distance import DamerauLevenshtein

common_words = set(open("corpus/common_words.txt").read().lower().split())

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

csv_file = 'slangs.csv'

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

def tokenize_text(s):
    """
    Tokenize string `s` dengan aturan:
    1. Digit 0-9 dan simbol ! @ $ dianggap “huruf”.
    2. Karakter yang bukan huruf dan bukan (1) menjadi satu token utuh
       bersama spasi di sekitarnya (contoh: ' , ', '... ').
    3. Digit yang diapit spasi → token sendiri; simbol ! @ $ yang diapit spasi
       → token ' ! ' / ' @ ' / ' $ '.
    4. Digit/simbol di antara huruf tetap di dalam kata (al4y, abi5, !slam).
    5. Simbol ! @ $ sesudah spasi dan sebelum huruf menjadi awalan kata ($aya).
    6. Tanda seru (!) setelah alfanumerik dan sebelum spasi berdiri sendiri
       (bag1! → ['bag1', '!']).
    7. Domain (contoh: unimelb.edu.au) harus jadi satu token utuh.
    8. Email (contoh: user@mail.id) juga harus jadi satu token utuh.
    """
    import re
    ascii_symbols = "!@$"
    tokens = []
    n = len(s)

    email_or_domain_pattern = re.compile(
        r"\b[\w\.-]+@[\w\.-]+\.\w+\b|\b[\w\-]+\.(?:[\w\-]+\.)*[\w\-]+\b"
    )
    domain_spans = {m.span(): m.group() for m in email_or_domain_pattern.finditer(s)}

    def is_letter(c):        return c.isalpha()
    def is_letterlike(c):    return c.isdigit() or c in ascii_symbols

    # sort by position
    domain_pos = sorted(domain_spans.items())
    idx = 0

    while idx < n:
        # domain/email check
        matched = False
        for (start, end), val in domain_pos:
            if idx == start:
                tokens.append(val)
                idx = end
                matched = True
                break
        if matched:
            continue

        # aturan 3: ' ! ' / ' @ ' / ' $ '
        if idx + 2 < n and s[idx] == " " and s[idx+1] in ascii_symbols and s[idx+2] == " ":
            tokens.append(s[idx:idx+3])
            idx += 3
            continue

        c = s[idx]

        # kandidat kata (huruf, digit, simbol)
        if is_letter(c) or is_letterlike(c):
            if c.isdigit() and (idx == 0 or s[idx-1] == " ") and (idx+1 == n or s[idx+1] == " "):
                tokens.append(c)
                idx += 1
                continue
            if c == "!" and idx > 0 and not s[idx-1].isspace() and (idx+1 == n or s[idx+1].isspace()):
                tokens.append("!")
                idx += 1
                continue
            j = idx
            while j < n:
                cj = s[j]
                if cj == "!" and j > idx and not s[j-1].isspace() and (j+1 == n or s[j+1].isspace()):
                    break
                if is_letter(cj) or is_letterlike(cj):
                    j += 1
                else:
                    break
            tokens.append(s[idx:j])
            idx = j
            continue

        # aturan 2: run spasi/punktuasi
        j = idx
        while j < n and not (is_letter(s[j]) or is_letterlike(s[j])):
            j += 1
        tokens.append(s[idx:j])
        idx = j

    return tokens

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

def is_abbreviation(abbr, word):
    if len(abbr) < (len(word) + 1) // 2:
        return False
    i = 0
    for c in word:
        if i < len(abbr) and abbr[i] == c:
            i += 1
    return i == len(abbr)

def slang_to_formal(word):
    """
    Mengubah sebuah kata slang menjadi bentuk formalnya berdasarkan map yang dimuat dari CSV.
    Jika kata tidak ditemukan di map, kata aslinya akan dikembalikan.
    """
    return _slang_to_formal_map.get(word, word)

def is_typo(word, target):
    """
    Memeriksa apakah 'word' adalah 'nearmiss' dari 'target'
    dengan tepat satu operasi (sisip, hapus, substitusi, transposisi).
    """
    distance = DamerauLevenshtein.distance(word, target)
    return distance == 1 or distance == 2