import os
from abc import ABCMeta, abstractmethod
from random import Random
from typing import Tuple

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from src.utils import random_string
from src.config import Config


class Encryption(metaclass=ABCMeta):
    encryptors = []

    def __init__(self, label):
        self.encryptors.append(self)

    @abstractmethod
    def encrypt(self, data) -> Tuple[str, str]:
        """
       Encrypts data,
       generates new key for each data
       :param data: data to encrypt
       :return: encrypted data and key to decrypt it
       """
        raise NotImplemented()

    @abstractmethod
    def decrypt(self, encrypted_data: str, key: str) -> str:
        """
       Decrypts data with provided key
       :param encrypted_data: data to decrypt
       :param key: decryption key
       :return: decrypted data
       """
        raise NotImplemented()

    @abstractmethod
    def key_file_name(self, filename: str) -> str:
        raise NotImplemented()

    @abstractmethod
    def key_file_match(self, key_file) -> bool:
        raise NotImplemented()

    @abstractmethod
    def key_file_ext(self) -> str:
        raise NotImplemented

    @staticmethod
    def get_encryptor_for_key_file(key_file):
        for encryptor in Encryption.encryptors:
            if encryptor.key_file_match(key_file):
                return encryptor
            else:
                return None

    @staticmethod
    def get_default_encryptor():
        return Encryption.get_encryptor_for_key_file(Config.encryption_type())


class SymetricEncryption(Encryption):

    def encrypt(self, data) -> Tuple[str, str]:
        session_key = random_string(10).encode()
        aes = AES.new(session_key, AES.MODE_AEX)
        encrypted_data, tag = aes.encrypt_and_digest(data.encode())
        # tag - контрольная сумма
        # nonce - случайное однократное значение которое добавляется в шифрование
        return [encrypted_data, f"{session_key},{tag},{aes.nonce}"]

    def decrypt(self, encrypted_data: str, key: str) -> str:
        session_key, tag, nonce = key.split(",")
        aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = aes.decrypt_and_verivy(encrypted_data, tag)
        return data

    def key_file_name(self, filename: str) -> str:
        return os.path.join(filename, self.key_file_ext())

    def key_file_match(self, key_file) -> bool:
        return key_file.endswith("." + self.key_file_ext())

    def key_file_ext(self) -> str:
        return "aes"


class HybrydEncryption(Encryption):

    def __init__(self):
        self.symetric_enctyption = SymetricEncryption()
        keys_path = Config.keys_path()
        keys_path = os.path.join(keys_path, "key.pem")
        if os.path.exists(keys_path):
            self.rsa_key = RSA.import_key(open(keys_path).read())
        else:
            random_generator = Random.new().read
            self.rsa_key = RSA.generate(1024, random_generator)  # generate public and private keys
            open(keys_path).write(self.rsa_key.export_key('PEM'))

    def encrypt(self, data) -> Tuple[str, str]:
        encrypted_data, symetric_key = self.symetric_encription.encrypt(data)
        encrypted_key = self.rsa_key.publickey.encrypt(symetric_key, 32)
        return encrypted_data, encrypted_key

    def decrypt(self, encrypted_data: str, encrypted_key: str) -> str:
        symetric_key = self.rsa_key.decrypt(encrypted_key.encode())
        data = self.symetric_enctyption.decrypt(encrypted_data, symetric_key.decode())
        return data

    def key_file_match(self, key_file):
        return key_file.endswith("." + self.key_file_ext())

    def key_file_ext(self):
        return "hybryd"
