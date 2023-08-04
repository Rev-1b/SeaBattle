def translate_letter_to_number(letter: str) -> int:
    dictionary = {'A': 0,
                  'B': 1,
                  'C': 2,
                  'D': 3,
                  'E': 4,
                  'F': 5,
                  'G': 6,
                  'H': 7,
                  'I': 8,
                  'J': 9}

    return dictionary[letter]
