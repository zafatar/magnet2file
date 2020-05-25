# yify-seedr.py

from __future__ import print_function  # Pyt 3

import argparse
import enum

from signal import signal, SIGINT
from sys import exit

from yifyseedr.Yify import Yify, MAX_NUMBER
from yifyseedr.ShowRSS import ShowRSS

from yifyseedr.Seedr import Seedr

from utils.utils import current_connection

from utils.nordvpn import get_best_available_server, get_country_list, print_country_list

from config import app_config

curr_conn = current_connection()

print("IP: {}".format(curr_conn['ip']))
print("Country: {}".format(curr_conn['country']))

config = app_config(env_name='local')

countries = get_country_list()
# print_country_list(countries=countries)


class Sources(enum.Enum):
    YIFY = "yify"
    SHOWRSS = "showrss"
    SEEDR = "seedr"


parser = argparse.ArgumentParser(description='Movie / Series Finder')
parser.add_argument("-s", "--source", help="source for the movies and series. Ex. yify, showrss")
parser.add_argument("-l", "--latest", help="get latest movies", action="store_true")
parser.add_argument("-c", "--search", help="search string for the movie and series")
parser.add_argument("-f", "--folder", help="Folder into where the file to be downloaded")
args = parser.parse_args()

seedr = Seedr({'email': config.SEEDR_USERNAME, 'password': config.SEEDR_PASSWORD})

source = args.source

print("Source: {}".format(source))


def handler(signal_received, frame):
    # Handle any cleanup here
    print('\n\nExiting...')
    exit(0)


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    print('Running. Press CTRL-C to exit.')

    if source.lower() == Sources.YIFY.value.lower():
        film_dict = None
        if args.search:
            film_dict = Yify.search_movies(args.search)
        elif args.latest:
            film_dict = Yify.get_latest_films()
        else:
            print("no command found")

        if film_dict is not None:
            Yify.print_films(film_dict)

            film_number = input("Select a movie for details [1.." + str(MAX_NUMBER) + "] :")
            selected_film = film_dict[int(film_number)]

            for torrent in selected_film.torrents:
                print("{} - {} - {}".format(torrent.type, torrent.size, torrent.magnet))
                if torrent.type.startswith('1080p'):
                    seedr.add_file_from_magnet(torrent.magnet)

    elif source.lower() == Sources.SHOWRSS.value.lower():
        series_dict = None

        if args.search:
            print("Searching for: {}".format(args.search))
            series_dict = ShowRSS.get_series(args.search)

        ShowRSS.print_films(series_dict)
        film_number = input("Select a movie for details [1.." + str(len(series_dict)) + "] :")
        selected_film = series_dict[int(film_number)]

        for torrent in selected_film.torrents:
            print("{} - {} - {}".format(torrent.type, torrent.size, torrent.magnet))
            if torrent.type.startswith('1080p'):
                seedr.add_file_from_magnet(torrent.magnet)

    elif source.lower() == Sources.SEEDR.value.lower():
        # list folders.
        folder_dict = seedr.get_folders_list()
        Seedr.print_folders(folder_dict)

        folder_number = input("Select a folder for details [1.." + str(len(folder_dict)) + "] :")
        selected_folder = folder_dict[int(folder_number)]

        print(selected_folder)

        folder_dict = seedr.get_folders_list(folder_id=selected_folder.get('id'))
        Seedr.print_folders(folder_dict)

        file_number = input("Select a file to download [1.." + str(len(folder_dict)) + "] :")
        selected_file = folder_dict[int(file_number)]

        print(selected_file)
        downloaded_file = seedr.get_file(file_id=selected_file.get('id'),
                                         file_name=selected_file.get('name'),
                                         folder=args.folder)

    else:
        print("{} : Not a valid source".format(source))
