from rapidfuzz.distance import DamerauLevenshtein

def is_typo(word, target):
    """
    Memeriksa apakah 'word' adalah 'nearmiss' dari 'target'
    dengan tepat satu operasi (sisip, hapus, substitusi, transposisi).
    """
    distance = DamerauLevenshtein.distance(word, target)
    return distance == 1 or distance == 2

print(f"'halo' dan 'halo': {is_typo('halo', 'halo')}")
print(f"'makan' dan 'maakn': {is_typo('maakn', 'makan')}")
print(f"'buku' dan 'buk': {is_typo('buk', 'buku')}")
print(f"'mobil' dan 'mo1bil': {is_typo('mo1bil', 'mobil')}")
print(f"'rumah' dan 'rumahh': {is_typo('rumahh', 'rumah')}")
print(f"'teman' dan 'timan': {is_typo('timan', 'teman')}")
print(f"'jalan' dan 'jalam': {is_typo('jalam', 'jalan')}")
print(f"'kucing' dan 'kucign': {is_typo('kucign', 'kucing')}")
print(f"'siswa' dan 'siwsa': {is_typo('siwsa', 'siswa')}")
print(f"'pulpen' dan 'pulpenna': {is_typo('pulpenna', 'pulpen')}")
print(f"'laptop' dan 'latopz': {is_typo('latopz', 'laptop')}")
print(f"'sekolah' dan 'skool': {is_typo('skool', 'sekolah')}")