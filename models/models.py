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

    def set_password(self, password, salt=""):
        self._hashed_password = clcrypto.hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, new_password):
        self.set_password(new_password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """ INSERT INTO users( username, hashed_password)
                        VALUES (%s, %s) RETURNING id """
            values = (f"{self.username}", f"{self.hashed_password}")
            cursor.execute(sql, values)
            cursor.close
            self._id = cursor.fetchone()[0]
            cursor.close()
            return True

        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                                       WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

            return False

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = """ SELECT id, username, hashed_password  FROM users
                WHERE username=%s      
        """

        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = """ SELECT *  FROM users
                        WHERE id=%s      
                """
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
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

    def __str__(self):
        return f" Id: [{self._id}] | User Name:{self.username} | Password:   {self.hashed_password}"


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
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            creation = cursor.fetchone()[1]
            new_id = cursor.fetchone()[0]
            self.creation_date = creation
            self._id = new_id
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

    def __str__(self):
        return f" Message from: {self.from_id} to: {self.to_id} \n" \
               f"{self.text}\n" \
               f" "

#
# new_user16 = User("Adam56665")
#
# new_user16.save_to_db(db_connection.cur())
# c = User.load_all_users(db_connection.cur())
# print(c)


# if __name__ == "__main__":
