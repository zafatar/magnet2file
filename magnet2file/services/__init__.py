# -*- coding: utf-8 -*-

import enum


class Services(enum.Enum):
    YIFY = "yts.mx"
    SHOWRSS = "showrss.info"
    SEEDR = "seedr.com"
    OPENSUBTITLES = "opensubtitles.org"

    def as_array():
        return list(Services)
