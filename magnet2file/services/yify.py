# -*- coding: utf-8 -*-
#
# services/Yify.py
#
import requests
from urllib.parse import quote
from lxml import html
from utils.utils import update_progress

from magnet2file.services import Services
from magnet2file.services.seedr import Seedr
from magnet2file.models.film import Film
from magnet2file.models.torrent import Torrent

MAIN_URL = "https://yts.mx"
MAX_NUMBER = 20


class Yify:
    """
    Yify class
    """
    CODE = Services.YIFY
    seedr_service = None

    def __init__(self, seedr_service: Seedr = None):
        self.seedr_service = seedr_service

    def run(self):
        search_string = input("Search in Yify: ")

        # TODO: Sanitize the search string
        film_dict = Yify.search_movies(search_string)

        if film_dict is not None:
            print(f"\n{len(film_dict)} found for `{search_string}`\n")
            Yify.print_films(film_dict)

            film_number = input(f"\nSelect a movie for details [1..{len(film_dict)}]: ")
            selected_film = film_dict[int(film_number)]

            for torrent in selected_film.torrents:
                print(torrent)
                if torrent.type.startswith('1080p'):
                    self.seedr_service.add_file_from_magnet(torrent.magnet)
        else:
            print(f"No film found for `{search_string}`\n")

    @staticmethod
    def search_movies(search_string):
        search_url = MAIN_URL + "/browse-movies/" + quote(search_string) + "/all/all/0/latest/0/all"
        response = requests.get(search_url)
        tree = html.fromstring(response.content)

        # How many movies found :
        number_of_movies = 0
        # movies_found = tree.xpath('//h2/span[text()[contains(., "Movies found")]]/text()')
        movies_found = tree.xpath('//h2/b/text()')

        if movies_found[0] is not None:
            pieces = movies_found[0].split(' ')
            number_of_movies = int(pieces[0])

        films = tree.xpath('//div[contains(@class, "browse-movie-wrap")]')

        count = 1
        film_dict = {}
        for film_node in films:
            if count > MAX_NUMBER:
                continue

            title = film_node.xpath('.//a[@class="browse-movie-title"]/text()')
            link = film_node.xpath('.//a[@class="browse-movie-link"]/@href')
            year = film_node.xpath('.//div[@class="browse-movie-year"]/text()')
            rating = film_node.xpath('.//h4[@class="rating"]/text()')

            film = Film(title=title[0],
                        link=link[0],
                        year=year[0],
                        rating=rating[0])

            film_details = requests.get(link[0])
            film_details_tree = html.fromstring(film_details.content)

            # print("{} - [{}] - {} - {}".format(str(count).rjust(3), film.year, film.title, film.link))

            torrents = film_details_tree.xpath('.//div[@class="modal-torrent"]')
            for torrent in torrents:
                torrent_type = torrent.xpath('.//div[@class="modal-quality"]//text()')
                torrent_size = torrent.xpath('.//p[@class="quality-size"]/text()')
                magnet_link = torrent.xpath('.//a[contains(@class, "magnet")]//@href')

                torrent = Torrent(type=torrent_type[0], size=torrent_size[1], magnet=magnet_link)
                film.torrents.append(torrent)

                # print("{} - {} - {}".format(str(torrent_type[0]).rjust(10), torrent_size[1], magnet_link))
                # result = seedr.add_file_from_magnet(magnet_link)
                # print("{} - {}", str(result['user_torrent_id']), result['title'])
                # print("{} - {}".format(str(torrent_type[0]).rjust(10), torrent_size[1]))

            # print("".join(["-"] * 100))

            film_dict[count] = film
            update_progress(count, number_of_movies)
            count += 1

        return film_dict

    @staticmethod
    def get_latest_films(page_number=1):
        browse_url = MAIN_URL + "/browse-movies?page=" + str(page_number)
        response = requests.get(browse_url)
        tree = html.fromstring(response.content)

        films = tree.xpath('//div[contains(@class, "browse-movie-wrap")]')

        count = 1
        film_dict = {}
        for film_node in films:
            if count > MAX_NUMBER:
                continue

            title = film_node.xpath('.//a[@class="browse-movie-title"]/text()')
            link = film_node.xpath('.//a[@class="browse-movie-link"]/@href')
            year = film_node.xpath('.//div[@class="browse-movie-year"]/text()')
            rating = film_node.xpath('.//h4[@class="rating"]/text()')

            film = Film(title=title[0], link=link[0], year=year[0], rating=rating[0])

            film_details = requests.get(link[0])
            film_details_tree = html.fromstring(film_details.content)

            # print("{} - [{}] - {} - {}".format(str(count).rjust(3), film.year, film.title, film.link))

            torrents = film_details_tree.xpath('.//div[@class="modal-torrent"]')
            for torrent in torrents:
                torrent_type = torrent.xpath('.//div[@class="modal-quality"]//text()')
                torrent_size = torrent.xpath('.//p[@class="quality-size"]/text()')
                magnet_link = torrent.xpath('.//a[contains(@class, "magnet")]//@href')

                torrent = Torrent(type=torrent_type[0], size=torrent_size[1], magnet=magnet_link)
                film.torrents.append(torrent)

                # print("{} - {} - {}".format(str(torrent_type[0]).rjust(10), torrent_size[1], magnet_link))
                # result = seedr.add_file_from_magnet(magnet_link)
                # print("{} - {}", str(result['user_torrent_id']), result['title'])
                # print("{} - {}".format(str(torrent_type[0]).rjust(10), torrent_size[1]))

            # print("".join(["-"] * 100))

            film_dict[count] = film
            update_progress(count * int(100 / MAX_NUMBER))
            count += 1

        return film_dict

    @staticmethod
    def print_films(film_dict):
        max_title_length = 0
        for count, film in film_dict.items():
            if len(film.title) > max_title_length:
                max_title_length = len(film.title)

        for count, film in film_dict.items():
            print("{} - [{}] - [{}] - {} - {}".format(str(count).rjust(3),
                                                      film.year,
                                                      str(film.rating).rjust(8),
                                                      str(film.title).ljust(max_title_length),
                                                      film.link))
