# ShowRSS.py

import requests
from lxml import html

from magnet2file.models.film import Film
from magnet2file.models.torrent import Torrent
from magnet2file.services import Services
from magnet2file.services.seedr import Seedr


MAIN_URL = "https://showrss.info"
MAX_NUMBER = 20


class ShowRSS:
    """
    ShowRSS.info class
    """
    CODE = Services.SHOWRSS
    seedr_service = None

    def __init__(self, seedr_service: Seedr = None):
        self.seedr_service = seedr_service

    def run(self):
        search_string = input("Search in ShowRSS: ")

        series_full_name, series_dict = ShowRSS.search_series(search_string)

        if series_dict is not None:
            print(f"\n{len(series_dict)} episodes/links found in `{series_full_name}`\n")

            ShowRSS.print_films(series_dict)

            film_number = input(f"\nSelect a series for details [1..{len(series_dict)}]: ")
            selected_film = series_dict[int(film_number)]

            for torrent in selected_film.torrents:
                print(torrent)
                if torrent.type.startswith('1080p'):
                    self.seedr_service.add_file_from_magnet(torrent.magnet)
        else:
            print(f"No series found for `{search_string}`\n")

    @staticmethod
    def search_series(search_string):
        search_url = MAIN_URL + "/browse/"

        response = requests.get(search_url, verify=True, timeout=5)
        tree = html.fromstring(response.content)

        series = tree.xpath(f'//option[text()[contains(., "{search_string}")]]')
        series_id = None

        if len(series) >= 1:
            print(f"\n{len(series)} found for `{search_string}`\n")

            ShowRSS.print_series(series=series)
            no_series = len(series)

            series_number = input(f"\nSelect a series to download [1..{no_series}]: ")
            series_id = series[int(series_number)-1].get('value')
            series_full_name = series[int(series_number)-1].text

            if series_id is not None:
                series_url = search_url + str(series_id)

                response = requests.get(series_url, verify=True, timeout=5)
                tree = html.fromstring(response.content)

                links = tree.xpath('//ul[@class="user-timeline"]/li')

                films = {}
                count = 1
                for link in links:
                    magnet_link = link.xpath('.//@href')
                    title = link.text_content().strip()

                    film = Film(title=title, link=None)

                    if '1080p' in title:
                        torrent = Torrent(type='1080p', size=0, magnet=magnet_link)
                        film.torrents.append(torrent)

                        films[count] = film
                        count += 1

                return series_full_name, films
        else:
            print(f"No series found with `{search_string}` keyword.")

    @staticmethod
    def print_films(film_dict):
        max_title_length = 0
        for count, film in film_dict.items():
            if len(film.title) > max_title_length:
                max_title_length = len(film.title)

        for count, film in film_dict.items():
            print("{} - {} - {}".format(str(count).rjust(3),
                                        str(film.title).ljust(max_title_length),
                                        film.link))

    @staticmethod
    def print_series(series):
        max_title_length = 0
        for series_name in series:
            if len(series_name) > max_title_length:
                max_title_length = len(series_name)

        count = 1
        for series_name in series:
            print("{} - {}".format(str(count).rjust(3),
                                   str(series_name.text).ljust(max_title_length)))
            count += 1
