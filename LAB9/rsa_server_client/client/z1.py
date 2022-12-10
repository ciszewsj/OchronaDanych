import client
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

if __name__ == "__main__":
    c = client.Client("http://localhost:5000")
    key = RSA.import_key(c.get_key("deadbeef"))
    cip = PKCS1_OAEP.new(key)
    encrypted = base64.b64encode(cip.encrypt(b"Top secret"))
    c.send_text_message("deadbeef", encrypted)
