# -*- coding: utf-8 -*-
#
# services/Yify.py
#
"""Yify module containingclass and functions to interact with Seedr data
coming from its API.
"""
from urllib.parse import quote
import requests
from lxml import html
from lxml.html import HtmlElement
from utils.utils import update_progress, sanitize_search_string

from magnet2file.services import Services, Service
from magnet2file.services.seedr import Seedr
from magnet2file.models.film import Film
from magnet2file.models.torrent import Torrent

MAIN_URL = "https://yts.mx"
MAX_NUMBER = 20


class Yify(Service):
    """
    Yify class
    """
    CODE = Services.YIFY
    seedr_service = None

    def __init__(self, seedr_service: Seedr = None):
        """Default constructor of YIFY

        Args:
            seedr_service (Seedr): service dependency
        """
        if seedr_service is None:
            raise Exception('Seedr service required')

        self.seedr_service = seedr_service

    def run(self):
        """
        Run instructions for the Yify service
        """
        search_string = input("Search in Yify: ")

        search_string = sanitize_search_string(search_string)

        films = Yify.search_movies(search_string)
        no_films = len(films)

        if no_films > 0:
            Yify.print_films(films)

            film_number = input(f"\nSelect a movie for details [1..{len(films)}]: ")
            selected_film = films[int(film_number) - 1]

            for torrent in selected_film.torrents:
                print(torrent)
                if torrent.resolution.startswith('1080p'):
                    self.seedr_service.add_file_from_magnet(torrent.magnet)
        else:
            print(f"No film found for `{search_string}`\n")

    @staticmethod
    def search_movies(search_string: str = None) -> dict:
        """This method searches the movies by using the search string.

        Args:
            search_string (str): search string. Default to None.

        Returns:
            dict: list of Film instances as dict
        """
        search_url = f'{MAIN_URL}/browse-movies/{quote(search_string)}/all/all/0/latest/0/all'
        response = requests.get(search_url)
        tree = html.fromstring(response.content)

        # Keep the track of how many results found.
        number_of_movies = 0
        movies_found = tree.xpath('//h2/b/text()')

        if movies_found[0] is not None:
            pieces = movies_found[0].split(' ')
            number_of_movies = int(pieces[0])

        film_nodes = tree.xpath('//div[contains(@class, "browse-movie-wrap")]')

        films = []
        for film_node in film_nodes:
            film = Yify._extract_film(film_node)

            Yify.get_film_torrents(film)

            films.append(film)
            update_progress(len(films), number_of_movies)

        return films

    @staticmethod
    def get_latest_films(page_number: int = 1) -> dict:
        """This method returns the latest movies from the main page.

        Args:
            page_number (int, optional): page number. Defaults to 1.

        Returns:
            dict: list of Film instances as dict
        """
        browse_url = f'{MAIN_URL}/browse-movies?page={str(page_number)}'
        response = requests.get(browse_url)
        tree = html.fromstring(response.content)

        number_of_movies = 20   # films per page by default

        films_node = tree.xpath('//div[contains(@class, "browse-movie-wrap")]')

        films = []
        for film_node in films_node:
            film = Yify._extract_film(film_node)

            Yify.get_film_torrents(film)

            films.append(film)
            update_progress(len(films), number_of_movies)

        return films

    @staticmethod
    def get_film_torrents(film: Film = None) -> None:
        """This method retrieves the torrents for the given film.

        Args:
            film (Film, optional): Film whose torreents to be found.
            Defaults to None.
        """
        film_details = requests.get(film.link)
        film_details_tree = html.fromstring(film_details.content)

        torrents = film_details_tree.xpath('.//div[@class="modal-torrent"]')
        for torrent_node in torrents:
            torrent = Yify._extract_torrent(torrent_node)
            film.torrents.append(torrent)

    @staticmethod
    def print_films(films: list = None) -> None:
        """This method prints the given film list.

        Args:
            films (list): list of films.
        """
        max_title_length = Service.max_title_size(films)

        for index, film in enumerate(films, 1):
            padded_index = str(index).rjust(3)
            rating = str(film.rating).rjust(8)
            title = str(film.title).ljust(max_title_length)

            print(f'{padded_index} - [{film.year}] - [{rating}] - {title} - {film.link}')

    @staticmethod
    def _extract_film(film_node: HtmlElement = None) -> Film:
        """This method extracts Film instance from given HtmlElement instance.

        Args:
            film_node (HtmlElement, optional): html node containing file data.
                Defaults to None.

        Returns:
            Film: Film instance.
        """
        title = film_node.xpath('.//a[@class="browse-movie-title"]/text()')
        link = film_node.xpath('.//a[@class="browse-movie-link"]/@href')
        year = film_node.xpath('.//div[@class="browse-movie-year"]/text()')
        rating = film_node.xpath('.//h4[@class="rating"]/text()')

        film = Film(title=title[0],
                    link=link[0],
                    year=year[0],
                    rating=rating[0])

        return film

    @staticmethod
    def _extract_torrent(torrent_node: HtmlElement = None) -> Torrent:
        """This method extracts Torrent instance from given
        HtmlElement instance.

        Args:
            torrent_node (HtmlElement, optional): html node containing
            torrent data.
                Defaults to None.

        Returns:
            Torrent: Torrent instance.
        """
        torrent_type = torrent_node.xpath('.//div[@class="modal-quality"]//text()')
        torrent_size = torrent_node.xpath('.//p[@class="quality-size"]/text()')
        magnet_link = torrent_node.xpath('.//a[contains(@class, "magnet")]//@href')

        torrent = Torrent(resolution=torrent_type[0], size=torrent_size[1], magnet=magnet_link)

        return torrent
