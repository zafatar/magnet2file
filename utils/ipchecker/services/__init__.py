# -*- coding: utf-8 -*-

import requests as r

CHECK_URL = None


class IPService():

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
        return r.get(self.check_url)
