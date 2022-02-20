#! c:\Users\Viktoria\AppData\Local\Programs\Python\Python310\python.exe
import argparse
import logging
import logging.config
import os

import yaml
from aiohttp import web

from src import file_service

import psycopg2
from src.config import Config
# from src.file_service.encrypted_file_service import EncryptedFileService
from src.http_server import create_web_app
from src.user_service import UserService


def read_file():
    filename = input("Enter file name to read: ")
    logging.info(f"read file : {filename}")
    if file_service.check_file(filename):
        print(file_service.read_file(filename))
    else:
        logging.error(f"file is not exist : {filename}")


def create_file():
    content = input("Enter file content : ")
    logging.info(f"created file : {file_service.create_file(content)}")


def delete_file():
    filename = input("Enter file name to delete: ")
    if file_service.check_file(filename):
        file_service.delete_file(filename)
    else:
        logging.error(f"file is not exist : {filename}")
    logging.info(f"deleted file : {filename}")


def list_dir():
    print(f"list dir")
    for d in file_service.lsdir():
        print(d)


def change_dir():
    directory = input("Enter dir name : ")
    if file_service.check_dir(directory):
        file_service.change_dir(directory)
        print(f"change dir : {directory}")
    else:
        logging.error(f"directory is not exist : {directory}")


def get_file_permissions():
    # Read file UNIX permissions
    filename = input("Enter file name to get permissions: ")
    if file_service.check_file(filename):
        logging.info(f"file permissions : {file_service.get_file_permissions(filename)}")
    else:
        logging.error(f"file is not exist : {filename}")


def set_file_permissions():
    filename = input("Enter file name to set permissions: ")
    if file_service.check_file(filename):
        permissions = input("Input UNIX permissions in oct format :")
        file_service.set_file_permissions(filename, permissions)
        logging.info(f"Set {permissions} to {filename}")
    else:
        logging.error(f"file is not exist : {filename}")


def get_file_metadata():
    filename = input("Enter file name to get metadata: ")
    if file_service.check_file(filename):
        print(file_service.get_file_meta_data(filename))
    else:
        logging.error(f"file is not exist : {filename}")


def create_signed():
    content = input("Input file content:")
    print(file_service.create_signed_file(content, Config.signature_algo()))


def read_signed():
    filename = input("Enter filename to read:")
    print(file_service.read_signed_file(filename))


def read_encrypted():
    filename = input('Enter file name: ')
    try:
        data = EncryptedFileService(file_service).read(filename)
        print(f"Reading file: {filename}")
        print(data)
    except Exception as e:
        print(e)


def create_encrypted():
    content = input("Enter content of file:")
    filename = EncryptedFileService(file_service).write(content)
    print(f"File {filename} created")


def main_():
    with open(file="./log_config.yaml", mode='r') as file:
        logging_yaml = yaml.load(stream=file, Loader=yaml.FullLoader)
        logging.config.dictConfig(config=logging_yaml)
    logging.getLogger("telemetry").info("start")

    commands = {
        "get": read_file,
        "create": create_file,
        "delete": delete_file,
        "ls": list_dir,
        "cd": change_dir,
        "read_perm": get_file_permissions,
        "set_perm": set_file_permissions,
        "metadata": get_file_metadata,
        "create_signed": create_signed,
        "read_signed": read_signed,
        "read_encrypted": read_encrypted,
        "create_encrypted": create_encrypted
    }
    parser = argparse.ArgumentParser(description='Restful file server')
    parser.add_argument('-d', '--directory', dest="path", help='Root directory of file server', default="d:/vika/tmp")
    parser.add_argument('-c', '--config', dest="conf", help='Config name', default="config")
    args = parser.parse_args()
    os.chdir(args.path)

    Config.load(args.conf)

    while True:
        command = input()
        if command == "exit":
            return
        if command not in commands:
            print("Unknown command")
            continue
        try:
            commands[command]()
        except Exception as ex:
            print(f"Error on {command} execution : {ex}")

    logging.getLogger("telemetry").info("end")


def main():
    conn = psycopg2.connect(dbname='007db', user='postgres', password='postgres', host='127.0.0.1', port='5433')
    user_service = UserService(conn)

    app = create_web_app(user_service)
    web.run_app(app)


if __name__ == "__main__":
    main()
