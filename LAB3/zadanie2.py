from Cryptodome.Random import get_random_bytes

from BMPcrypt import encrypt_data

if __name__ == "__main__":
    encrypt_data("demo24.bmp", "CBC", get_random_bytes(32))
    encrypt_data("demo24.bmp", "ECB", get_random_bytes(32))
