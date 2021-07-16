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
    pass


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
    LibraryApp().run()

