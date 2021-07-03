import psycopg2

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
DB = "communicator_db"
sql_db_create = """
CREATE DATABASE communicator_db;
"""
sql_crate_tab_users = """
CREATE TABLE users (
id serial primary key,
username varchar(255) UNIQUE ,
hashed_password varchar(80)
);
"""
sql_crate_tab_msg = """
CREATE TABLE messages (
id serial primary key,
from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
to_id INTEGER REFERENCES users(id) ON DELETE CASCADE,  
text text,
creation_date timestamp default now()

);

"""

"""
cerat data base
"""


def create_db(sql):
    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
        )
        conn.autocommit = True

        with conn.cursor() as cursor:

            try:
                cursor.execute(sql)
                print("data base created")
            except psycopg2.errors.DuplicateDatabase as err:
                print("Duplicate Database", err)
    except psycopg2.OperationalError as error:
        print("Connection error", error)
    else:
        conn.close()
        cursor.close()


"""
cerat table in database
"""


def create_table(sql, db):
    conn = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        database=db)
    conn.autocommit = True
    with conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
        except psycopg2.errors.DuplicateTable as err:
            print('Duplicate Table', err)
    conn.close()
    cursor.close()


def run():
    create_db(sql_db_create)
    create_table(sql_crate_tab_users, DB)
    create_table(sql_crate_tab_msg, DB)


run()
# if __name__ == "__main__":
#     run()
