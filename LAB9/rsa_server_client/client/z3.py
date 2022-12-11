import client
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import json

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

    # Generate Signature
    hash_msg = SHA256.new(msg.encode())
    msg_sig = pkcs1_15.new(rsa_keys1).sign(hash_msg)
    public_key_usr2 = RSA.import_key(c.get_key(usr2))

    # Create Object with signature and msg
    cip = PKCS1_OAEP.new(public_key_usr2)
    a = {"msg": base64.b64encode(cip.encrypt(msg.encode())).decode(), "sig": base64.b64encode(msg_sig).decode()}
    object_to_encryption = json.dumps(a)

    # SEND:
    encrypted = base64.b64encode(object_to_encryption.encode())
    c.send_text_message(usr1, encrypted)

    # RECEIVE :
    public_key_usr1 = RSA.import_key(c.get_key(usr1))
    text_1_to_decode = base64.b64decode(c.get_text_message(usr1)).decode()
    json_text = json.loads(text_1_to_decode)

    # DECODE MSG
    encrypted_message = base64.b64decode(json_text["msg"])
    cip = PKCS1_OAEP.new(rsa_keys2)
    decrypted_message = cip.decrypt(encrypted_message).decode()
    hash_decrypted_msg = SHA256.new(decrypted_message.encode())

    # Validate SIGNATURE
    encrypted_signature = base64.b64decode(json_text["sig"])
    pkcs1_15.new(public_key_usr1).verify(hash_decrypted_msg, encrypted_signature)

    print(f"RETURNED MSG FROM {usr1} : '{decrypted_message}'")

    # SECOND WAY
    msg = decrypted_message
    # Generate Signature
    hash_msg = SHA256.new(msg.encode())
    msg_sig = pkcs1_15.new(rsa_keys2).sign(hash_msg)
    public_key_usr1 = RSA.import_key(c.get_key(usr1))

    # Create Object with signature and msg
    cip = PKCS1_OAEP.new(public_key_usr1)
    a = {"msg": base64.b64encode(cip.encrypt(msg.encode())).decode(), "sig": base64.b64encode(msg_sig).decode()}
    object_to_encryption = json.dumps(a)

    # SEND:
    encrypted = base64.b64encode(object_to_encryption.encode())
    c.send_text_message(usr2, encrypted)

    # RECEIVE :
    public_key_usr1 = RSA.import_key(c.get_key(usr1))
    text_2_to_decode = base64.b64decode(c.get_text_message(usr2)).decode()
    json_text = json.loads(text_2_to_decode)

    # DECODE MSG
    encrypted_message = base64.b64decode(json_text["msg"])
    cip = PKCS1_OAEP.new(rsa_keys1)
    decrypted_message = cip.decrypt(encrypted_message).decode()
    hash_decrypted_msg = SHA256.new(decrypted_message.encode())

    # Validate SIGNATURE
    encrypted_signature = base64.b64decode(json_text["sig"])
    pkcs1_15.new(public_key_usr2).verify(hash_decrypted_msg, encrypted_signature)

    print(f"RETURNED MSG FROM {usr2} : '{decrypted_message}'")
