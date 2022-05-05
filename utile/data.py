import sqlite3


def connect_db(db_filename) -> sqlite3.Connection:
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect(db_filename, check_same_thread=False)
    except sqlite3.Error as error:
        print("Failed to connect database", db_filename, error)
    finally:
        if sqlite_connection:
            return sqlite_connection


def select_data(db_conn, query, param):
    try:
        cur = db_conn.cursor()
        cur.execute(query, param)
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as error:
        print("Failed to select database", query, error)


def insert_data(db_conn, query, param):
    try:
        cur = db_conn.cursor()
        cur.execute(query, param)
        db_conn.commit()
        print("coucou")

    except sqlite3.Error as e:
        print("echec de la connexion :", e)


def update_data(db_conn, query, param):
    cur = db_conn.cursor()
    cur.execute(query, param)


def del_data(db_conn, query, param):
    cur = db_conn.cursor()
    cur.execute(query, param)


def disconnect_db(db_conn):
    db_conn.close()
