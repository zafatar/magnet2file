"""
This is init module for magnet2file
"""
from .models.film import Film
from .models.torrent import Torrent

from .services.seedr import Seedr
from .services.yify import Yify, MAX_NUMBER
