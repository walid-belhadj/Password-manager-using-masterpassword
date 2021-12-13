from hashlib import sha256
from Cryptodome.Cipher import AES
from pbkdf2 import PBKDF2
import hashlib
from base64 import b64encode, b64decode
from hashlib import sha256
import hashlib

# Salut choisi
salt = b'\x02\x00\x02\x01'
# generation du master password

def query_master_pwd(master_password, second_FA_location):
    # Use master_password_hash_generator.py to generate a master password hash.
    master_password_hash = "c097511b9ac5913064587815a42dbfe0b1037edd5c9f00ef7f8cb8089172ebe2"
    compile_factor_together = hashlib.sha256(master_password + second_FA_location).hexdigest()
    if compile_factor_together == master_password_hash:
        return True
#chiffrer les messages qu'on devrait stocker dans localement

def encrypt_password(password_to_encrypt, master_password_hash):
#j'applique PBKDF2 sur le hash du master password + salt
    key = PBKDF2(str(master_password_hash), salt).read(32)
    print("here is the key after pbkdf"+ key)
    data_convert = str.encode(password_to_encrypt)
    print("here is data_convert"+ data_convert)
    cipher = AES.new(key, AES.MODE_EAX)
    print("here is cipher after aes eax stands for encrypt + authentifcate and translate "+ data_convert)
    nonce = cipher.nonce
    print("extract nonce"+ nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data_convert)
    print("Crypter et digérer pour obtenir les données chiffrées et la balise: "+ ciphertext)
    add_nonce = ciphertext + nonce
    print("ajout du nonce"+ add_nonce)
    encoded_ciphertext = b64encode(add_nonce).decode()
    print("encoded message ( binary to printable ascii"+ encoded_ciphertext)
    return encoded_ciphertext

def decrypt_password(password_to_decrypt, master_password_hash):

    if len(password_to_decrypt) % 4:

     password_to_decrypt += '=' * (4 - len(password_to_decrypt) % 4)

    convert = b64decode(password_to_decrypt)

    key = PBKDF2(str(master_password_hash), salt).read(32)

    nonce = convert[-16:]

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    plaintext = cipher.decrypt(convert[:-16])

    return plaintext


