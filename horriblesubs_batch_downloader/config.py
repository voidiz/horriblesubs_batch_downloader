import appdirs
import configparser
import os
import subprocess
import sys


class Config:
    _app_name = "horriblesubs_batch_downloader"
    _config_dir = appdirs.user_config_dir(_app_name)
    _config_file_name = "hsbd.conf"
    _config_path = os.path.join(_config_dir, _config_file_name)

    def __init__(self):
        self.rd_api_token = ""

        self.parse_config_file()

    def get_rd_api_token(self):
        if not self.rd_api_token:
            print("No RealDebrid API token stored")
            self.set_rd_api_token()

        return self.rd_api_token

    def set_rd_api_token(self):
        token = input("Paste API token: ")

        if not token:
            raise ValueError("No API token supplied")

        parser = configparser.ConfigParser()
        parser.read(self._config_path)
        parser["RealDebrid"]["api_token"] = token

        with open(self._config_path, "w") as f:
            parser.write(f)

    def parse_config_file(self):
        """
        Parse the config file stored in the default location.
        """

        if not os.path.isfile(self._config_path):
            self.create_config_file()

        parser = configparser.ConfigParser()
        parser.read(self._config_path)

        self.rd_api_token = parser["RealDebrid"]["api_token"]

    def create_config_file(self):
        """
        Create the configuration file.
        """

        config = configparser.ConfigParser()

        config["RealDebrid"] = {}
        config["RealDebrid"]["api_token"] = ""

        os.makedirs(self._config_dir, exist_ok=True)
        with open(self._config_path, "w") as f:
            config.write(f)
