import re
import pandas as pd
import os
import collections

# Mengimpor semua fungsi dari file functions.py (impor relatif)
from .functions import ( # Perhatikan titik (.) di depan `functions`
    tokenize_text,
    normalize_repetitions,
    is_abbreviation,
    normalize_leet,
    normalize_forced_leet,
    slang_to_formal,
    is_typo
)

class Normalizer:
    """
    Kelas untuk menormalisasi teks Bahasa Indonesia dan menghitung statistik terkait.
    Memuat korpus dari common_words.txt dan slangs.csv.
    """
    _COMMON_WORDS = set()
    _SLANG_TO_FORMAL_MAP = {}

    def __init__(self):
        """
        Inisialisasi Normalizer dan memuat korpus yang diperlukan.
        File korpus diasumsikan berada di subfolder 'corpus/' di dalam package 'text_normalizer'.
        """
        # Dapatkan direktori dari file Normalizer.py ini
        base_dir = os.path.dirname(os.path.abspath(__file__))
        corpus_dir = os.path.join(base_dir, 'corpus')

        self.common_words_path = os.path.join(corpus_dir, 'common_words.txt')
        self.slangs_csv_path = os.path.join(corpus_dir, 'slangs.csv')

        # Load COMMON_WORDS
        try:
            with open(self.common_words_path, "r", encoding="utf-8") as f:
                self._COMMON_WORDS = set(f.read().lower().split())
        except FileNotFoundError:
            print(f"WARNING: {self.common_words_path} not found. Some normalization features may not work.")
            self._COMMON_WORDS = set()
        except Exception as e:
            print(f"WARNING: Error loading {self.common_words_path}: {e}. Some normalization features may not work.")
            self._COMMON_WORDS = set()

        # Load SLANG_TO_FORMAL_MAP
        if os.path.exists(self.slangs_csv_path):
            try:
                df_slang = pd.read_csv(self.slangs_csv_path)
                if 'slang' in df_slang.columns and 'formal' in df_slang.columns:
                    # Pastikan kunci slang diubah ke lowercase jika fungsi slang_to_formal membutuhkannya
                    self._SLANG_TO_FORMAL_MAP = df_slang.set_index('slang')['formal'].to_dict()
                else:
                    print(f"WARNING: '{self.slangs_csv_path}' must have 'slang' and 'formal' columns. Slang map empty.")
            except Exception as e:
                print(f"WARNING: Error loading '{self.slangs_csv_path}': {e}. Slang map empty.")
        else:
            print(f"WARNING: '{self.slangs_csv_path}' not found. Slang map empty.")

    def text_to_words(self, s: str) -> list[str]:
        """
        1) Mengubah teks (string panjang) menjadi array of string (tokens)
           menggunakan fungsi `tokenize_text` dari functions.py.
        """
        return tokenize_text(s) # Memanggil fungsi yang diimpor

    def normalize_text(self, s: str) -> tuple[str, dict]:
        """
        2) Normalisasi teks input 's' melalui serangkaian langkah:
           - Tokenisasi
           - Normalisasi pengulangan huruf
           - Normalisasi leet (korpus)
           - Normalisasi leet paksa
           - Cek singkatan (terhadap common_words)
           - Normalisasi slang
           - Koreksi typo (terhadap common_words)

        Mengembalikan teks yang dinormalisasi dan dictionary counts dari setiap operasi.
        """
        if not s:
            return "", collections.defaultdict(int)

        counts = collections.defaultdict(int)
        tokens = tokenize_text(s) # Panggil fungsi dari functions.py
        normalized_tokens = []

        for token in tokens:
            original_token = token
            processed_token = token

            # Hanya proses token yang kemungkinan adalah kata (regex \w+ cocok)
            if re.fullmatch(r"\w+", token, re.UNICODE):
                # 1. Panggil normalize_repetitions
                temp_token = normalize_repetitions(processed_token) # Panggil fungsi dari functions.py
                if temp_token != processed_token:
                    counts['normalize_repetitions'] += 1
                processed_token = temp_token

                # 2. Panggil normalize_leet (meneruskan common_words_set)
                temp_token_leet = normalize_leet(processed_token, self._COMMON_WORDS) # Panggil fungsi dari functions.py
                
                # Cek kondisi untuk memanggil normalize_forced_leet
                if temp_token_leet == processed_token and \
                   re.search(r"[^a-zA-Z0-9_]", original_token) and \
                   original_token.lower() not in self._COMMON_WORDS:
                    
                    temp_token_forced = normalize_forced_leet(original_token) # Panggil fungsi dari functions.py
                    if temp_token_forced != original_token:
                        counts['normalize_forced_leet'] += 1
                    processed_token = temp_token_forced
                else:
                    processed_token = temp_token_leet

                # 3. Cek is_abbreviation (terhadap COMMON_WORDS)
                found_abbr_conversion = False
                for common_word in self._COMMON_WORDS: # Iterasi melalui COMMON_WORDS milik instance
                    if is_abbreviation(processed_token, common_word): # Panggil fungsi dari functions.py
                        processed_token = common_word
                        counts['is_abbreviation'] += 1
                        found_abbr_conversion = True
                        break
                
                # 4. Panggil slang_to_formal (meneruskan slang_map)
                temp_token = slang_to_formal(processed_token, self._SLANG_TO_FORMAL_MAP) # Panggil fungsi dari functions.py
                if temp_token != processed_token:
                    counts['slang_to_formal'] += 1
                processed_token = temp_token

                # 5. Panggil is_typo (terhadap COMMON_WORDS)
                if processed_token.lower() not in self._COMMON_WORDS: # Hanya cek typo jika kata belum baku
                    found_typo_correction = False
                    for common_word_target in self._COMMON_WORDS: # Iterasi melalui COMMON_WORDS milik instance
                        # Pastikan kita tidak membandingkan kata dengan dirinya sendiri
                        if processed_token.lower() != common_word_target.lower() and \
                           is_typo(processed_token, common_word_target): # Panggil fungsi dari functions.py
                            processed_token = common_word_target
                            counts['is_typo'] += 1
                            found_typo_correction = True
                            break
            
            normalized_tokens.append(processed_token)

        # Gabungkan kembali token menjadi string, dengan penanganan spasi di sekitar tanda baca
        final_text = " ".join(normalized_tokens)
        final_text = re.sub(r'\s([.,!?;:])', r'\1', final_text)
        final_text = re.sub(r'([([{])\s', r'\1', final_text)
        final_text = re.sub(r'\s([)\]}])', r'\1', final_text)

        return final_text, dict(counts)

    def count_alays(self, s: str) -> int:
        """
        3) Menghitung total kemunculan normalisasi alay (normalize_leet dan normalize_forced_leet)
           dalam teks 's'. Memanggil `normalize_text` secara internal.
        """
        _, counts = self.normalize_text(s) # Panggil metode dari instance kelas
        return counts['normalize_leet'] + counts['normalize_forced_leet']

    def count_slangs(self, s: str) -> int:
        """
        4) Menghitung total kemunculan normalisasi slang (slang_to_formal) dalam teks 's'.
           Memanggil `normalize_text` secara internal.
        """
        _, counts = self.normalize_text(s) # Panggil metode dari instance kelas
        return counts['slang_to_formal']

