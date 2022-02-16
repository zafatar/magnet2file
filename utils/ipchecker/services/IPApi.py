# -*- coding: utf-8 -*-

from requests import Response
from utils.ipchecker.services import IPService


CHECK_URL = "http://ip-api.com/json/?fields=61439"


class IPApi(IPService):

    check_url = CHECK_URL

    def check(self) -> bool:
        res = self._get_check_url()

        if res.status_code != 200:
            raise Exception('Unsuccessful connection attempt', res.status_code)

        ip = self._ip(res)
        country = self._country(res)

        return {
            'ip': ip,
            'country': country
        }

    def _ip(self, res: Response = None) -> str:
        ip = str(res.json().get("ip"))
        return ip

    def _country(self, res: Response = None) -> str:
        country = str(res.json().get("country"))
        return country
