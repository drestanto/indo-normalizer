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
        re.findall(r"\w+|[^\w\s]", s, re.UNICODE)

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