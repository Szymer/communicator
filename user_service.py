import argparse
import psycopg2
from models.models import User
from clcrypto import check_password

""" cursor = cur
db connection variables below 
"""
USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
DB = "communicator_db"
"""
parser arguments
"""
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="users list", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
parser.add_argument("-t", "--to", help=" send to user")
parser.add_argument("-s", "--send", help="send message", action="store_true")

args = parser.parse_args()




def check_if_user_exist_in_db(cur, username):
    sql = """ SELECT username FROM users"""
    cur.execute(sql)
    for row in cur:
        if username == row[0]:
            return True
    return False


def validate_password_len(password):
    if len(password) < 8:
        raise Exception("the password should be 8 characters long \n try again")
    else:
        return True


def create_new_user(cur, username, password):
    if not check_if_user_exist_in_db(cur, username):
        if validate_password_len(password):
            new_user = User(username, password)
            new_user.save_to_db(cur)
            print(f"user {username} added to Data Base")
    else:
        raise Exception(f"user: {username} already exist in database")


def check_if_password_is_proper(cur, password, username):
    sql = """SELECT hashed_password From users 
                WHERE username=%s;"""
    value = username
    cur.execute(sql, (value,))
    hashed_pass = cur.fetchone()[0]
    if check_password(password, hashed_pass):
        return True
    else:
        return False


def pass_change(cur, username, password, n_pass):
    if check_if_user_exist_in_db(cur, username):
        if check_if_password_is_proper(cur, password, username):
            logged_user = User.load_user_by_username(cur, username)
            new_password = n_pass
            logged_user.hashed_password = new_password
            logged_user.save_to_db(cur)
            print("password changed")
        else:
            raise Exception("WRONG Password or Username access denied")


def delete_user(cur, username, password):
    logged_user = User.load_user_by_username(cur, username)

    if not logged_user:
        raise Exception("WRONG Password or Username access denied")
    elif check_if_password_is_proper(cur, password, username):
            logged_user.delete(cur)
            print(f"user {username} delete from  Data Base")
    else:
        raise Exception("WRONG Password or Username access denied")


def print_all_users(cur):
    all_users = User.load_all_users(cur)
    for user in all_users:
        print(user)


if __name__ == '__main__':

    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=DB)
        conn.autocommit = True
        cursor = conn.cursor()

        if args.username and args.password and args.new_pass and args.edit:
            pass_change(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_new_user(cursor, args.username, args.password)
        elif args.list:

            print_all_users(cursor)
        else:
            parser.print_help()
        cursor.close()
        conn.close()

    except psycopg2.OperationalError as err:
        print("Connection Error: ", err)


