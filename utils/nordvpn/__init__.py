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

        results[country.get('code')] = result

    return results


def print_country_list(countries=None):
    for country_code, country in countries.items():
        print("{} : {} : {} ({})".format(country.get('id'),
                                         country_code,
                                         country.get('name'),
                                         country.get('servers_count')))


def get_best_available_server(country_id=0):
    action = "servers_recommendations"
    country_id = 174
    URL = f"{NV_URL}?action={action}&filters={'country_id':{country_id}}"

    ip_json = requests.get(URL).text

    result = json.loads(ip_json)
    return result
