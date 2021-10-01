from kivy import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')
Config.set('graphics', 'resizable', False)

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from os import path
import threading
from queue import Queue
from Client import *
from kivy.core.window import Window
from kvStyle.myWidgets import AsyncImageButton, Book


fonts_path = path.abspath("fonts")
kvStyle_path = path.abspath("kvStyle")

# kivy version
kivy.require(kivy.__version__)
LabelBase.register(name="Arial", fn_regular=path.join(fonts_path, "arial.ttf"))


def add_book_widgets(manager, book):
    book_image = AsyncImage(source=book.image,
                            pos=(600, 90))

    name_label = Label(text=' / ' + book.book_name,
                       font_size=22,
                       font_name="Arial",
                       pos=(300, 300))

    author_label = Label(text=book.author,
                         font_size=22,
                         font_name="Arial",
                         pos=(300, 270))

    summary_label = Label(text=book.summary,
                          font_size=16,
                          font_name="Arial",
                          halign="right",
                          size=(400, 400),
                          padding=(50, 20),
                          size_hint=(None, None))

    # Change screen to book_screen.
    manager.current = "book_screen"

    # Add the widget to the float layout.
    manager.ids.book_window.ids.float.add_widget(book_image)
    manager.ids.book_window.ids.float.add_widget(name_label)
    manager.ids.book_window.ids.float.add_widget(author_label)
    manager.ids.book_window.ids.scroll.add_widget(summary_label)


class LoginWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    labelName = ObjectProperty(None)

    def callback(self):
        self.labelName.text = "Hello " + self.username.text + "!"

    def login(self):
        """ Login function, [1] == Login. """
        data_to_transfer = [1]
        d = {}
        if self.username.text != "" and self.password != "":
            d['USERNAME'] = self.username.text
            d['PASSWORD'] = self.password.text
            data_to_transfer.append(d)
        else:
            return None

        q.put(data_to_transfer)
        return self.isLogin()

    def isLogin(self):
        """ Get the info from the client, and check if account is found,
            Add the books form the database. """
        isFound = q1.get()  # Get if the account is in the system.
        if isFound:
            self.update_wish_list_window()
        return isFound

    def update_wish_list_window(self):
        """ Show all the wish-list books for the account. """
        my_books = q2.get()
        for book in my_books:
            book_details = book[2:]  # Get the relevant info, book info.
            my_book = Book(book_details, self.manager)
            my_book.bind(on_press=self.update_book_page)
            self.manager.ids.wish_list_window.ids.grid.add_widget(my_book)  # Show the image on the grid.

    def update_book_page(self, book):
        """ Change the current screen to book page.
            Update the book page by book that was clicked."""

        add_book_widgets(self.manager, book)
        q4.put(book)


class SignupWindow(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm_password = ObjectProperty(None)

    def signup(self):
        """ Signup function, [2] == Signup. """
        data_to_transfer = [2]
        d = {}
        if self.password.text == self.confirm_password.text and self.username.text != "" and self.email.text != "":
            d['USERNAME'] = self.username.text
            d['EMAIL'] = self.email.text
            d['PASSWORD'] = self.password.text
            data_to_transfer.append(d)
        else:
            return None

        # Write to the Queue the data to have in the main function.
        q.put(data_to_transfer)

        return data_to_transfer


class WishListWindow(Screen):
    width1, height1 = Window.size
    bookNameText = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WishListWindow, self).__init__(**kwargs)

        scroll = ScrollView(size_hint_y=.73,
                            pos_hint={"center_x": 0.5, "center_y": 0.2},
                            do_scroll_x=False,
                            do_scroll_y=True)

        self.layout = GridLayout(size=(self.width1, self.height1),
                                 size_hint_x=1,
                                 size_hint_y=5,
                                 cols=int(self.width / 100 * 5),
                                 height=Window.minimum_height,
                                 row_default_height=180,
                                 row_force_default=True)

        self.ids['grid'] = self.layout  # Set the id for the main GridLayout.

        # Add layout to ScrollView.
        scroll.add_widget(self.layout)

        # Add ScrollView to window.
        self.add_widget(scroll)

    def add_new_book(self):
        """ Add new book to Database and add it to the screen, [3] == NewBook"""
        username = self.manager.ids.login_window.ids.username.text
        q.put([3, [self.bookNameText.text, username]])

        # Handle the book_details to show up.
        def pop_book():
            book_details = q3.get()
            if book_details is None:
                pass
            else:
                print("print on screen... ")
                my_book = Book(book_details, self.manager)
                my_book.bind(on_press=self.update_book_page)
                self.layout.add_widget(my_book)

        # Thread that get info and print to screen.
        pop_book_thread = threading.Thread(target=pop_book, args=(), daemon=True)
        pop_book_thread.start()

    def update_book_page(self, book):
        """ Change the current screen to book page.
            Update the book page by book that was clicked."""

        add_book_widgets(self.manager, book)
        q4.put(book)


class BooksReadWindow(Screen):
    pass


class BookWindow(Screen):

    def __init__(self, **kwargs):
        super(BookWindow, self).__init__(**kwargs)

        self.float = FloatLayout(size_hint=(0.2, 0.4))
        self.scroll_float = FloatLayout(size_hint=(0.6, 1))

        scroll = ScrollView(size_hint_y=.90,
                            pos_hint={"center_x": 0.60, "center_y": 0.15},
                            do_scroll_x=True,
                            do_scroll_y=True)

        self.ids['float'] = self.float  # Set the id for the main FloatLayout.
        self.ids['scroll'] = scroll

        self.add_widget(self.float)

        self.scroll_float.add_widget(scroll)
        self.add_widget(self.scroll_float)

    def reset_page(self):
        """ Clear the screen and right after it build the init again. """
        q4.queue.clear()  # Clear the queue when data is not relevant.

        self.canvas.clear()
        self.__init__()

    def delete_book(self):
        """ Delete the book and Clear the page. """
        book = q4.get()  # Book Widget
        book_name = book.book_name

        q.put([4, [book_name]])  # Pass the info to client.

        self.manager.ids.wish_list_window.ids.grid.remove_widget(book)  # Remove the book from the WishList window.
        self.reset_page()  # Clear widgets from book page.


class WindowManager(ScreenManager):
    pass


class LibraryApp(App):

    def build(self):
        return Builder.load_file(path.join(kvStyle_path, "kvStyle.kv"))


if __name__ == "__main__":

    # Use to transfer data between the main thread and the others.
    q = Queue()  # data_to_transfer -> [1\2\3, {}]
    q1 = Queue()  # isFound -> True / Flase
    q2 = Queue()  # wish_list_book -> [(), ()]
    q3 = Queue()  # book_details  --> [name, author, summary, image]
    q4 = Queue()  # book that pass for delete.

    # Start new thread for the network connection.
    x = threading.Thread(target=main, args=(q, q1, q2, q3, ), daemon=True)
    x.start()

    # Run the kivy application.
    LibraryApp().run()
