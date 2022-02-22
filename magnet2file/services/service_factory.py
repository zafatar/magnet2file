# -*- coding: utf-8 -*-
"""This is the service factory modules containing
ServiceFactory class which generates and returns
the selected service.
"""
from magnet2file.services import Services
from magnet2file.services.seedr import Seedr
from magnet2file.services.showrss import ShowRSS
from magnet2file.services.yify import Yify


class ServiceFactory:
    """ServiceFactory class which
    decides which service will be called and return
    based on the given service code and config.
    """
    @staticmethod
    def get_service(service_code, config):
        """Service build method

        This method returns the service based on the given
        service code and the application config.

        Args:
            service_code (enum): service enum value.
            config (dict): application config as dict.

        Raises:
            f: Unsupported service error in case of not-defined service code.

        Returns:
            Service: service instance.
        """
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

    def __repr__(self) -> str:
        return f"<{__class__}>"
