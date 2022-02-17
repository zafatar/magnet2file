# -*- coding: utf-8 -*-

from magnet2file.services import Services
from magnet2file.services.Seedr import Seedr
from magnet2file.services.ShowRSS import ShowRSS
from magnet2file.services.Yify import Yify


class ServiceFactory:

    @staticmethod
    def get_service(service_code, config):
        service = None

        # dependency for the Yify and ShowRSS
        seedr_service = Seedr({
            'email': config.SEEDR_USERNAME,
            'password': config.SEEDR_PASSWORD
        })

        if service_code == Services.YIFY:
            service = Yify(seedr_service)
        elif service_code == Services.SHOWRSS:
            service = ShowRSS(seedr_service)
        elif service_code == Services.SEEDR:
            service = seedr_service
        else:
            raise f"Unsupported service: {service_code}"

        return service
