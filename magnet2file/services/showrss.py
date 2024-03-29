# -*- coding: utf-8 -*-
#
# services/showrss.py
#
"""ShowRSS module containing class and functions to interact with Seedr data
coming from its API.
"""
import requests
from lxml import html
from lxml.html import HtmlElement
from utils.utils import sanitize_search_string

from magnet2file.services import Services, Service, SourceService
from magnet2file.models.series import Series
from magnet2file.models.torrent import Torrent


MAIN_URL = "https://showrss.info"
MAX_NUMBER = 20


class ShowRSS(SourceService):
    """
    ShowRSS.info class
    """

    CODE = Services.SHOWRSS
    seedr_service = None

    def run(self):
        """
        Run instructions for the ShowRSS service
        """
        search_string = input("Search in ShowRSS: ")

        search_string = sanitize_search_string(search_string)

        series = ShowRSS.search_series(search_string)
        no_series = len(series)

        if no_series > 0:
            ShowRSS.print_series(series=series)

            series_number = input(f"\nSelect a series for details [1..{no_series}]: ")

            selected_series = series[int(series_number) - 1]

            ShowRSS.get_series_torrents(series=selected_series)

            ShowRSS.print_torrents(torrents=selected_series.torrents)

            no_torrents = len(selected_series.torrents)
            film_number = input(f"\nSelect an episode to download [1..{no_torrents}]: ")
            selected_torrent = selected_series.torrents[int(film_number) - 1]

            self.save_torrent_to_seedr(torrent=selected_torrent)
        else:
            print(f"No series found for `{search_string}`\n")

    @staticmethod
    def search_series(search_string: str = None) -> list:
        """This method searches the movies by using the search string.

        Args:
            search_string (str): search string. Default to None.

        Returns:
            list: list of Series instances as list
        """
        search_url = f"{MAIN_URL}/browse/"

        response = requests.get(search_url, verify=True, timeout=5)
        tree = html.fromstring(response.content)

        series_nodes = tree.xpath(f'//option[text()[contains(., "{search_string}")]]')
        series = []

        if len(series_nodes) >= 1:
            print(f"\n{len(series_nodes)} found for `{search_string}`\n")

            for series_node in series_nodes:
                serie = ShowRSS._extract_series(series_node)
                series.append(serie)
        else:
            print(f"No series found with `{search_string}` keyword.")

        return series

    @staticmethod
    def get_series_torrents(series: Series = None) -> None:
        """This method retrieves the list of torrents for the given series.

        Args:
            series (Series, optional): Series whose episodes to be downloaded.
            Defaults to None.
        """
        response = requests.get(series.link, verify=True, timeout=5)
        tree = html.fromstring(response.content)

        links = tree.xpath('//ul[@class="user-timeline"]/li')

        for link_node in links:
            torrent = ShowRSS._extract_torrent(torrent_node=link_node)
            series.torrents.append(torrent)

        print(f"\n{len(series.torrents)} episodes/links found in `{series.title}`\n")

    @staticmethod
    def print_series(series: list = None) -> None:
        """This method prints the given series dict.

        Args:
            series (dict): list of series as dict.
        """
        max_title_length = Service.max_title_size(entities=series)

        for index, serie in enumerate(series):
            padded_title = str(serie.title).ljust(max_title_length)
            print(f"{str(index + 1).rjust(3)} - {padded_title}")

    @staticmethod
    def _extract_series(series_node: HtmlElement = None) -> Series:
        """This method extracts Series instance from given HtmlElement instance.

        Args:
            series_node (HtmlElement, optional): series node with option
            element. Defaults to None.

        Returns:
            Series: Series instance
        """
        series_id = series_node.get("value")
        title = series_node.text

        series = Series(title=title, link=f"{MAIN_URL}/browse/{series_id}")

        return series

    @staticmethod
    def _extract_torrent(torrent_node: HtmlElement = None) -> Torrent:
        """This method extracts Torrent instance from given HtmlElement instance.

        Args:
            series_node (HtmlElement, optional): html node containing
            file data. Defaults to None.

        Returns:
            Torrent: Torrent instance.
        """
        magnet_link = torrent_node.xpath(".//@href")
        title = torrent_node.text_content().strip()
        resolution = "1080p"
        size = "0 Gb"

        return Torrent(
            title=title, resolution=resolution, size=size, magnet=magnet_link
        )
