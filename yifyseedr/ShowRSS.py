# ShowRSS.py

import requests
from lxml import html

from . import Film, Torrent


MAIN_URL = "https://showrss.info"
MAX_NUMBER = 20


class ShowRSS:
    """
    ShowRSS.info class
    """
    @staticmethod
    def get_series(series_name):
        search_url = MAIN_URL + "/browse/"

        response = requests.get(search_url, verify=True, timeout=5)
        tree = html.fromstring(response.content)

        series = tree.xpath('//option[text()[contains(., "{}")]]'.format(series_name))
        series_id = None

        if len(series) >= 1:
            ShowRSS.print_series(series=series)
            series_number = input("Select a series for details [1.." + str(len(series)) + "] :")
            series_id = series[int(series_number)-1].get('value')

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

                return films
        else:
            print("No series found with `{}` keyword.".format(series_name))

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
