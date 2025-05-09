# -*- coding: utf-8 -*-
"""
This is the client which interacts with the user
and collects the input and presents the input from
different services.
"""
from __future__ import print_function

import sys
import argparse
import pycountry

from utils.logging import logger

from utils.ipchecker import IPChecker
from utils.utils import yes_or_no

from utils.signal import add_sigint_handler

from config import get_config

from magnet2file.services import Services
from magnet2file.services.service_factory import ServiceFactory

# Read and load command line params
parser = argparse.ArgumentParser(description="Magnet2File client")
parser.add_argument("--debug", help="activate debug mode", action="store_true")
args = parser.parse_args()
debug = args.debug

# Prepare and set the logger
# logger = get_logger(__name__, debug)

# Load the config
config = get_config()


def main():
    """
    Main function
    """
    # Check the connection IP and location.
    ipchecker = IPChecker()

    curr_result = ipchecker.check()
    country = curr_result.get("country")
    country_name = pycountry.countries.get(alpha_2=country).name
    ip = curr_result.get("ip")

    print(f"Country: {country_name} ({country}) ({ip})")

    # Ask if we'd like to proceed within current country.
    proceed = yes_or_no(f"Do you like to proceed within {country_name}?")

    if not proceed:
        print("OK, quitting...")
        sys.exit()

    # List the available services.
    print("\nAvailable services:")
    services_as_list = Services.as_array()
    selected_service_index = -1

    while int(selected_service_index) not in range(1, len(services_as_list) + 1):
        if selected_service_index != -1:
            print("\nInvalid selection. Please try again.")

        for index, service in enumerate(services_as_list, start=1):
            print(f"{str(index).rjust(3)} - [{service.name}] - [{service.value}]")

        selected_service_index = input(
            f"\nSelect the service [1..{len(services_as_list)}]: "
        )

    selected_service = services_as_list[int(selected_service_index) - 1]

    print(f"\nSelected service: {selected_service}")

    # Pick the service and then run it.
    service = ServiceFactory.get_service(selected_service, config)

    if service:
        try:
            service.run()
        except Exception as exp: 
            logger.error(f"*** {exp} ***")    

if __name__ == "__main__":
    # Tell Python to run the handler() function when SIGINT is received
    add_sigint_handler()

    while True:
        main()
