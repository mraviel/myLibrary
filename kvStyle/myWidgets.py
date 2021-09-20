from kivy.uix.button import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label


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
        # self.color = (5, 5, 5)

    def on_release(self):
        print("on_release")
        # self.color = (1, 1, 1, 1)


class Book(AsyncImageButton):

    """ Class that represent book. """

    def __init__(self, book_details, manager):
        self.book_details = book_details
        self.book_name, self.author, self.summary, self.image = self.book_details
        self.manager = manager

        super(Book, self).__init__(self.image)

    def on_press(self):
        super(Book, self).on_press()

        self.book_page()

    def book_page(self):
        """ Book Page. Switch screen and Create widget for book page. """

        book_image = AsyncImage(source=self.image,
                                pos=(600, 90))

        name_label = Label(text=' / ' + self.book_name,
                           font_size=22,
                           font_name="Arial",
                           pos=(300, 300))

        author_label = Label(text=self.author,
                             font_size=22,
                             font_name="Arial",
                             pos=(300, 270))

        summary_label = Label(text=self.summary,
                              font_size=16,
                              font_name="Arial",
                              halign="right",
                              size=(400, 400),
                              padding=(50, 20),
                              size_hint=(None, None))

        # Change screen to book_screen.
        self.manager.current = "book_screen"

        # Add the widget to the float layout.
        self.manager.ids.book_window.ids.float.add_widget(book_image)
        self.manager.ids.book_window.ids.float.add_widget(name_label)
        self.manager.ids.book_window.ids.float.add_widget(author_label)
        self.manager.ids.book_window.ids.scroll.add_widget(summary_label)
