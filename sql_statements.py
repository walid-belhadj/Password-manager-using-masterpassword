

def insert_db_row():
    insert_query = """INSERT INTO accounts (url, username, password) VALUES (%s, %s,%s)"""
    return insert_query

def delete_db_row():
    sql_delete_query = """Delete from accounts where url = %s"""
    return sql_delete_query

def update_db_url():
    update_query_url = """UPDATE accounts SET url = %s WHERE url = %s"""
    return update_query_url

def update_db_usrname():
    update_query_usrname = """UPDATE accounts SET username = %s WHERE url = %s"""
    return update_query_usrname

def update_db_passwd():
    update_query_passwd = """UPDATE accounts SET password = %s WHERE url = %s"""
    return update_query_passwd

def select_db_entry():
    select_query = """SELECT * from accounts where url = %s"""
    return select_query

def update_db():
    update_db = """UPDATE accounts SET password = %s"""
    return update_db
