# -*- coding: utf-8 -*-
"""Library for the IfconfigMe related calls
"""

from requests import Response
from utils.ipchecker.services import IPService


CHECK_URL = "https://ifconfig.me/ip"


class IfconfigMe(IPService):
    """IP service class for IfconfigMe
    """
    # pylint: disable=too-few-public-methods

    check_url = CHECK_URL

    def _ip(self, res: Response = None) -> str:
        ip_value = str(res.content.decode("utf-8"))
        return ip_value

    def _country(self, res: Response = None) -> str:
        country = str(res.content.decode("utf-8"))
        return country
