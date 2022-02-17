# -*- coding: utf-8 -*-
"""Library for the IPInfo related calls
"""
from requests import Response
from utils.ipchecker.services import IPService


CHECK_URL = "https://ipinfo.io"


class IPInfo(IPService):

    check_url = CHECK_URL

    def _ip(self, res: Response = None) -> str:
        ip = str(res.json().get("ip"))
        return ip

    def _country(self, res: Response = None) -> str:
        country = str(res.json().get("country"))
        return country
