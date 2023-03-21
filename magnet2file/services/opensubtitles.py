# -*- coding: utf-8 -*-
#
# services/Seedr.py
#
"""Seedr class and functions to interact with Seedr data
coming from its API.
"""
import sys
import requests

from magnet2file.services import Services, Service

class OpenSubtitles(Service): 
    """
    OpenSubtitles class
    """
    CODE = Services.OPENSUBTITLES

    def run(self) -> None:
        """
        Run instructions for the Seedr service
        """
        print("run opensubtiels...")


        