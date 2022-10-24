from Cryptodome.Random import get_random_bytes
import skimage.measure
import skimage.io
from BMPcrypt import encrypt_data

if __name__ == "__main__":
    encrypt_data("demo24.bmp", "CBC", get_random_bytes(32))
    encrypt_data("demo24.bmp", "ECB", get_random_bytes(32))
    image_cbc = skimage.io.imread(fname="demo24_CBC_encrypted.bmp")
    image_ecb = skimage.io.imread(fname="demo24_ECB_encrypted.bmp")
    img = skimage.io.imread(fname="demo24.bmp")

    entropy_cbc = skimage.measure.shannon_entropy(image_cbc)
    entropy_ecb = skimage.measure.shannon_entropy(image_ecb)

    print(f"CBC Entropy: {entropy_cbc}")
    print(f"ECB Entropy: {entropy_ecb}")
