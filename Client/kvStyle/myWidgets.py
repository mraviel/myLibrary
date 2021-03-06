from kivy.uix.button import ButtonBehavior
from kivy.uix.image import AsyncImage


class AsyncImageButton(ButtonBehavior, AsyncImage):
    """
    Class used to create an AsyncImageButton widget.
    :param  source: The source of the image.
            name: Filename of the image to be used as source.
    :return: The AsyncImageButton object.
    """

    def __init__(self, source, name=""):
        super(AsyncImageButton, self).__init__()
        self.source = source
        self.name = name

    def on_press(self):
        print("on_press")

    def on_release(self):
        print("on_release")


class Book(AsyncImageButton):

    """ Class that represent book. """

    def __init__(self, book_details, manager):
        self.book_details = book_details
        self.book_name, self.author, self.summary, self.image = self.book_details
        self.manager = manager

        super(Book, self).__init__(self.image)

    def on_press(self):
        super(Book, self).on_press()
