# utils.py

import json
import requests

IPINFO_URL = "https://ipinfo.io/json"


def current_connection():
    ip_json = requests.get(IPINFO_URL).text
    return json.loads(ip_json)


def update_progress(progress):
    print("\r [{0}{1}] {2}%".format('#'*(progress//10), ' '*(10 - progress//10), progress), end='')
    if progress == 100:
        print("")  # kind of eol


def pprint_dict(dict_to_print: None) -> None:
    max_title_length = 0
    for key, value in dict_to_print.items():
        if len(key) > max_title_length:
            max_title_length = len(key)

    for key, value in dict_to_print.items():
        print("\t{} - {}".format(str(key).ljust(max_title_length), value))
