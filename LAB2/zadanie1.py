# Zaszyfruj teksty w 3 różnych dowolnych językach przy pomocy algorytmu przesunięcia cyklicznego (dowolnego).
# Korzystając z analizy statystycznej występowania znaków dla danego języka złam klucz (przesunięcie) i odszyfruj
# wiadomości. (1 pkt)
import random

letterFrequencyEnglish = {'E': 0.1200,
                          'T': 0.0910,
                          'A': 0.0812,
                          'O': 0.0768,
                          'I': 0.0731,
                          'N': 0.0695,
                          'S': 0.0628,
                          'R': 0.0602,
                          'H': 0.0592,
                          'D': 0.0432,
                          'L': 0.0398,
                          'U': 0.0288,
                          'C': 0.0271,
                          'M': 0.0261,
                          'F': 0.0230,
                          'Y': 0.0211,
                          'W': 0.0209,
                          'G': 0.0203,
                          'P': 0.0182,
                          'B': 0.0149,
                          'V': 0.0111,
                          'K': 0.0069,
                          'X': 0.0017,
                          'Q': 0.0011,
                          'J': 0.0010,
                          'Z': 0.0007}

letterFrequencySpanish = {'A': 0.1216,
                          'B': 0.0149,
                          'C': 0.0387,
                          'D': 0.0467,
                          'E': 0.1408,
                          'F': 0.0069,
                          'G': 0.0100,
                          'H': 0.0118,
                          'I': 0.0598,
                          'J': 0.0052,
                          'K': 0.0011,
                          'L': 0.0524,
                          'M': 0.0308,
                          'N': 0.0700,
                          'O': 0.0920,
                          'P': 0.0289,
                          'Q': 0.0111,
                          'R': 0.0641,
                          'S': 0.0720,
                          'T': 0.0460,
                          'U': 0.0469,
                          'V': 0.0105,
                          'W': 0.0004,
                          'X': 0.0014,
                          'Y': 0.0109,
                          'Z': 0.0047,
                          }

letterFrequencyItalian = {"A": 0.1100,
                          'B': 0.0105,
                          'C': 0.0430,
                          'D': 0.0339,
                          'E': 0.1197,
                          'F': 0.0101,
                          'G': 0.0165,
                          'H': 0.0143,
                          'I': 0.1027,
                          'J': 0.0000,
                          'K': 0.0000,
                          'L': 0.0570,
                          'M': 0.0287,
                          'N': 0.0702,
                          'O': 0.1098,
                          'P': 0.0296,
                          'Q': 0.0045,
                          'R': 0.0619,
                          'S': 0.0548,
                          'T': 0.0697,
                          'U': 0.0328,
                          'W': 0.0000,
                          'X': 0.0000,
                          'V': 0.0175,
                          'Y': 0.0000,
                          'Z': 0.0085
                          }


def change_text_to_plain(string):
    string = string.upper().replace(" ", "").replace("Ù", "U").replace("Ò", "O").replace("Ì", "I").replace("È", "E") \
        .replace("É", "E").replace("À", "A").replace("Ú", "U").replace("Ü", "U").replace("Ó", "O").replace("Ñ", "N") \
        .replace("Í", "I").replace("É", "E").replace("Á", "A")
    txt = ""
    for letter in string:
        if ord("A") <= ord(letter) <= ord("Z"):
            txt += letter
    return txt


def encryption(string, k=1):
    txt = list(string)
    for i in range(len(txt)):
        if "A" <= txt[i] <= "Z":
            txt[i] = chr(ord(txt[i]) + k)
        if ord(txt[i]) > ord("Z"):
            txt[i] = chr((ord(txt[i]) % (ord("Z") + 1)) + ord("A"))
        if ord(txt[i]) < ord("A"):
            txt[i] = chr(ord(txt[i]) - ord("A") + ord("Z") + 1)
    return "".join(txt)


def text_to_list(string):
    frequency = {}
    for i in range(ord("A"), ord("Z") + 1):
        frequency[chr(i)] = 0
    k = 0
    for i in string:
        k += 1;
        if i in frequency:
            frequency[i] += 1
        else:
            raise Exception("Error")
    for i in frequency:
        if frequency[i] != 0:
            frequency[i] = frequency[i] / len(string)
    return frequency


def calculate_language(letters, language):
    solution_pointer = 0.0
    range_to_do = len(letters)
    if range_to_do != len(language):
        raise Exception("Something go wrong!")
    for i in range(range_to_do):
        solution_pointer += (letters[i] - language[i]) ** 2
    return solution_pointer


def sort_dict(dictionary):
    return dict(sorted(dictionary.items(), key=lambda item: item[1]))


languages = {"English": sort_dict(letterFrequencyEnglish),
             "Spanish": sort_dict(letterFrequencySpanish),
             "Italian": sort_dict(letterFrequencyItalian)
             }

if __name__ == "__main__":
    for file in ["english-article.txt", "italian-article.txt", "spanish-article.txt"]:
        text = "".join(open(file, "r").readlines())
        plain_text = change_text_to_plain(text)
        encrypted_text = encryption(plain_text, random.randint(1, 26))
        list_of_letters_in_plain_text = sort_dict(text_to_list(encrypted_text))
        solution = 1
        detected_language = None
        for language in languages:
            prop = calculate_language(list(list_of_letters_in_plain_text.values()),
                                      list(languages[language].values()))
            if prop < solution:
                solution = prop
                detected_language = language
        key = ord(list(languages[detected_language].keys())[-1]) - ord(list(list_of_letters_in_plain_text.keys())[-1])
        decrypted_text = encryption(encrypted_text, key)
        if decrypted_text == plain_text:
            print('Decryption successful, Detected language for file: {} is: {} key is {}'
                  .format(file, detected_language, key))
        else:
            print('Decryption unsuccessful, Detected language for file: {} is: {} key is {}'
                  .format(file, detected_language, key))
