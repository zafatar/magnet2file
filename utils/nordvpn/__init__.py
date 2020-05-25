# utils/nordvpn/__init__.py

import json
import requests

NV_URL = "https://nordvpn.com//wp-admin/admin-ajax.php"


def get_country_list():
    action = "servers_countries"
    URL = "{}?action={}".format(NV_URL, action)
    ip_json = requests.get(URL).text

    countries = json.loads(ip_json)

    results = {}
    for country in countries:
        result = {
            'id': country.get('id'),
            'code': country.get('code'),
            'name': country.get('name'),
            'servers_count': country.get('servers_count')
        }

        results[country.get('name')] = result

    return results


def print_country_list(countries=None):
    for country_name in countries:
        country = countries.get(country_name)
        print("{} : {} : {} ({})".format(country.get('id'),
                                         country.get('code'),
                                         country_name,
                                         country.get('servers_count')))


def get_best_available_server(country_id=0):
    action = "servers_recommendations"
    URL = "{}?action={}&filters={'country_id':{}}".format(NV_URL, action, 174)
    ip_json = requests.get(URL).text
    print(URL)

    result = json.loads(ip_json)
    return result
