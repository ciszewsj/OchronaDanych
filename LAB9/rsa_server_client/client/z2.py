import client
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

if __name__ == "__main__":
    c = client.Client("http://localhost:5000")
    msg = "666213769 - Numer z Ojca mateusza XD"
    usr1 = "tom"
    usr2 = "alice"

    rsa_keys1 = RSA.generate(2048)
    pub_key1 = rsa_keys1.public_key()
    rsa_keys2 = RSA.generate(2048)
    pub_key2 = rsa_keys2.public_key()

    c.send_key(usr1, pub_key1.exportKey())
    c.send_key(usr2, pub_key2.exportKey())

    # FIRST WAY

    # SEND:
    public_key_usr2 = RSA.import_key(c.get_key(usr2))
    cip = PKCS1_OAEP.new(public_key_usr2)
    encrypted = base64.b64encode(cip.encrypt(msg.encode()))
    c.send_text_message(usr1, encrypted)

    # RECEIVE
    text_1_to_decode = c.get_binary_message(usr1)
    cip = PKCS1_OAEP.new(rsa_keys2)
    returned_msg = cip.decrypt(text_1_to_decode).decode()
    print(f"RETURNED MSG FROM {usr1} : '{returned_msg}'")

    # SECOND WAY

    # SEND:
    public_key_usr1 = RSA.import_key(c.get_key(usr1))
    cip = PKCS1_OAEP.new(public_key_usr1)
    encrypted = base64.b64encode(cip.encrypt(returned_msg.encode()))
    c.send_text_message(usr2, encrypted)

    # RECEIVE
    text_2_to_decode = c.get_binary_message(usr2)
    cip = PKCS1_OAEP.new(rsa_keys1)
    returned_msg_2 = cip.decrypt(text_2_to_decode).decode()
    print(f"RETURNED MSG FROM {usr2} : '{returned_msg_2}'")
