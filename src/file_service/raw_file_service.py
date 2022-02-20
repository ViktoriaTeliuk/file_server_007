import os
from datetime import datetime
from typing import Tuple, Optional

from src.file_service import FileService
from src import utils


class RawFileService(FileService):

    def __init__(self, workdir):
        self.workdir = workdir

    def read(self, filename: str) -> str:
        """
        Reads file

        :param filename
        :return: content if file exist, None otherwise
        """
        if self.check_file(filename):
            with open(filename, "r") as f:
                return f.read()
        else:
            return None

    def write(self, content: str) -> str:
        """
        Creates file with unique name

        :param content of file
        :return: filename
        """
        filename = self.unique_file_name()
        return self.create_file_named(filename, content)

    def remove(self, filename: str):
        """
        Deletes file if exist

        :returns: True if file exist and was deleted
        """
        if self.check_file(filename):
            os.remove(filename)
            return True
        return False

    def ls(self) -> [str]:
        """
        Gets list of directories

        :return: list of directories
        """
        return os.listdir()

    def cd(self, dirname: str) -> bool:
        """
         Changes current directory

         :param directory - path to directory to go
         :returns True if dir exist, False otherwise
         """
        if self.check_dir(dirname):
            os.chdir(dirname)
            return True
        return False

    def read_metadata(self, filename: str) -> Tuple[str, str, int]:
        """
        Reads file creation date, edit date, file size

        :param filename: filename to read
        :return: tuple (create_date, modification_date, filesize)
        :raises Exception if file not found
        """
        if self.check_file(filename):
            status = os.stat(filename)
            cdate = datetime.datetime.fromtimestamp(status.st_ctime).strftime("%b %d %Y %H:%M:%S")
            mdate = datetime.datetime.fromtimestamp(status.st_mtime).strftime("%b %d %Y %H:%M:%S")
            return cdate, mdate, status.st_size
        else:
            raise OSError(f"file {filename} is not exist")

    def unique_file_name(self):
        """
        Creates unique file name

        :return: file name
        """
        while True:
            filename = utils.random_string(10)
            if not os.path.exists(filename):
                return filename

    def create_file_named(self, filename: str, content: str) -> str:
        with open(filename, "w") as f:
            f.write(content)
        return filename

    def check_file(self, filename: str) -> bool:
        """
        Checks if file exist

        :param filename full file name with path
        :returns: True if file exist False otherwise
        """
        return os.path.isfile(filename)

    def check_dir(self, directory: str) -> bool:
        """
        Checks if directory exist

        :param directory path to directory to check
        :returns: True if directory exists
        """
        return os.path.isdir(directory)

    def get_file_permissions(self, filename: str) -> Optional[str]:
        """
        Gets file permissions in hex

        :param filename name of file
        :returns: hex number
        """
        if self.check_file(filename):
            return hex(os.stat(filename).st_mode)
        else:
            return None

    def set_file_permissions(self, filename: str, permissions: str):
        """
        Sets file permissions

        :param filename name of file
        :param permissions hex number
        :returns: True if permissions set
        """
        if self.check_file(filename):
            os.chmod(filename, int(permissions, 16))
            return True
        else:
            return False

    async def async_write(self, content: str) -> str:
        return self.write(content.encode())




