# -*- coding: utf-8 -*-
"""Library for the http client
"""


class Client:
    """
    Simple HTTP Client (WIP)
    """
    @staticmethod
    def http_headers(content_type=None, auth_required=False):
        headers = {}
        if content_type is not None:
            headers['content-type'] = content_type

        if auth_required:
            headers['Authorization'] = None

        return headers

    @staticmethod
    def basic_headers():
        return Client.http_headers(auth_required=False,
                                   content_type="application/json")
