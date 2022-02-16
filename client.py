# -*- coding: utf-8 -*-
#
# yify-seedr-v2.py
#
from __future__ import print_function

from signal import signal, SIGINT
from sys import exit

from utils.ipchecker import IPChecker
from utils.nordvpn import get_country_list
from utils.utils import yes_or_no

from config import get_config

from yifyseedr.services import Services
from yifyseedr.services.Seedr import Seedr
from yifyseedr.services.ShowRSS import ShowRSS
from yifyseedr.services.Yify import Yify

# Load the config
config = get_config()

# Get the country list from NV
countries = get_country_list()


def handler(signal_received, frame):
    # Handle any cleanup here
    print('\n\nExiting...\nBye.\n')
    exit(0)


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    # Check the connection IP and location.
    ipchecker = IPChecker(service=config.IPCHECKER_SERVICE)

    curr_conn = ipchecker.check()
    country = curr_conn.get('country')
    country_name = countries[curr_conn.get('country')].get('name')
    ip = curr_conn.get('ip')

    print(f"Country: {country_name} ({country}) ({ip})")

    # Ask if we'd like to proceed within current country.
    proceed = yes_or_no(f"Do you like to proceed within {country_name}?")

    if not proceed:
        print("OK, quitting...")
        exit()

    # List the available services.
    print("\nAvailable services:")
    services_as_list = Services.as_array()

    for index, service in enumerate(services_as_list):
        index = index + 1
        print("{} - [{}] - [{}]".format(str(index).rjust(3),
                                        service.name,
                                        service.value))

    selected_service_index = input("\nSelect the service [1..4]: ")
    selected_service = services_as_list[int(selected_service_index) - 1]

    print(f"\nSelected service: {selected_service}")

    # Pick the service and then run it.
    service = None
    seedr_service = Seedr({
        'email': config.SEEDR_USERNAME,
        'password': config.SEEDR_PASSWORD
    })

    if selected_service == Services.YIFY:
        service = Yify(seedr_service)
    elif selected_service == Services.SHOWRSS:
        service = ShowRSS(seedr_service)
    elif selected_service == Services.SEEDR:
        service = seedr_service

    if service:
        service.run()
