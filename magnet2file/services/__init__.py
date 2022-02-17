# -*- coding: utf-8 -*-
"""Services class contains the list of available services
and their unique code names with values (websites).
"""
import enum


class Services(enum.Enum):
    YIFY = "yts.mx"
    SHOWRSS = "showrss.info"
    SEEDR = "seedr.com"
    OPENSUBTITLES = "opensubtitles.org"

    @staticmethod
    def as_array():
        return list(Services)
