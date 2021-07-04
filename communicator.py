import argparse
import psycopg2
from models.models import Messages, User
from user_service import check_if_password_is_proper

""" 
cursor = cur
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
parser.add_argument("-t", "--to", help=" send to user")
parser.add_argument("-l", "--list", help="messages list", action="store_true")
parser.add_argument("-s", "--send", help="send message", action="store_true")

args = parser.parse_args()

""""
Mian app
"""


def user_checker(cur, username, password):
    logged_user = User.load_user_by_username(cur, username)
    if logged_user:
        if check_if_password_is_proper(cur, password, username):
            return True
        else:
            raise Exception("WRONG Password  access denied")
    else:
        raise Exception("WRONG  Username access denied")


def adress_checker(cur, to_id):
    user = User.load_user_by_id(cur, to_id)
    if user:
        return True
    else:
        raise Exception(f"User whit ID: {to_id} not exist")


def messages_list(cur, username, password):
    if user_checker(cur, username, password):
        messages = Messages.load_all_messages(cur)
        for message in messages:
            print(message)


def message_send(cur, username, password, to_id):
    if user_checker(cur, username, password):
        if adress_checker(cur, to_id):
            sender = User.load_user_by_username(cur, username)
            sender_id = sender.id
            text = ""
            while len(text) == 0 or len(text) > 255:
                text = input("wpisz wiadomość: \n")
                if len(text) > 255:
                    print("message is long!")
            message = Messages(sender_id, to_id, text)
            message.save_to_db(cur)


if __name__ == '__main__':

    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=DB)
        conn.autocommit = True
        cursor = conn.cursor()

        if args.username and args.password and args.t and args.s:
            message_send(cursor, args.username, args.password, args.t)
        if args.username and args.password and args.list:

            messages_list(cursor, args.username, args.password)
        else:
            parser.print_help()

    except psycopg2.OperationalError as err:
        print("Connection Error: ", err)
