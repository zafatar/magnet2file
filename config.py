# config.py

import yaml


class BaseConfig(object):
    """
    Base configuration
    """
    DEBUG = True
    TESTING = False
    SEEDR_USERNAME = None
    SEEDR_PASSWORD = None
    SEEDR_API_URL = None
    VPN_USERNAME = None
    VPN_PASSWORD = None


class Local(BaseConfig):
    """
    Local Configuration
    """
    def load_config(self):
        self.DEBUG = True
        self.TESTING = False
        self.SEEDR_USERNAME = CONFIG['seedr']['username']
        self.SEEDR_PASSWORD = CONFIG['seedr']['password']
        self.SEEDR_API_URL = CONFIG['seedr']['api']['url']
        self.VPN_USERNAME = CONFIG['vpn']['username']
        self.VPN_PASSWORD = CONFIG['vpn']['password']


def app_config(env_name):
    """
    Configuration object by environment name

    :param env_name:
    :return:
    """
    global CONFIG
    CONFIG = load_config_from_yaml("config.yaml")

    config = Local()
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
