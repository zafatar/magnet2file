# -*- coding: utf-8 -*-
"""IPService class for the parent of IP Checker classes
"""
from abc import ABC, abstractmethod
from requests import Response, get


CHECK_URL = None


class IPService(ABC):
    """Parent class for the IP services
    """
    # pylint: disable=too-few-public-methods

    check_url = CHECK_URL

    def check(self) -> dict:
        """This method checks the service connection and returns
        IP and country code.

        Raises:
            Exception: Unsuccessful connection attempt

        Returns:
            dict: IP and country code as dict.
        """
        res = self._get_check_url()

        if res.status_code != 200:
            raise Exception('Unsuccessful connection attempt', res.status_code)

        ip_value = self._ip(res)
        country = self._country(res)

        return {
            'ip': ip_value,
            'country': country
        }

    def _get_check_url(self):
        return get(self.check_url)

    @abstractmethod
    def _ip(self, res: Response = None) -> str:
        pass

    @abstractmethod
    def _country(self, res: Response = None) -> str:
        pass
