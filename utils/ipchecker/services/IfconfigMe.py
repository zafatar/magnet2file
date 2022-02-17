# -*- coding: utf-8 -*-
"""Library for the IfconfigMe related calls
"""

from requests import Response
from utils.ipchecker.services import IPService


CHECK_URL = "https://ifconfig.me/ip"


class IfconfigMe(IPService):

    check_url = CHECK_URL

    def _ip(self, res: Response = None) -> str:
        ip = str(res.content.decode("utf-8"))
        return ip

    def _country(self, res: Response = None) -> str:
        country = str(res.content.decode("utf-8"))
        return country
