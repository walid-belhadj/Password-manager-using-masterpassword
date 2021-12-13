import psycopg2

def connection_db():
    # je me connecte au stckage desidentifiants
    try:
        connection = psycopg2.connect("dbname=passwordmanager user=postgres password=postgres")
        return connection
    except (Exception, psycopg2.Error) as error:
        print(error)
