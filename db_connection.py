import psycopg2


USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
DB = "communicator_db"


def cur():
    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=DB)
        conn.autocommit = True

        return conn.cursor()
    except psycopg2.errors.OperationalError as err:
        print("Connection Error: ", err)
