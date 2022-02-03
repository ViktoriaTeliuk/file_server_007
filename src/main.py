#! c:\Users\Viktoria\AppData\Local\Programs\Python\Python310\python.exe
import argparse
import os
import file_service


def read_file():
    filename = input("Enter file name to read: ")
    print(f"read file : {filename}")
    if file_service.check_file(filename):
        print(file_service.read_file(filename))
    else:
        print(f"file is not exist : {filename}")


def create_file():
    content = input("Enter file content : ")
    print(f"created file : {file_service.create_file(content)}")


def delete_file():
    filename = input("Enter file name to delete: ")
    if file_service.check_file(filename):
        file_service.delete_file(filename)
    else:
        print(f"file is not exist : {filename}")
    print(f"deleted file : {filename}")


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
        print(f"directory is not exist : {directory}")


def get_file_permissions():
    # Read file UNIX permissions
    filename = input("Enter file name to get permissions: ")
    if file_service.check_file(filename):
        print(f"file permissions : {file_service.get_file_permissions(filename)}")
    else:
        print(f"file is not exist : {filename}")


def set_file_permissions():
    filename = input("Enter file name to set permissions: ")
    if file_service.check_file(filename):
        permissions = input("Input UNIX permissions in oct format :")
        file_service.set_file_permissions(filename, permissions)
        print(f"Set {permissions} to {filename}")
    else:
        print(f"file is not exist : {filename}")


def main():
    commands = {
        "get": read_file,
        "create": create_file,
        "delete": delete_file,
        "ls": list_dir,
        "cd": change_dir,
        "read_perm": get_file_permissions,
        "set_perm": set_file_permissions
    }
    parser = argparse.ArgumentParser(description='Restful file server')
    parser.add_argument('-d', '--directory', dest="path", help='Root directory of file server', default="d:/temp/")
    args = parser.parse_args()
    os.chdir(args.path)

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


if __name__ == "__main__":
    main()
