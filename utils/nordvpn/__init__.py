# -*- coding: utf-8 -*-
"""Library for the NordVPN related calls
"""
import json
import requests

NV_URL = "https://nordvpn.com//wp-admin/admin-ajax.php"


def get_country_list():
    """This returns the available countries as a dict
    whose keys are country codes and values are data blob.

    Returns:
        dict: list of countries by country code
    """
    action = "servers_countries"
    url = f"{NV_URL}?action={action}"
    try:
        ip_json = requests.get(url, timeout=10).text
    except requests.exceptions.Timeout:
        print("Cannot get country list. Timeout")
        return {}

    countries = json.loads(ip_json)

    results = {}
    for country in countries:
        result = {
            "id": country.get("id"),
            "code": country.get("code"),
            "name": country.get("name"),
            "servers_count": country.get("servers_count"),
        }

        results[country.get("code")] = result

    return results


def print_country_list(countries: dict) -> None:
    """This prints the list of countries given as a dict

    Args:
        countries (dict, optional): List of countries. Defaults to None.
    """
    for country_code, country in countries.items():
        print(
            "- {%s} [{%s}] {%s} ({%s})",
            country.get("id"),
            country_code,
            country.get("name"),
            country.get("servers_count"),
        )


def get_best_available_server(country_id: int = 0):
    """This gets the best available server from the given country.

    Args:
        country_id (int, optional): country id for best available servers.
            Defaults to 0.

    Returns:
        dict: Best available servers from the given country.
    """
    action = "servers_recommendations"
    country_id = 174
    url = f"{NV_URL}?action={action}&filters={'country_id':{country_id}}"

    ip_json = requests.get(url).text

    result = json.loads(ip_json)
    return result
