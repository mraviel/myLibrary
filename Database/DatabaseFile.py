import sqlite3
from sqlite3 import Error
from os import path


class Database:

    def __init__(self):
        self.conn = self.crate_connection()
        self.cur = self.conn.cursor()
        self.create_table()

    @staticmethod
    def crate_connection():
        """ Create a database connection to a SQLite database """
        db_file = 'dataB'
        dataB_path = path.abspath("Database")  # The path to the 'Database' Folder.
        try:
            conn = sqlite3.connect(path.join(dataB_path, db_file))  # Create the file in the direct folder.
            print(sqlite3.version)
            return conn
        except Error as e:
            print(e, 'ERROR')

    def create_table(self):
        """ Create a table to the database (Only once) """
        try:
            self.cur.execute('''CREATE TABLE USERS (ID int NOT NULL PRIMARY KEY,
                                                    USERNAME varchar(255) NOT NULL UNIQUE CHECK(LENGTH(USERNAME)<=30),
                                                    PASSWORD varchar(255) NOT NULL)''')

        except sqlite3.OperationalError as e:
            print("Table already exits ", e)

    def add_user_signup(self, user):
        """ Add user to the database """
        count_id = 1
        try:
            i = self.cur.execute('''SELECT * FROM USERS ORDER BY ID DESC LIMIT 1''')
            print(count_id)
            count_id = i.fetchall()[0][0] + 1
            print(count_id)
        except sqlite3.IntegrityError and IndexError:
            print("BIG PROBLEM...")

        new_user = '''INSERT INTO USERS VALUES ({0}, "{1}", "{2}")'''.format(count_id, user[0], user[1])
        print(new_user)
        try:
            self.cur.execute(new_user)
        except sqlite3.IntegrityError as e:
            print("USERNAME already taken: ", e)

        self.conn.commit()
        for row in self.cur.execute('SELECT * FROM USERS ORDER BY ID'):
            print(row)

    def login(self, user):
        """ Log user to the database """
        find_user = ''' SELECT * FROM USERS WHERE USERNAME="{0}" AND PASSWORD="{1}"; '''.format(user[0], user[1])
        if self.cur.execute(find_user).fetchone():
            print("FOUND")
        else:
            print("NOT FOUND")