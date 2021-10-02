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

    def id_tracker(self, table, id):
        # Keep track for ID.
        count_id = 1
        try:
            # Keep track of UserID column.
            order = '''SELECT * FROM {0} ORDER BY {1} DESC LIMIT 1'''.format(table, id)
            count_id = self.cur.execute(order).fetchall()[0][0] + 1

        except sqlite3.IntegrityError and IndexError as e:
            print(str(e))

        return count_id

    def add_user_signup(self, user):
        """ Add user to the database """

        # Keep track for ID.
        count_id = self.id_tracker("Users", "UserID")

        # Insert the values to the database.
        try:
            self.cur.execute('''INSERT INTO Users VALUES (?, ?, ?, ?)''', (count_id, user[0], user[1], user[2]))
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
            return True
        else:
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

    def add_new_book(self, book_details):
        """ Add new book to the Books table. """

        # Keep track for ID.
        count_id = self.id_tracker("Books", "BookID")

        name, author, description, image = book_details[0], book_details[1], book_details[2], book_details[3]

        try:
            self.cur.execute(''' INSERT INTO Books VALUES (?, ?, ?, ?, ?)''', (count_id, name, author,
                                                                               description, image))
        except sqlite3.IntegrityError as e:
            print("Book Already exist ", e)

        self.conn.commit()  # Commit the changes.
        print("GOOD JOB!!!")

    def add_book_to_wishlist(self, book_details, username):
        """ Add new book to wishlist. """

        def get_id(question):
            return self.cur.execute(question).fetchall()[0][0]

        book_name = book_details[0]
        # Keep track for ID.
        count_id = self.id_tracker("WishList", "ID")

        # Sql question.
        user_id = ''' SELECT UserID FROM Users WHERE Username="{0}" '''.format(username)
        book_id = ''' SELECT BookID FROM Books WHERE Name="{0}" '''.format(book_name)

        user_id = get_id(user_id)
        book_id = get_id(book_id)

        try:
            self.cur.execute(''' INSERT INTO WishList Values (?, ?, ?) ''', (count_id, user_id, book_id))
        except sqlite3.IntegrityError as e:
            print("Book Already exist in WishList", e)

        self.conn.commit()  # Commit the changes.

    def delete_wish_list_book(self, book_name, username):
        """ Delete book from database. """

        # Find the book ID for deletion.
        sql = ''' SELECT BookID FROM Books WHERE Name="{0}" '''.format(book_name)
        book_id = self.cur.execute(sql).fetchone()[0]

        # Find the user ID for deletion.
        sql = ''' Select UserID FROM Users WHERE Username="{0}" '''.format(username)
        user_id = self.cur.execute(sql).fetchone()[0]

        # Delete book by BookID.
        sql = ''' DELETE FROM WishList WHERE UserID={0} AND BookID={1} '''.format(user_id, book_id)
        self.cur.execute(sql)

        self.conn.commit()
