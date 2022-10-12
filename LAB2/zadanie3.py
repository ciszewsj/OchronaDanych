from Cryptodome.Cipher import ARC4


def count_arc4(key, original_text):
    s = [x for x in range(256)]
    j = 0
    for i in range(256):
        j = (j + s[i] + ord(key[i % len(key)])) % 256
        swp = s[i]
        s[i] = s[j]
        s[j] = swp

    i = 0
    j = 0
    g = []
    for iterator in range(len(original_text)):
        i = (i + 1) % 256
        j = (j + s[i]) % 256

        swp = s[i]
        s[i] = s[j]
        s[j] = swp
        g.append(s[(s[i] + s[j]) % 256])
        g[iterator] = g[iterator] ^ ord(original_text[iterator])
    return bytes(g)


def encrypt(key, text):
    arc = ARC4.new(key)
    return arc.encrypt(text)


def decrypt(key, text):
    arc = ARC4.new(key)
    return arc.decrypt(text)


values = {
    "Key": "Plaintext",
    "Wiki": "pedia",
    "Secret": "Attack at dawn",
    "Kry": "ptologia"
}
ARC4.key_size = range(3, 257)

for key in values:
    print(f"Try for pair: {key} - {values[key]}")
    encrypted_arc4 = count_arc4(key, values[key])
    encrypted_arc4_with_crypto = encrypt(key.encode(), values[key].encode())

    decrypted_arc4 = count_arc4(key, "".join([chr(x) for x in list(encrypted_arc4)]))
    decrypted_arc4_with_crypto = decrypt(key.encode(), encrypted_arc4_with_crypto)

    if encrypted_arc4_with_crypto == encrypted_arc4:
        print(f"Encrypted value of arc4 is same as ARC4.encrypt")
    else:
        print("Encryption failure")
    if decrypted_arc4.decode() == values[key] and values[key] == decrypted_arc4_with_crypto.decode():
        print(f"Decrypted value of arc4 is same as ARC4.encrypt")
    else:
        print("Decryption failure")
