# -*- coding: utf-8 -*-
"""Services class contains the list of available services
and their unique code names with values (websites).
"""
import enum
from abc import ABC, abstractmethod
from magnet2file.exceptions.services import MissingServiceError

from magnet2file.models.torrent import Torrent


class Services(enum.Enum):
    """Services class for the available services
    as Enum.
    """

    YIFY = "yts.mx"
    SHOWRSS = "showrss.info"
    SEEDR = "seedr.com"
    EZTV = "eztvx.to"

    @staticmethod
    def as_array() -> list:
        """This returns the available services as list

        Returns:
            list: available services as list
        """
        return list(Services)


class Service(ABC):
    """Abstract class for the Service classes."""

    CODE = None

    @abstractmethod
    def run(self):
        """
        Service run instruction
        """

    @staticmethod
    def max_title_size(entities: list = None) -> int:
        """This calculates the max title length based on the
        given list of films / torrents as dict.

        Args:
            entities (list, optional): list of films / torrents.
            Defaults to None.

        Returns:
            int: max length of title in the given films / torrents.
        """
        max_title_length = 0

        for entity in entities:
            if len(entity.title) > max_title_length:
                max_title_length = len(entity.title)

        return max_title_length


class SourceService(Service):
    """Service class for the source services (Yify, ShowRSS, Eztv)"""

    def __init__(self, seedr_service: Service = None):
        """Default constructor of YIFY / ShowRSS / Eztv

        Args:
            seedr_service (Seedr): service dependency
        """
        if seedr_service is None:
            raise MissingServiceError("Seedr service required")

        self.seedr_service = seedr_service

    @staticmethod
    def print_torrents(torrents: list = None) -> None:
        """This method prints the given torrents dict.

        Args:
            series (dict): list of episodes as dict.
        """
        max_title_length = Service.max_title_size(entities=torrents)

        for index, film in enumerate(torrents, 1):
            padded_index = str(index).rjust(3)
            padded_title = str(film.title).ljust(max_title_length)

            print(f"{padded_index} - {padded_title}")

    def save_torrent_to_seedr(
        self, torrent: Torrent = None, only1080p: bool = True
    ) -> None:
        """This method saves the given Torrent into seedr service.

        Args:
            torrent (Torrent, optional): torrent to be save to seedr.
                Defaults to None.
            only1080p (bool, optional): save only if 1080p.
                Defaults to False.

        Returns:
            _type_: _description_
        """
        # TODO: To be extended  # noqa
        if only1080p and torrent.resolution.startswith("1080p"):
            self.seedr_service.add_file_from_magnet(torrent.magnet)
        else:
            print(
                "The resolution of the selected episode is not 1080p. Please try again."
            )
