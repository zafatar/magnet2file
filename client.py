# -*- coding: utf-8 -*-
"""This is the client which interacts with the user
and collects the input and presents the input from
different services.
"""
from __future__ import print_function

from signal import signal, SIGINT
import sys
import logging
import argparse

from utils.ipchecker import IPChecker
from utils.nordvpn import get_country_list
from utils.utils import yes_or_no

from config import get_config

from magnet2file.services import Services
from magnet2file.services.service_factory import ServiceFactory

# Read and load command line params
parser = argparse.ArgumentParser(description='Magnet2File client')
parser.add_argument("--debug", help="activate debug mode", action="store_true")
args = parser.parse_args()
debug = args.debug

# Prepare and set the logger
logger = logging.getLogger(__name__)
logging.basicConfig()

if debug:
    logger.setLevel(logging.DEBUG)
    logger.debug("****************************")
    logger.debug("*** Debug mode is active ***")
    logger.debug("****************************")
else:
    logger.setLevel(logging.INFO)

# Load the config
config = get_config()

# Get the country list from NV
countries = get_country_list()


def handler(signal_received, frame):
    """This is a handler method which runs with a system signal

    Args:
        signal_received (Signal): Signal type
        frame (Frame): Frame which received the signal
    """
    logger.info('%s - %s', signal_received, frame)

    # Handle any cleanup here
    print('\n\nExiting...\nBye.\n')
    sys.exit()


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
        sys.exit()

    # List the available services.
    print("\nAvailable services:")
    services_as_list = Services.as_array()

    for index, service in enumerate(services_as_list):
        index = index + 1
        print(f"{str(index).rjust(3)} - [{service.name}] - [{service.value}]")

    selected_service_index = input(f"\nSelect the service [1..{len(services_as_list)}]: ")
    selected_service = services_as_list[int(selected_service_index) - 1]

    print(f"\nSelected service: {selected_service}")

    # Pick the service and then run it.
    service = ServiceFactory.get_service(selected_service, config)

    if service:
        service.run()
