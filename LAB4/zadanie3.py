from passlib.hash import argon2
import base64

hash_text = "$argon2id$v=19$m=65536,t=3,p=4$4Vzr3bvXWuvdmzMG4PxfCw$NWNunMWdo0ugkWWsL8Z+sdMKnDcJp0vDfMkr30Lmpd4"
if __name__ == "__main__":
    split_text = hash_text.split("$")
    hash_type = split_text[1]
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
    for a in range(ord("a"), ord("z") + 1):
        for b in range(ord("a"), ord("z") + 1):
            word = chr(a) + chr(b)
            recreate = argon2.using(type=argon2_type, salt=salt, time_cost=argon2_time_cost,
                                    memory_cost=argon2_memory_cost,
                                    parallelism=argon2_parallelization, digest_size=digest_size).hash(word)
            if recreate == hash_text:
                print(f"FOUND hash : {recreate} , word : {word}")
                exit(0)
