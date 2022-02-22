# -*- coding: utf-8 -*-
"""Series data model
"""


class Series:
    """
    Series class
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, title=None, link=None):
        self.title = title
        self.link = link
        self.torrents = []

    def __repr__(self):
        return f'<Series: {self.title} ({self.link})>'
