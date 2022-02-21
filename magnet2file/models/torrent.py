# -*- coding: utf-8 -*-
"""Torrent data model
"""


class Torrent:
    """
    Torrent class
    """
    def __init__(self, resolution=None, size=None, magnet=None):
        self.resolution = resolution
        self.size = size
        self.magnet = magnet

    def __repr__(self):
        return f'<Torrent: {self.resolution} ({self.size}) - {self.magnet}'
