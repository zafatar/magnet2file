# -*- coding: utf-8 -*-

import enum

from utils.ipchecker.services.ifconfigme import IfconfigMe
from utils.ipchecker.services.ipinfo import IPInfo
from utils.ipchecker.services.ipapi import IPApi

VERSION = '0.0.1'


class Services(enum.Enum):
    IPINFO = 'ipinfo.io'
    IPAPI = 'ip-api.com'
    IFCONFIG = 'ifconfig.me'


class IPChecker():

    def __init__(self, service: str = None):
        self.service = service

    def check(self) -> bool:
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
