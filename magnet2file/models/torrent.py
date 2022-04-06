# -*- coding: utf-8 -*-
"""Torrent data model
"""


class Torrent:
    """
    Torrent class
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, title=None, resolution=None, size=None, magnet=None):
        self.title = title
        self.resolution = resolution
        self.size = size
        self.magnet = magnet

    def __repr__(self):
        return f'<Torrent: {self.resolution} ({self.size}) - {self.title} = {self.magnet[0:50]}>'  # noqa: E501
