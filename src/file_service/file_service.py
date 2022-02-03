import os
from file_server_007.src import utils


def unique_file_name():
    return utils.random_string(10)


def create_file(content):
    filename = unique_file_name()
    while os.path.exists(filename):
        filename = unique_file_name()
    with open(filename, "w") as f:
        f.write(content)
    return filename


def delete_file(filename):
    os.remove(filename)


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def lsdir():
    return os.listdir()


def change_dir(directory):
    os.chdir(directory)


def check_file(filename):
    return os.path.exists(filename) and os.path.isfile(filename)


def check_dir(directory):
    return os.path.exists(directory) and os.path.isdir(directory)


def get_file_permissions(filename):
    return oct(os.stat(filename).st_mode)


def set_file_permissions(filename, permissions):
    os.chmod(filename, int(permissions, 16))
