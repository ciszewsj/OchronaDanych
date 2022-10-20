from itertools import chain

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

AES.key_size = range(10, 100)
key_size = 16
possible_start = ['BM', 'BA', 'CI', 'CP', "IC", "PT"]
if __name__ == "__main__":
    range_of_attack = chain(range(ord("a"), ord("z") + 1), range(ord("0"), ord("9") + 1))
    encrypted_image = pad(open("security_ECB_encrypted.bmp", "rb").read(), key_size)
    for i in range_of_attack:
        key = chr(i) * key_size
        aes = AES.new(key.encode(), AES.MODE_ECB)
        w = aes.decrypt(encrypted_image)
        header = w[0:2].decode(errors="ignore")
        if header in possible_start:
            file_save = key + ".bmp"
            print(f"Found header: {header} for key: {key} save file: {file_save}")
            o = open(file_save, "wb")
            o.write(w)
            o.close()
