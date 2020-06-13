"""Defines the phone class that contains the details of a phone."""
import webbrowser

class phone(object):
    """This class provides a way to store phone related information.

    Attributes:
        title: A string to store the title of the phone.
        storyline: A string to store the basic plot of the phone.
        poster_image_url: A string to store the URL of the phone poster.
        trailer_youtube_url: A string to store the URL of the phone trailer.
        release_date: A string to store the release date of the phone.
    """

    def __init__(self, phone_name, phone_features, poster_image):
        """Initialises phone class instance variables."""
        self.phone_name = phone_name
        self.phone_features = phone_features
        self.poster_image_url = poster_image
        

    def show_trailer(self):
        """Plays the phone trailer in the web browser."""
        webbrowser.open(self.trailer_youtube_url)
