import password_generator
import sql_statements
import db_connect
import psycopg2
import argparse
import master_password
import getpass
import sys
import hashlib
#from master_password_hash_generator import master_password_gen
print("\n")
print("---------------Bienvenue au password manager Firstpass--------------------")
print("")
print("Password Manager Accounts: Créer, Ajouter, et supprimer URL, Usernames, et Passwords",
    "usage=[options]")
print("\n")
def main():
    my_parser = argparse.ArgumentParser(description="Password Manager Acounts: Créer, Ajouter, et supprimer URL, Usernames, et Passwords",
    usage="[options]")
# première chose est de demander un master password
    master_password_input = getpass.getpass("Veuillez saisir votre Master Password: ").encode()
# je rejoute un second factor authentification ( il peut être une chose plus compliqué avec certaines exigéance)
    #second_FA_location ="Hello World".encode()
    second_FA_location = input("Veuillez saisir votre deuxième facteur d'authentification: ").encode()
#j'utilise sha256pour hasher les deux ensemble MPW+SFA
    master_password_hash = hashlib.sha256(master_password_input + second_FA_location).hexdigest()
    #print( master_password_hash) # to be commented later
#je check à l'aide de query mpw( master_passsword.py )
    if master_password.query_master_pwd(master_password_input, second_FA_location) is True: # si ok, i canconnect to db
        connection = db_connect.connection_db()
        print("\nAuthentification réussie ! .\n")
    else:
        print("Authenitification échouée ! ")
        sys.exit()
# gestion des argument, ça dépend:1,2, ou3 args
    my_parser.add_argument("-a", "--add", type=str, nargs=2, help="Ajouter une nouvelle entrée", metavar=("[URL]", "[USERNAME]"))
    my_parser.add_argument("-q", "--query", type=str, nargs = 1, help="Chercher une entrée par URL", metavar=("[URL]"))
    my_parser.add_argument("-l", "--list", action="store_true", help="Lister toutes les entrées dans password Accounts")
    my_parser.add_argument("-d", "--delete", type=str, nargs=1, help="Supprimer une entrée par URL", metavar=("[URL]"))
    my_parser.add_argument("-ap", "--add_password", type=str, nargs=3, help="Ajouter manuellement un password", metavar=("[URL]", "[USERNAME]", "[PASSWORD]"))
    my_parser.add_argument("-uurl", "--update_url", type=str, nargs=2, help="Mise à jour URL", metavar=("[NEW_URL]", "[OLD_URL]"))
    my_parser.add_argument("-uuname", "--update_username", type=str, nargs=2, help="Mise à jour un username dans account", metavar=("[URL]", "[NEW_USERNAME]"))
    my_parser.add_argument("-upasswd", "--update_password", type=str, nargs=2, help="Mise à jour un password dans account", metavar=("[URL]", "[NEW_PASSWORD]"))
    args = my_parser.parse_args()
    cursor = connection.cursor()
    connection.commit()

    if args.add:
        URL = args.add[0]
        username = args.add[1]
        password = password_generator.password_gen(20)
        print("Password généré....:"+password)
        password_official = master_password.encrypt_password(password, master_password_hash)
        insert_query = """INSERT INTO accounts (url, username, password) VALUES (%s, %s,%s)"""
        cursor.execute(insert_query, (URL, username, password_official))
        print("Enregistrement ajouté:" + "\n URL: {0}, Username: {1}, Password: {2} (Password généré)".format(URL, username, password))
        print("Enregistrement ajouté:" + "\n URL: {0}, Username: {1}, Password: {2} (Password à stocker)".format(URL, username, password_official))

    if args.query:
        URL = args.query[0]
        select_query = """SELECT * from accounts where url = %s"""
        cursor.execute(select_query, (URL, ))
        record = cursor.fetchone()
        password_field = record[2]
        decrypt_password = master_password.decrypt_password(password_field, master_password_hash)
        if bool(record):
            print("Enregistrement: " + "\n URL: {0}, Username: {1}, Password: {2}".format(record[0], record[1], decrypt_password.decode('utf-8')))
            print("Enregsitrement avec password chiffré: " + "\n URL: {0}, Username: {1}, Password: {2}".format(record[0], record[1], record[2]))
        else:
            print("Aucun enregistrement correspond à la valeur de: \'%s\'" % (URL))

    if args.delete:
        URL = args.delete[0]
        sql_delete_query = """Delete from accounts where url = %s"""
        cursor.execute(sql_delete_query, (URL, ))

    if args.add_password:
        URL = args.add_password[0]
        username = args.add_password[1]
        password = args.add_password[2]
        password_official = master_password.encrypt_password(password, master_password_hash)
        insert_query = """INSERT INTO accounts (url, username, password) VALUES (%s, %s,%s)"""
        cursor.execute(insert_query, (URL, username, password_official))
        print("Enregistrement ajouté ! .")

    if args.update_url:
        new_URL = args.update_url[0]
        old_URL = args.update_url[1]
        update_query_url = """UPDATE accounts SET url = %s WHERE url = %s"""
        cursor.execute(update_query_url, (new_URL, old_URL, ))

    if args.update_username:
        new_username = args.update_username[0]
        URL = args.update_username[1]
        update_query_usrname = """UPDATE accounts SET username = %s WHERE url = %s"""
        cursor.execute(update_query_usrname, (new_username, URL ))

    if args.update_password:
        print("Entrer l'ancien password: ")
        new_password = args.update_password[0]
        URL = args.update_password[1]
        update_query_passwd = """UPDATE accounts SET password = %s WHERE url = %s"""
        cursor.execute(update_query_passwd, (new_password, URL ))

    if args.list:
        cursor.execute("SELECT * from accounts")
        record = cursor.fetchall()
        for i in range(len(record)):
            entry = record[i]
            for j in range(len(entry)):
                titles = ["URL: ", "Username: ", "Password: "]
                if titles[j] == "Password: ":
                    bytes_row = entry[j]
                    password = master_password.decrypt_password(bytes_row, master_password_hash)
                    print("Password: " + str(password.decode('utf-8')))
                else:
                    print(titles[j] + entry[j])
            print( "----------")
    connection.commit()
    cursor.close()
main()

