# -*- coding: utf-8 -*-
"""Library for the http client
"""


class Client:
    """
    Simple HTTP Client (WIP)
    """
    @staticmethod
    def http_headers(content_type: str = None,
                     auth_required: bool = False) -> dict:
        """Build http headers for the client

        Args:
            content_type (str, optional): content type in of the request.
                Defaults to None.
            auth_required (bool, optional): Authorization included or not.
                Defaults to False.

        Returns:
            dict: basic headers as dict
        """
        headers = {}
        if content_type is not None:
            headers['content-type'] = content_type

        if auth_required:
            headers['Authorization'] = None

        return headers

    @staticmethod
    def basic_headers() -> dict:
        """Generate basic headers with no Auth for json content.

        Returns:
            dict: basic headers as dict
        """
        return Client.http_headers(auth_required=False,
                                   content_type="application/json")
