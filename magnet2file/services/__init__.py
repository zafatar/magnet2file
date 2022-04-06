# -*- coding: utf-8 -*-
"""Services class contains the list of available services
and their unique code names with values (websites).
"""
import enum
from abc import ABC, abstractmethod


class Services(enum.Enum):
    """Services class for the available services
    as Enum.
    """
    YIFY = "yts.mx"
    SHOWRSS = "showrss.info"
    SEEDR = "seedr.com"
    OPENSUBTITLES = "opensubtitles.org"
    EZTV = "eztv.ro"

    @staticmethod
    def as_array() -> list:
        """This returns the available services as list

        Returns:
            list: available services as list
        """
        return list(Services)


class Service(ABC):
    """Abstract class for the Service classes.
    """
    CODE = None

    @abstractmethod
    def run(self):
        """
        Service run instruction
        """

    @staticmethod
    def max_title_size(films: list = None) -> int:
        """This calculates the max title length based on the
        given list of films as dict.

        Args:
            films (list, optional): list of films. Defaults to None.

        Returns:
            int: max length of title in the given films.
        """
        max_title_length = 0

        for film in films:
            if len(film.title) > max_title_length:
                max_title_length = len(film.title)

        return max_title_length


class SourceService(Service):
    """Service class for the source services (Yify, ShowRSS, Eztv)
    """
    def __init__(self, seedr_service: Service = None):
        """Default constructor of YIFY / ShowRSS / Eztv

        Args:
            seedr_service (Seedr): service dependency
        """
        if seedr_service is None:
            raise Exception('Seedr service required')

        self.seedr_service = seedr_service
