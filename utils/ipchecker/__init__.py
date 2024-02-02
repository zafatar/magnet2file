# -*- coding: utf-8 -*-
"""This is the ipchecker module init file.
"""
import enum
from requests import Response

from utils.ipchecker.services.ifconfigme import IfconfigMe
from utils.ipchecker.services.ifconfigco import IfconfigCo
from utils.ipchecker.services.ipinfo import IPInfo
from utils.ipchecker.services.ipapi import IPApi

VERSION = "0.0.1"


class Services(enum.Enum):
    """Available services as enum list"""

    IPINFO = "ipinfo.io"
    IPAPI = "ip-api.com"
    IFCONFIG = "ifconfig.me"
    IFCONFIGCO = "ifconfig.co"


class IPChecker:
    """IP Checked service abstract class"""

    # pylint: disable=too-few-public-methods
    service = None

    def check(self) -> dict:
        """This method checks the selected service and
        returns the IP and counttry code as dict.

        Raises:
            Exception: Undefined IP service requested
            Exception: Can't find the current IP

        Returns:
            dict: IP and country code as dict.
        """

        # we need to check the services one by one and quit
        # if we find the current IP and country code
        try:
            self.service = IPInfo()
            result = self.service.check()
        except Exception:
            try:
                self.service = IfconfigMe()
                result = self.service.check()
            except Exception:
                try:
                    self.service = IfconfigCo()
                    result = self.service.check()
                except Exception:
                    try:
                        self.service = IPApi()
                        result = self.service.check()
                    except Exception:
                        result = None

        print(f"IP Checker Service name: {self.service.service_name}")

        if result is None:
            raise Exception("Can't find the current IP")

        return result

    def _ip(self, res: Response) -> str:
        """
        This extracts IP from the service
        """

    def _country(self, res: Response) -> str:
        """
        This extracts country code from the service
        """
