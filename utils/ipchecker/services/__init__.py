# -*- coding: utf-8 -*-
"""IPService class for the parent of IP Checker classes
"""
from requests import Response, get

CHECK_URL = None


class IPService:
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

    def _get_check_url(self):
        # TODO: Add error control and handling.
        return get(self.check_url)

    def _ip(self, res: Response = None) -> str:
        return "Not Implemented"

    def _country(self, res: Response = None) -> str:
        return "Not Implemented"
