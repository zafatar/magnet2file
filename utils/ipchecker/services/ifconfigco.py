# -*- coding: utf-8 -*-
"""
Library for the ifconfig.co related calls
"""

from requests import Response
from utils.ipchecker.services import IPService


CHECK_URL = "https://ifconfig.co/json"
SERVICE_NAME = "ifconfig.co"


class IfconfigCo(IPService):
    """IP service class for IfconfigCo"""

    # pylint: disable=too-few-public-methods

    check_url = CHECK_URL
    service_name = SERVICE_NAME

    def _ip(self, res: Response) -> str:
        ip_value = str(res.json().get("ip"))
        return ip_value

    def _country(self, res: Response) -> str:
        country = str(res.json().get("country_iso"))
        return country