# --- Contoh Penggunaan Library (untuk demo) ---
if __name__ == "__main__":
    # Penting: Pastikan folder 'corpus' dan file-file di dalamnya ada
    # di dalam 'text_normalizer/' saat Anda menjalankan skrip ini.
    # Juga, pastikan `functions.py` ada di `text_normalizer/`.

    # Buat struktur direktori dummy dan file
    print("--- Menyiapkan Struktur Direktori dan File Dummy untuk Demo ---")
    os.makedirs('text_normalizer/corpus', exist_ok=True)
    
    # Buat common_words.txt dummy
    dummy_common_words_content = """
    yang
    dan
    ini
    itu
    dengan
    dari
    ada
    untuk
    juga
    bisa
    tidak
    dalam
    ayam
    tunggu
    oke
    sudah
    massa
    kucing
    makan
    tidur
    pergi
    datang
    mobil
    rumah
    buku
    pensil
    meja
    kursi
    sekolah
    apel
    jeruk
    sepatu
    menetas
    menyenangkan
    menggemaskan
    menyarankan
    menemukan
    mengikuti
    menyamakan
    menyangka
    mencebur
    misal
    halo
    jemput
    komputer
    banget
    ngomong-ngomong
    tidak jelas
    kamu
    """
    with open("text_normalizer/corpus/common_words.txt", "w", encoding="utf-8") as f:
        f.write(dummy_common_words_content.lower())

    # Buat slangs.csv dummy
    dummy_slangs_content = """slang,formal
netaas,menetas
nyenengin,menyenangkan
gemesiin,menggemaskan
saranin,menyarankan
nemuin,menemukan
ngikutin,mengikuti
nyamain,menyamakan
nyangka,menyangka
nyebur,mencebur
gaje,tidak jelas
btw,ngomong-ngomong
yg,yang
km,kamu
bgt,banget
"""
    with open("text_normalizer/corpus/slangs.csv", "w", encoding="utf-8") as f:
        f.write(dummy_slangs_content)
    
    # Buat dummy functions.py (JANGAN GUNAKAN INI DI PRODUKSI, GANTI DENGAN FUNCTIONS.PY ASLI ANDA)
    # Ini hanya untuk memastikan script demo bisa jalan jika functions.py belum ada
    dummy_functions_content = """
import re
# Placeholder functions for demo. Replace with your actual functions.
def tokenize_text(s: str) -> list[str]: return re.findall(r"\\\\w+|[^\\\\w\\\\s]", s, re.UNICODE)
def normalize_repetitions(word: str) -> str: return word.replace('ooo', 'o').replace('eee', 'e') # Simple placeholder
def is_abbreviation(abbr: str, word: str) -> bool: return (abbr.lower() == 'yg' and word.lower() == 'yang') or (abbr.lower() == 'km' and word.lower() == 'kamu') or (abbr.lower() == 'bgt' and word.lower() == 'banget')
def normalize_leet(word: str, common_words_set: set) -> str:
    leet_map_basic = {'4': 'a', '1': 'i', '3': 'e', '0': 'o', '@': 'a', '$': 's'}
    temp_word = "".join(leet_map_basic.get(char.lower(), char.lower()) for char in word)
    return temp_word if temp_word in common_words_set else word
def normalize_forced_leet(word: str) -> str:
    leet_map_aggressive = {'4': 'a', '1': 'i', '3': 'e', '0': 'o', '@': 'a', '$': 's'}
    return "".join(leet_map_aggressive.get(char.lower(), char.lower()) for char in word)
def slang_to_formal(word: str, slang_map: dict) -> str: return slang_map.get(word.lower(), word)
def is_typo(word: str, target: str) -> bool:
    if word.lower() == target.lower(): return False
    from rapidfuzz.distance import DamerauLevenshtein; dist = DamerauLevenshtein.distance(word.lower(), target.lower()); return 0 < dist <= 2
    """
    with open("text_normalizer/functions.py", "w", encoding="utf-8") as f:
        f.write(dummy_functions_content)

    print("\n--- Menginisialisasi Normalizer ---")
    # Instansiasi kelas Normalizer.
    # Karena konstruktor tidak lagi menerima path, ia akan otomatis mencari di 'corpus/'
    normalizer_instance = Normalizer()

    print("\n--- Testing `text_to_words` ---")
    test_sentence_1 = "Halo, apa kabar? Aku lagi netaas ide baru."
    words_1 = normalizer_instance.text_to_words(test_sentence_1)
    print(f"Original: '{test_sentence_1}'")
    print(f"Tokens: {words_1}")

    print("\n--- Testing `normalize_text` ---")
    test_sentence_2 = "H4l0o, aku k3ren bgt! g4j3 kyknya btw ini masssaa aku s4raninnn km n4nti JEMpUt aku yaa. pusinggg banget!"
    normalized_text, counts = normalizer_instance.normalize_text(test_sentence_2)
    print(f"Original: '{test_sentence_2}'")
    print(f"Normalized: '{normalized_text}'")
    print(f"Counts: {counts}")

    print("\n--- Testing `count_alays` ---")
    alay_count = normalizer_instance.count_alays(test_sentence_2)
    print(f"Total Alay Count: {alay_count}")

    print("\n--- Testing `count_slangs` ---")
    slang_count = normalizer_instance.count_slangs(test_sentence_2)
    print(f"Total Slang Count: {slang_count}")

    # Opsional: bersihkan file dummy setelah pengujian
    # import shutil
    # shutil.rmtree('text_normalizer')