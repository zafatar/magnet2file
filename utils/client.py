# src/utils/client.py

import requests
import config


class Client:
    """
    Generic
    """
    @staticmethod
    def http_headers(content_type=None, auth_required=False):
        headers = {}
        if content_type is not None:
            headers['content-type'] = content_type

        if auth_required:
            headers['Authorization'] = Client.auth_header()

        return headers

    @staticmethod
    def basic_headers():
        return Client.http_headers(auth_required=False, content_type="application/json")

    @staticmethod
    def auth_header():
        # TODO: To be improved.
        return config.CONFIG['database']['auth_prefix'] + " " + config.CONFIG['database']['auth_token']