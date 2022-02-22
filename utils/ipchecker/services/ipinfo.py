# -*- coding: utf-8 -*-
"""Library for the IPInfo related calls
"""
from requests import Response
from utils.ipchecker.services import IPService


CHECK_URL = "https://ipinfo.io"


class IPInfo(IPService):
    """IP service class for IPInfo
    """
    # pylint: disable=too-few-public-methods

    check_url = CHECK_URL

    def __init__(self, service: str = None):
        self.service = service

    def _ip(self, res: Response = None) -> str:
        ip_value = str(res.json().get("ip"))
        return ip_value

    def _country(self, res: Response = None) -> str:
        country = str(res.json().get("country"))
        return country
