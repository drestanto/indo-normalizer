def is_abbreviation(abbr, word):
    if len(abbr) < (len(word) + 1) // 2:
        return False
    i = 0
    for c in word:
        if i < len(abbr) and abbr[i] == c:
            i += 1
    return i == len(abbr)

print(is_abbreviation("ptgjbk", "pertanggungjawabkan"))
print(is_abbreviation("blm", "belum"))
print(is_abbreviation("lom", "belom"))
print(is_abbreviation("bs g?", "bisa ga?"))
print(is_abbreviation("mk", "makan"))