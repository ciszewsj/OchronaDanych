# >>> from BMPcrypt import encrypt_data
# >>> from BMPcrypt import encrypt_full
# >>> encrypt_data("demo24.bmp", "ECB", b"x" * 16) 
from PIL import Image
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


def nullpadding(data, length=16):
    return data + b"\x00" * (length - len(data) % length)


def convert_to_RGB(data):
    pixels = []

    for i in range(0, len(data) - 1, 3):
        r = int(data[i])
        g = int(data[i + 1])
        b = int(data[i + 2])

        pixels.append((r, g, b))
    return pixels


def encrypt_full(input_filename, mode, key):
    img_in = open(input_filename, "rb")
    data = img_in.read()

    data_padded = nullpadding(data)

    if mode == "CBC":
        iv = get_random_bytes(16)
        aes = AES.new(key, AES.MODE_CBC, iv)
    elif mode == "ECB":
        aes = AES.new(key, AES.MODE_ECB)

    encrypted_data = aes.encrypt(data_padded)
    encrypted_data_unpadded = encrypted_data[:len(data)]

    name = ''.join(input_filename.split('.')[:-1])
    img_format = str(input_filename.split('.')[-1])

    output_filename = name + '_' + mode + '_encrypted.' + img_format

    img_out = open(output_filename, "wb")
    img_out.write(encrypted_data_unpadded)
    img_out.close()
    img_in.close()


def encrypt_data(input_filename, mode, key):
    img_in = Image.open(input_filename)
    data = img_in.convert("RGB").tobytes()

    data_padded = nullpadding(data)

    if mode == "CBC":
        iv = get_random_bytes(16)
        aes = AES.new(key, AES.MODE_CBC, iv)
    elif mode == "ECB":
        aes = AES.new(key, AES.MODE_ECB)

    encrypted_data = aes.encrypt(data_padded)
    encrypted_data_unpadded = encrypted_data[:len(data)]
    img_out = Image.new(img_in.mode, img_in.size)
    img_out.putdata(convert_to_RGB(encrypted_data_unpadded))

    name = ''.join(input_filename.split('.')[:-1])
    img_format = str(input_filename.split('.')[-1])

    output_filename = name + '_' + mode + '_encrypted.' + img_format

    img_out.save(output_filename, img_format)
