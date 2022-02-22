# -*- coding: utf-8 -*-
"""This is the ipchecker module init file.
"""
import enum
from requests import Response

from utils.ipchecker.services.ifconfigme import IfconfigMe
from utils.ipchecker.services.ipinfo import IPInfo
from utils.ipchecker.services.ipapi import IPApi

VERSION = '0.0.1'


class Services(enum.Enum):
    """Available services as enum list
    """
    IPINFO = 'ipinfo.io'
    IPAPI = 'ip-api.com'
    IFCONFIG = 'ifconfig.me'


class IPChecker:
    """IP Checked service abstract class
    """
    # pylint: disable=too-few-public-methods

    check_url = None

    def __init__(self, service: str = None):
        self.service = service

    def check(self) -> dict:
        """This method checks the selected service and
        returns the IP and counttry code as dict.

        Raises:
            Exception: Undefined IP service requested
            Exception: Can't find the current IP

        Returns:
            dict: IP and country code as dict.
        """
        if self.service == Services.IPINFO.value.lower():
            service = IPInfo()
        elif self.service == Services.IFCONFIG.value.lower():
            service = IfconfigMe()
        elif self.service == Services.IPAPI.value.lower():
            service = IPApi()
        else:
            raise Exception("Undefined IP service requested")

        print(f"IP Checker Service name: {self.service}")

        connection = service.check()
        if connection is None:
            raise Exception("Can't find the current IP")

        return connection

    def _ip(self, res: Response = None) -> str:
        """
        This extracts IP from the service
        """

    def _country(self, res: Response = None) -> str:
        """
        This extracts country code from the service
        """
