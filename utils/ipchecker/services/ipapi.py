# -*- coding: utf-8 -*-
"""Library for the IPApi related calls
"""
from requests import Response
from utils.ipchecker.services import IPService


CHECK_URL = "http://ip-api.com/json/?fields=61439"


class IPApi(IPService):
    """IP service class for IP-API
    """
    # pylint: disable=too-few-public-methods

    check_url = CHECK_URL

    def _ip(self, res: Response = None) -> str:
        ip_value = str(res.json().get("query"))
        return ip_value

    def _country(self, res: Response = None) -> str:
        country = str(res.json().get("countryCode"))
        return country
