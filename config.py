# config.py

import os
import yaml


class BaseConfig(object):
    """
    Base configuration
    """
    DEBUG = True
    TESTING = False
    IPCHECKER_SERVICE = None
    SEEDR_USERNAME = None
    SEEDR_PASSWORD = None
    SEEDR_API_URL = None
    VPN_USERNAME = None
    VPN_PASSWORD = None

    def load_config(self):
        self.DEBUG = True
        self.TESTING = False
        self.IPCHECKER_SERVICE = CONFIG['ipchecker_service']
        self.SEEDR_USERNAME = CONFIG['seedr']['username']
        self.SEEDR_PASSWORD = CONFIG['seedr']['password']
        self.SEEDR_API_URL = CONFIG['seedr']['api']['url']
        self.VPN_USERNAME = CONFIG['vpn']['username']
        self.VPN_PASSWORD = CONFIG['vpn']['password']


def get_config():
    """
    Configuration object by environment name

    :return: config object
    """
    global CONFIG
    CONFIG = load_config_from_yaml("config.yaml")

    config_dir_path = os.path.dirname(os.path.realpath(__file__))
    CONFIG = load_config_from_yaml(config_dir_path + "/config.yaml")

    config = BaseConfig()
    config.load_config()

    return config


def load_config_from_yaml(config_file_path):
    config = read_config(config_file_path)
    return config


def read_config(config_file_path):
    config = None
    with open(config_file_path, 'rb') as f:
        try:
            config = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as err:
            print(err)

    return config
