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
        self.color = (5, 5, 5)

    def on_release(self):
        print("on_release")
        self.color = (1, 1, 1, 1)
