from configparser import ConfigParser
from typing import Union


class Configurator:
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read("config.ini")

    def get_param(self, section: str, key: str) -> Union[int, str]:
        """
        Returns value in config.ini.example
        :param section: A section of config
        :param key: A key
        """
        return self.parser[section][key]
