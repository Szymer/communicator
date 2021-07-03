import psycopg2

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
DB = "communicator_db"


def cur():
    conn = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        database=DB)
    with  conn.cursor() as cursor:
        return cursor
