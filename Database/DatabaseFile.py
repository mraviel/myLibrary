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
            self.cur.execute('''CREATE TABLE Users (UserID int NOT NULL PRIMARY KEY,
                                                    USERNAME varchar(255) NOT NULL UNIQUE CHECK(LENGTH(USERNAME)<=30),
                                                    PASSWORD varchar(255) NOT NULL,
                                                    EMAIl varchar(255) NOT NULL UNIQUE);''')

            self.cur.execute('''CREATE TABLE Books (BookID int NOT NULL PRIMARY KEY,
                                                    Name varchar(255) NOT NULL UNIQUE,
                                                    Author varchar(255) NOT NULL,
                                                    Description Text(255),
                                                    Image varchar(255));''')

            self.cur.execute('''CREATE TABLE WishList (ID int NOT NULL PRIMARY KEY,
                                                       UserID int NOT NULL REFERENCES Users(UserID),
                                                       BookID int NOT NULL REFERENCES Books(BookID));''')

            self.cur.execute('''CREATE TABLE BooksRead (ID int NOT NULL PRIMARY KEY,
                                                        UserID int NOT NULL REFERENCES Users(UserID),
                                                        BookID int NOT NULL REFERENCES Books(BookID));''')

        except sqlite3.OperationalError as e:
            print("Table already exits ", e)

    def add_user_signup(self, user):
        """ Add user to the database """
        count_id = 1
        try:
            # Keep track of UserID column.
            i = self.cur.execute('''SELECT * FROM Users ORDER BY UserID DESC LIMIT 1''')
            count_id = i.fetchall()[0][0] + 1

        except sqlite3.IntegrityError and IndexError:
            print("BIG PROBLEM...")

        # Insert the values to the database.
        new_user = '''INSERT INTO Users VALUES ({0}, "{1}", "{2}", "{3}")'''.format(count_id, user[0], user[1], user[2])
        print(new_user)
        try:
            self.cur.execute(new_user)
        except sqlite3.IntegrityError as e:
            print("USERNAME already taken: ", e)

        self.conn.commit()  # Commit the changes.

        # Print the Users column.
        for row in self.cur.execute('SELECT * FROM Users ORDER BY UserID'):
            print(row)

    def login(self, user):
        """ Log user to the database """
        find_user = ''' SELECT * FROM Users WHERE USERNAME="{0}" AND PASSWORD="{1}"; '''.format(user[0], user[1])
        if self.cur.execute(find_user).fetchone():
            print("FOUND")
            return True
        else:
            print("NOT FOUND")
            return False

    def all_wish_list_books(self, user):
        """ Func that return list of all WishList books.
        Return: [(), (), ()] """

        all_books = "SELECT WishList.ID, Users.USERNAME, Books.name, Books.Author, Books.Description, Books.Image " \
                    "FROM WishList " \
                    "INNER JOIN Users ON WishList.UserID=Users.UserID " \
                    "INNER JOIN Books ON WishList.BookID=Books.BookID " \
                    "WHERE Users.USERNAME='{0}' " \
                    "ORDER BY WishList.ID;".format(user[0])

        return self.cur.execute(all_books).fetchall()
