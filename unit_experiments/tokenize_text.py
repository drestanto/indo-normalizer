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

print(tokenize_text("anak-anak suka banget bermain bola. tapi menurut sumber-detik.com-tidak ada,blah"))
print(tokenize_text("... agama aku , !slam kan? hehehehe. bag1 aku, cara baca itu penting abi5!"))
print(tokenize_text("   oi 5 bagi dan 55 orang sama2 makan nih..."))
print(tokenize_text("instagram aku @dresdyas nih, follow ya"))
print(tokenize_text("email dari dubius.id yang asli adalah official@dubius.id, ga ada email lain"))