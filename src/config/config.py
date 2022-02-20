import configparser

from src.utils import Singleton


class Config(metaclass=Singleton):
    SIGNATURE_SECTION = "Signature"

    def __init__(self):
        self.config_data = None

    def load(self, filename: str):
        self.config_data = configparser.ConfigParser()
        self.config_data.read(filename)

    def signature_algo(self) -> str:
        return self.get_conf_value('signature_algo', 'md5')

    def signatures_dirs(self) -> str:
        return self.get_conf_value('signature_dirs', '')

    def encryption_type(self) -> str:
        return self.get_conf_value("encryption", 'aes')

    def get_conf_value(self, param: str, default: str) -> str:
        if Config.SIGNATURE_SECTION not in self.config_data:
            return default
        section = self.config_data[Config.SIGNATURE_SECTION]
        if str not in section:
            raise Exception(f"Signature.{param}  is absent in config")
        return section[param]

    @staticmethod
    def key_path() -> str:
        return "."

