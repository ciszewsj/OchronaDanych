from passlib.hash import sha1_crypt
from passlib.hash import sha256_crypt
from passlib.hash import sha512_crypt
from passlib.hash import md5_crypt
from passlib.hash import bcrypt
from passlib.hash import argon2
import base64

# https://hashcat.net/wiki/doku.php?id=example_hashes
word = "password"


def print_alg(alg, salt, rounds, recreate, equal, additional_info=None):
    print(f"    Alghoritm  : {alg}")
    print(f"    Salt       : {salt}")
    print(f"    Rounds     : {rounds}")
    print(f"    Recreate   : {recreate}")
    print(f"    Equal      : {equal}")
    if additional_info is not None:
        print(f"    Additional : {additional_info}")


if __name__ == "__main__":
    for hash_text in open("hashes.txt", "r"):
        hash_text = hash_text.replace("'", "").replace("\n", "")
        split_text = hash_text.split("$")
        hash_type = split_text[1]
        print("\n")
        print(hash_text + " :")

        if hash_type == "sha1":
            rounds = split_text[2]
            salt = split_text[3]
            recreate = sha1_crypt.hash(word, rounds=rounds, salt=salt)
            print_alg("sha1_encrypt", salt, rounds, recreate, recreate == hash_text)

        elif hash_type == "5":
            rounds = split_text[2].replace("rounds=", "")
            salt = split_text[3]
            recreate = sha256_crypt.hash(word, rounds=rounds, salt=salt)
            print_alg("sha256_crypt", salt, rounds, recreate, recreate == hash_text)

        elif hash_type == "6":
            rounds = split_text[2].replace("rounds=", "")
            salt = split_text[3]
            recreate = sha512_crypt.hash(word, rounds=rounds, salt=salt)
            print_alg("sha512_crypt", salt, rounds, recreate, recreate == hash_text)

        elif hash_type in ["2b", "2y"]:
            rounds = int(split_text[2])
            salt = split_text[3][0:22]
            recreate = bcrypt.hash(word, salt=salt, rounds=rounds, ident=hash_type)
            print_alg(f"bcrypt {hash_type}", salt, rounds, recreate, recreate == hash_text)

        elif hash_type == "1":
            rounds = ""
            salt = split_text[2]
            recreate = md5_crypt.hash(word, salt=salt)
            print_alg("md5_crypt", salt, rounds, recreate, recreate == hash_text)

        elif "argon2" in hash_type:
            argon2_type = split_text[1].replace("argon2", "").upper()
            argon2_revision = split_text[2].replace("v=", "")

            split_argon2 = split_text[3].split(",")
            argon2_memory_cost = split_argon2[0].replace("m=", "")
            argon2_time_cost = split_argon2[1].replace("t=", "")
            argon2_parallelization = split_argon2[2].replace("p=", "")

            argon2_digest_size = len(split_text[5])
            rounds = "linear to t"
            salt_padding = "=" * (len(split_text[4]) % 4)
            salt_base64_bytes = (split_text[4] + salt_padding).encode('ascii')
            salt_message_bytes = base64.b64decode(salt_base64_bytes)
            salt = salt_message_bytes

            digit_padding = "=" * (len(split_text[5]) % 4)
            digit_base64_bytes = (split_text[5] + digit_padding).encode('ascii')
            digit_message_bytes = base64.b64decode(digit_base64_bytes)
            digest_size = len(digit_message_bytes)

            recreate = argon2.using(type=argon2_type, salt=salt, time_cost=argon2_time_cost,
                                    memory_cost=argon2_memory_cost,
                                    parallelism=argon2_parallelization, digest_size=digest_size).hash(word)
            split_argon2.append(f"digest_size: {argon2_digest_size}")
            print_alg(f"argon2 {argon2_type}", salt, rounds, recreate, recreate == hash_text,
                      split_argon2)
        else:
            print(f"    NOT IMPLEMENTED YET")
