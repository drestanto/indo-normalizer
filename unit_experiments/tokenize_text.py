def tokenize_text(s: str):
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
    """
    ascii_symbols = "!@$"
    tokens = []
    i, n = 0, len(s)

    def is_letter(c):        return c.isalpha()
    def is_letterlike(c):    return c.isdigit() or c in ascii_symbols

    while i < n:
        # aturan 3: ' ! ' / ' @ ' / ' $ '
        if i + 2 < n and s[i] == " " and s[i+1] in ascii_symbols and s[i+2] == " ":
            tokens.append(s[i:i+3]); i += 3; continue

        c = s[i]

        # kandidat kata (huruf, digit, simbol)
        if is_letter(c) or is_letterlike(c):
            # digit tunggal di antara spasi
            if c.isdigit() and (i == 0 or s[i-1] == " ") and (i+1 == n or s[i+1] == " "):
                tokens.append(c); i += 1; continue
            # tanda seru lone (!) – aturan 6
            if c == "!" and i > 0 and not s[i-1].isspace() and (i+1 == n or s[i+1].isspace()):
                tokens.append("!"); i += 1; continue
            # bangun token kata
            j = i
            while j < n:
                cj = s[j]
                if cj == "!" and j > i and not s[j-1].isspace() and (j+1 == n or s[j+1].isspace()):
                    break
                if is_letter(cj) or is_letterlike(cj):
                    j += 1
                else:
                    break
            tokens.append(s[i:j]); i = j; continue

        # aturan 2: run spasi/punktuasi
        j = i
        while j < n and not (is_letter(s[j]) or is_letterlike(s[j])):
            j += 1
        tokens.append(s[i:j]); i = j

    return tokens

print(tokenize_text("... agama aku , !slam kan? hehehehe. bag1 aku, cara baca itu penting abi5!"))
print(tokenize_text("   oi 5 bagi dan 55 orang sama2 makan nih..."))