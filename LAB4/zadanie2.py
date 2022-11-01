from passlib.hash import md5_crypt
import random
import string


def count_birthday_paradox():
    w = 1
    i = 0
    k = 52 ** 5
    s = 0.5
    while 1:
        w = w * (1 - i / k)
        if w < 1 - s:
            print(f" {i} -> {s} -> {w}")
            break
        i += 1


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


if __name__ == "__main__":
    count_birthday_paradox()
    hashes = {}
    while True:
        new_string = get_random_string(random.randint(3, 20))
        if new_string in hashes:
            continue
        hash_text = md5_crypt.hash(new_string)
        hash_text = hash_text.replace("'", "").replace("\n", "")
        split_text = hash_text.split("$")
        key = split_text[3][0:5]
        if key in hashes:
            print(f"FIND SOLUTION IN NUMBER OF {len(hashes) + 1}")
            print(f"Hash 1 : {hashes[key][1]} , text : {hashes[key][0]}")
            print(f"Hash 1 : {hash_text} , text : {new_string}")
            break
        hashes[key] = (new_string, hash_text)
