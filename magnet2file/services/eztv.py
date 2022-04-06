# -*- coding: utf-8 -*-
#
# services/Seedr.py
#
"""Seedr class and functions to interact with Seedr data
coming from its API.
"""
import requests

from lxml import html
from lxml.html import HtmlElement
from utils.utils import sanitize_search_string

from magnet2file.services import Services, Service, SourceService
from magnet2file.models.torrent import Torrent

MAIN_URL = "https://eztv.ro"


class Eztv(SourceService):
    """
    Seedr class
    """
    CODE = Services.EZTV
    seedr_service = None

    def run(self) -> None:
        """
        Run instructions for the Eztv service
        """
        search_string = input("Search in Eztv: ")

        search_string = sanitize_search_string(search_string)

        torrents = Eztv.search_torrents(search_string)
        no_torrents = len(torrents)

        if no_torrents > 0:
            Eztv.print_torrents(torrents)

            film_number = input(f"\nSelect an episode to download [1..{no_torrents}]: ")
            selected_torrent = torrents[int(film_number) - 1]

            if selected_torrent.resolution.startswith('1080p'):
                self.seedr_service.add_file_from_magnet(selected_torrent.magnet)
            else:
                print("The resolution of the selected episode is not 1080p. Please try again.")
        else:
            print(f"No series found for `{search_string}`\n")

    @staticmethod
    def search_torrents(search_string: str = None) -> list:
        """This method searches the movies by using the search string.

        Args:
            search_string (str): search string. Default to None.

        Returns:
            list: list of Series instances as list
        """
        search_url = f'{MAIN_URL}/search/?q1={search_string}&search=Search'

        response = requests.get(search_url, verify=True, timeout=5)

        tree = html.fromstring(response.content)

        torrent_nodes = tree.xpath("//tr[@class='forum_header_border']")
        torrents = []
        no_torrent_nodes = len(torrent_nodes)

        if no_torrent_nodes >= 1:
            print(f"\n{no_torrent_nodes} torrents found for `{search_string}`\n")

            for torrent_node in torrent_nodes:
                torrent = Eztv._extract_torrent(torrent_node=torrent_node)
                torrents.append(torrent)
        else:
            print(f"No series found with `{search_string}` keyword.")

        return torrents

    @staticmethod
    def print_torrents(torrents: list = None) -> None:
        """This method prints the given episodes dict.

        Args:
            series (dict): list of episodes as dict.
        """
        max_title_length = Service.max_title_size(films=torrents)

        for index, film in enumerate(torrents, 1):
            padded_index = str(index).rjust(3)
            padded_title = str(film.title).ljust(max_title_length)

            print(f'{padded_index} - {padded_title}')

    @staticmethod
    def _extract_torrent(torrent_node: HtmlElement = None) -> Torrent:
        """This method extracts Film instance from given HtmlElement instance.

        Args:
            series_node (HtmlElement, optional): html node containing
            file data. Defaults to None.

        Returns:
            Torrent: Torrent instance.
        """
        magnet_link = torrent_node.xpath(".//td/a[starts-with(@href,'magnet')]/@href")[0]
        title = torrent_node.xpath(".//td/a[@class='epinfo']")[0].text_content().strip()

        torrent = Torrent(title=title,
                          resolution='1080p',
                          size=0,
                          magnet=magnet_link)

        return torrent
