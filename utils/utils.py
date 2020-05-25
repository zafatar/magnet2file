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
