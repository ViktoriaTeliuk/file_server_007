import datetime
import os
from typing import Optional, Tuple
from src import utils
from src.crypto.signature import SignatureFactory

from abc import ABCMeta, abstractmethod


class FileService(metaclass=ABCMeta):

    @abstractmethod
    def read(self, filename: str) -> str: raise Exception("not implemented")

    @abstractmethod
    def write(self, filename: str) -> str: raise Exception("not implemented")

    @abstractmethod
    def remove(self, filename: str): raise Exception("not implemented")

    @abstractmethod
    def ls(self) -> [str]: raise Exception("not implemented")

    @abstractmethod
    def cd(self, dirname: str) -> None: raise Exception("not implemented")

    @abstractmethod
    def read_metadata(self, filename: str) -> Tuple[str, str, int]: raise Exception("not implemented")

    @abstractmethod
    async def async_write(self, content: str) -> str:
        raise NotImplemented

