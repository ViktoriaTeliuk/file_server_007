from aiohttp import web

from src.config import Config
from src.crypto.encryption import Encryption
from src.file_service import RawFileService
# from src.file_service.signed_file_service import SignedFileService
import json


def auth_need(func):
    async def wrapper(self, request, *args, **keyargs):
        # user_service = self.user_service
        uuid = request.headers.get("Authorization")
        print("CHECK auth")
        if not self.user_service.is_authorized(uuid):
            return web.Response(status=401, text='Not authorized')
        return await func(self, request, *args, **keyargs)
        # RESPONSE 401 - Not authorized
    return wrapper


class Handler:

    def __init__(self, user_service):
        self.user_service = user_service
        raw_file_service = RawFileService(".")
        self.fs = raw_file_service
#        if Config.encrypted():
#            self.fs = Encryption.get_default_encryptor()
#        else:
#            self.fs = SignedFileService(self.fs)

    @auth_need
    async def ls(self, request, *args, **keyargs):
        try:
            print(self.fs)
            dir_listing = self.fs.ls()
            return web.Response(text="\n".join(dir_listing))
        except Exception as ex:
            print(ex)

    @auth_need
    async def cd(self, request, *args, **keyargs):
        try:
            directory = request.query['dir']
            cd = self.fs.cd(directory)
            return web.Response(text=str(directory))
        except Exception as ex:
            print(ex)

    @auth_need
    async def pwd(self, request, *args, **keyargs):
        try:
            return web.Response(text=json.dumps(self.fs.workdir))
        except Exception as ex:
            print(ex)

    @auth_need
    async def rm(self, request, *args, **keyargs):
        try:
            filename = request.query['filename']
            cdate, mdate, st_size = self.fs.read_metadata(filename)
            return web.Response(text=str(f"created: {cdate} modified: {mdate} size: {st_size}"))
        except Exception as ex:
            print(ex)

    @auth_need
    async def read(self, request, *args, **keyargs):
        try:
            filename = request.query['filename']

            content = self.fs.read(filename)
            response = {
                "content": content
            }
            return web.Response(text=json.dumps(response))

        except Exception as ex:
            print(ex)

    @auth_need
    async def write(self, request, *args, **keyargs):
        data = b''
        while not request.content.at_eof(): #body  request.query - параметры чз запятую
            data += await request.content.read()
        filename = self.fs.async_write(data)
        response = {
            "filename" : filename
        }
        return web.Response(text=json.dumps(response))

    async def signup(self, request: web.Request, *args, **keyargs) -> web.Response:
        # POST
        # get username\passwd from body, ask user service to signup
        # respond with result of user service
        data = b''
        # print(request.query)
        while not request.content.at_eof():
            data += await request.content.read()
        data = data.decode()
        data = json.loads(data)

        self.user_service.add_user(data["username"], data["passwd"])
        return web.Response(status=200, text="Registration success")

    async def login(self, request: web.Request, *args, **keyargs):
        data = b''

        while not request.content.at_eof():
            data += await request.content.read()

        data = json.loads(data.decode())

        user_uuid = self.user_service.add_session(data["username"], data["passwd"])
        response = web.Response(status=200, text="Auth success", headers={"Authorization": user_uuid})
        return response

    async def logout(self, request: web.Request, *args, **keyargs):
        # get uuid from body, ask user service to delete session
        # respond result of user service
        user_uuid = request.headers.get("Authorization")
#        data = b''
#        print(request.query)
#        while not request.content.at_eof():
#            data += await request.content.read()
        self.user_service.logout(user_uuid)
        response = web.Response(status=200, text="Logout successful", headers={"uuid": user_uuid})
        return response


def create_web_app(user_service):
    app = web.Application()
    handler = Handler(user_service)
    app.add_routes([
        web.get('/ls', handler.ls),
        web.put('/cd', handler.cd),
        web.get('/pwd', handler.pwd),
        web.get('/rm', handler.rm),
        web.get('/read', handler.read),
        web.get('/write', handler.write),
        web.post('/users/signup', handler.signup),
        web.post('/users/login', handler.login),
        web.post('/users/logout', handler.logout)
    ])
    return app
