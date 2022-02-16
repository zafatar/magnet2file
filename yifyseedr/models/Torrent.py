# Torrent.py

class Torrent:
    """
    Torrent class
    """
    def __init__(self, type=None, size=None, magnet=None):
        self.type = type
        self.size = size
        self.magnet = magnet

    def __repr__(self):
        return "<Torrent {} - {} - {}".format(self.type,
                                              self.size,
                                              self.magnet)
