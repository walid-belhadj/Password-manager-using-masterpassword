from hashlib import sha256
import hashlib

def master_password_gen():

    print("---------------Génération du master password------------------------------")

    master_password = input("Veuillez saisir votre master password: ").encode()

    compile_factor_together = hashlib.sha256(master_password).hexdigest()
    print("\n")
    print("Hashed Master Password: " + str(compile_factor_together))

master_password_gen()
