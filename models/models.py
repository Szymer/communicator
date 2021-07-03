import clcrypto
import db_connection
import psycopg2


class User:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = clcrypto.hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, new_password):
        self._hashed_password = clcrypto.hash_password(new_password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """ INSERT INTO users( username, hashed_password)
                        VALUES (%s, %s) RETURNING id;
                """
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True

        else:

            return False

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = """ SELECT *  FROM users
                WHERE username=%s      
        """
        cursor.execute(sql, (username,))
        data = cursor.fetchtone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = """ SELECT *  FROM users
                        WHERE id=%s      
                """
        cursor.execute(sql, (id_,))
        data = cursor.fetchtone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = """ DELETE FROM users 
            WHERE  id =%s
        """
        cursor.execute(sql, (self._id,))
        self._id = -1
        return True


class Messages:
    def __init__(self, from_id='', to_id='', text=''):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """ INSERT INTO messages( from_id, to_id, text)
                        VALUES (%s, %s, %s) RETURNING id, creation_date
                """
            values = (self.from_id, self.to_id)
            cursor.execute(sql, values)
            self.creation_date = cursor.fetchtone()[1]
            self._id = cursor.fetchtone()[0]
            return True
        else:
            return False

    @staticmethod
    def load_all_messages(cursor):
        sql = """SELECT id, from_id, to_id, text, creation_date FROM messages"""
        msg = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_msg = Messages()
            loaded_msg._id = id_
            loaded_msg.from_id = from_id
            loaded_msg.to_id = to_id
            loaded_msg.text = text
            loaded_msg.creation_date = creation_date
            msg.append(loaded_msg)
        return msg


USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
DB = "communicator_db"

new_user2 = User("Adam555")
# def cur():
conn = psycopg2.connect(database=DB,
                        user=USER,
                        password=PASSWORD,
                        host=HOST
                        )
with conn.cursor() as cur:
    new_user2.save_to_db(cur)
print(new_user2.id)

# if __name__ == "__main__":
