from Cryptodome.Cipher import ARC4
from math import log2


def shanon_entropy(string):
    entropy = 0.0
    size = len(string)
    for i in range(256):
        prob = string.count(chr(i)) / size
        if prob > 0.0:
            entropy += prob * log2(prob)
    return -entropy


def decrypt(encrypted_text, key):
    arc = ARC4.new(key)
    return arc.decrypt(encrypted_text)


ARC4.key_size = range(3, 257)
expected_shanon_entropy_value = 4.5

if __name__ == "__main__":
    for file in ["crypto.rc4", "crypto2.rc4"]:
        print(f"Looking keys for file: {file} with expected_shanon_entropy_value: {expected_shanon_entropy_value}")
        in_file = open(file, "rb")
        data_to_decrypt = in_file.read()
        in_file.close()
        for i in range(ord("a"), ord("z")):
            for j in range(ord("a"), ord("z")):
                for k in range(ord("a"), ord("z")):
                    key_gen = chr(i) + chr(j) + chr(k)
                    decrypted_text = decrypt(data_to_decrypt, key_gen.encode())
                    decoded_decrypted_text = decrypted_text.decode(errors="ignore")
                    shanon_entropy_value = shanon_entropy(decoded_decrypted_text)
                    if shanon_entropy_value < expected_shanon_entropy_value:
                        print(f"Found shanon_entropy_value: {shanon_entropy_value} with key: {key_gen}")
                        save_key = open(file.replace(".", "_") + "_" + key_gen + ".txt", "w+")
                        save_key.writelines(decoded_decrypted_text)
                        save_key.close()
