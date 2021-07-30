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
            self.cur.execute('''CREATE TABLE USERS (UserID int NOT NULL PRIMARY KEY,
                                                    USERNAME varchar(255) NOT NULL UNIQUE CHECK(LENGTH(USERNAME)<=30),
                                                    PASSWORD varchar(255) NOT NULL,
                                                    EMAIl varchar(255) NOT NULL UNIQUE)''')

        except sqlite3.OperationalError as e:
            print("Table already exits ", e)

    def add_user_signup(self, user):
        """ Add user to the database """
        count_id = 1
        try:
            # Keep track of UserID column.
            i = self.cur.execute('''SELECT * FROM USERS ORDER BY UserID DESC LIMIT 1''')
            count_id = i.fetchall()[0][0] + 1

        except sqlite3.IntegrityError and IndexError:
            print("BIG PROBLEM...")

        # Insert the values to the database.
        new_user = '''INSERT INTO USERS VALUES ({0}, "{1}", "{2}", "{3}")'''.format(count_id, user[0], user[1], user[2])
        print(new_user)
        try:
            self.cur.execute(new_user)
        except sqlite3.IntegrityError as e:
            print("USERNAME already taken: ", e)

        self.conn.commit()  # Commit the changes.

        # Print the Users column.
        for row in self.cur.execute('SELECT * FROM USERS ORDER BY UserID'):
            print(row)

    def login(self, user):
        """ Log user to the database """
        find_user = ''' SELECT * FROM USERS WHERE USERNAME="{0}" AND PASSWORD="{1}"; '''.format(user[0], user[1])
        if self.cur.execute(find_user).fetchone():
            print("FOUND")
        else:
            print("NOT FOUND")
