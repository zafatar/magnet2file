# -*- coding: utf-8 -*-
"""Services class contains the list of available services
and their unique code names with values (websites).
"""
import enum


class Services(enum.Enum):
    """Services class for the available services
    as Enum.
    """
    YIFY = "yts.mx"
    SHOWRSS = "showrss.info"
    SEEDR = "seedr.com"
    OPENSUBTITLES = "opensubtitles.org"

    @staticmethod
    def as_array() -> list:
        """This returns the available services as list

        Returns:
            list: available services as list
        """
        return list(Services)
