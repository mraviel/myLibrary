import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
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


fonts_path = path.abspath("fonts")
kvStyle_path = path.abspath("kvStyle")

# kivy version
kivy.require(kivy.__version__)
LabelBase.register(name="Arial", fn_regular=path.join(fonts_path, "arial.ttf"))


class LoginWindow(Screen):
    username = ObjectProperty(None)
    labelName = ObjectProperty(None)
    
    def callback(self):
        self.labelName.text = "Hello " + self.username.text + "!"


class SignupWindow(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm_password = ObjectProperty(None)

    def signup(self):
        data_to_transfer = [2]
        d = {}
        if self.password.text == self.confirm_password.text and self.username.text != "" and self.email.text != "":
            d['USERNAME'] = self.username.text
            d['EMAIL'] = self.email.text
            d['PASSWORD'] = self.password.text
            data_to_transfer.append(d)
            print(data_to_transfer)
        else:
            return None

        q.put(data_to_transfer)  # Write to the Queue the data to have in the main function.
        return data_to_transfer


class WishListWindow(Screen):
    pass


class BooksReadWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class LibraryApp(App):

    def build(self):
        return Builder.load_file(path.join(kvStyle_path, "kvStyle.kv"))


if __name__ == "__main__":
    q = Queue()  # Use to transfer data between the main thread and the others.

    # Start new thread for the network connection.
    x = threading.Thread(target=main, args=(q,))
    x.start()

    # Run the kivy application.
    LibraryApp().run()
