# -*- coding: utf-8 -*-
"""Config class contains the set of configuration values
read from a YAML file and stored into a dict.
"""
import os
import yaml


class Config:
    """
    Base configuration class
    """
    DEBUG = True
    TESTING = False
    IPCHECKER_SERVICE = None
    SEEDR_USERNAME = None
    SEEDR_PASSWORD = None
    SEEDR_API_URL = None
    VPN_USERNAME = None
    VPN_PASSWORD = None

    def load_config(self, config: dict = None):
        """load the config values from the global variable
        into the Config class attributes.
        """
        self.DEBUG = True
        self.TESTING = False
        self.IPCHECKER_SERVICE = config['ipchecker_service']
        self.SEEDR_USERNAME = config['seedr']['username']
        self.SEEDR_PASSWORD = config['seedr']['password']
        self.SEEDR_API_URL = config['seedr']['api']['url']
        self.VPN_USERNAME = config['vpn']['username']
        self.VPN_PASSWORD = config['vpn']['password']

    def __repr__(self) -> str:
        return f"<Config: debug: {self.DEBUG}, testing: {self.TESTING}>"


def get_config():
    """
    Configuration object by environment name

    :return: config object
    """
    config_from_yaml = load_config_from_yaml("config.yaml")

    config_dir_path = os.path.dirname(os.path.realpath(__file__))
    config = load_config_from_yaml(config_dir_path + "/config.yaml")

    config = Config()
    config.load_config(config=config_from_yaml)

    return config


def load_config_from_yaml(config_file_path: str = None):
    """Load configuration from a YAML file
    by reading it.

    Args:
        config_file_path (str): file path of config file

    Returns:
        dict: config as dictionary
    """
    config = read_config(config_file_path)
    return config


def read_config(config_file_path):
    """Read configuration from any place, for now only
    from YAML file.

    Args:
        config_file_path (str): file path of config file

    Returns:
        dict: config as dictionary
    """
    config = None
    with open(config_file_path, 'rb') as config_file:
        try:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as err:
            print(err)

    return config
