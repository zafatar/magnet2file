# -*- coding: utf-8 -*-

from requests import Response
from utils.ipchecker.services import IPService


CHECK_URL = "http://ip-api.com/json/?fields=61439"


class IPApi(IPService):

    check_url = CHECK_URL

    def _ip(self, res: Response = None) -> str:
        ip = str(res.json().get("query"))
        return ip

    def _country(self, res: Response = None) -> str:
        country = str(res.json().get("countryCode"))
        return country
