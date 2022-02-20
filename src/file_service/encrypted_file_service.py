import os
from typing import Tuple

import file_service

from src.config import Config
from src.crypto.encryption import Encryption


class EncryptedFileService(file_service.FileService):

    def __init__(self, wrapped_file_service: file_service.FileService):
        self.wrapped_file_service = wrapped_file_service

    def read(self, filename: str) -> str:
        encryptor = self.find_encryptor_for_file(filename)
        key_file_name = encryptor.key_file_name(filename)
        with open(key_file_name) as f:
            key = f.read()
        encrypted_data = self.wrapped_file_service.read(filename)
        decrypted_data = encryptor.decrypt(encrypted_data, key)
        return decrypted_data

    def write(self, data: str) -> str:
        encryptor = Encryption.get_default_encryptor()
        encrypted_data, key = encryptor.encrypt(data)
        filename = self.wrapped_file_service.write(encrypted_data)
        key_file_name = encryptor.key_file_name(filename)
        with open(key_file_name) as f:
            f.write(key)
        return filename

    def remove(self, filename: str) -> None:
        self.wrapped_file_service.remove(filename)
        encryptor = self.find_encryptor_for_file(filename)
        key_file_name = encryptor.key_file_name(filename)
        os.remove(key_file_name)

    def ls(self) -> [str]:
        return self.wrapped_file_service.ls()

    def cd(self, dir: str) -> None:
        return self.wrapped_file_service.cd(dir)

    def read_metadata(self, filename: str) -> Tuple[str, str, int]:
        return self.wrapped_file_service.read_metadata(filename)

    @staticmethod
    def find_encryptor_for_file(filename):
        # find all keys for filename
        for key_file in os.listdir(Config.key_path()):
            if key_file.startswith(filename):
                return Encryption.get_encryptor_for_key_file(key_file)
        # find encryptor for key

    async def async_write(self, content: str) -> str:
        return self.write(content.encode())

