# -*- coding: utf-8 -*-
#
# services/Seedr.py
#
"""Seedr class and functions to interact with Seedr data
coming from its API.
"""
import requests

import logging

from lxml import html
from lxml.html import HtmlElement
from utils.utils import sanitize_search_string

from magnet2file.services import Services, SourceService
from magnet2file.models.torrent import Torrent

MAIN_URL = "https://eztvx.to"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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

            self.save_torrent_to_seedr(torrent=selected_torrent)
        else:
            print(f"No series found for `{search_string}`\n")

    @staticmethod
    def search_torrents(search_string: str) -> list:
        """This method searches the movies by using the search string.

        Args:
            search_string (str): search string. Default to None.

        Returns:
            list: list of Series instances as list
        """
        search_url = f"{MAIN_URL}/search/?q1={search_string}&search=Search"

        logger.debug(f'Searching for `{search_string}` in Eztv...')
        logger.debug(f'URL: {search_url}')

        cookies = {}

        response = requests.get(search_url, verify=True, timeout=5, cookies=cookies)

        response = requests.post(
            search_url,
            verify=True,
            timeout=5,
            cookies=cookies,
            data={"layout": "def_wlinks"},
        )

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
    def _extract_torrent(torrent_node: HtmlElement) -> Torrent:
        """This method extracts Torrent instance from given HtmlElement instance.

        Args:
            series_node (HtmlElement, optional): html node containing
            file data. Defaults to None.

        Returns:
            Torrent: Torrent instance.
        """
        magnet_links = torrent_node.xpath(".//td/a[starts-with(@href,'magnet')]/@href")
        magnet_link = magnet_links[0]

        title = torrent_node.xpath(".//td/a[@class='epinfo']")[0].text_content().strip()

        size = torrent_node.xpath(".//td[@class='forum_thread_post']")[3].text_content().strip()
        
        resolution = Eztv.get_resolution_from_title(title)

        return Torrent(
            title=title, resolution=resolution, size=size, magnet=magnet_link
        )

    @staticmethod
    def get_resolution_from_title(title: str) -> str: 
        """This method extracts resolution from the title of the torrent.

        Args:
            title (str): title of the torrent.

        Returns:
            str: resolution of the torrent.
        """
        if "2160p" in title:
            resolution = "2160p"
        if "1080p" in title:
            resolution = "1080p"
        elif "720p" in title:
            resolution = "720p"
        elif "480p" in title:
            resolution = "480p"
        elif "4K" in title:
            resolution = "4K"
        else: 
            resolution = "Unknown"

        return resolution
