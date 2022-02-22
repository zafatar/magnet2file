# -*- coding: utf-8 -*-
"""Film data model
"""


class Film:
    """
    Film class
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, title=None, year=None, link=None, rating=None):
        self.title = title
        self.year = year
        self.link = link
        self.rating = rating
        self.torrents = []

    def __repr__(self):
        return f'<Film: {self.title} ({self.year}) [{self.rating}]>'
