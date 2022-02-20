from datetime import timedelta, datetime

from psycopg2 import sql
import uuid


class UserService:
    def __init__(self, db):
        self.db = db

    def add_user(self, username, passwd):
        cursor = self.db.cursor()
        request = sql.SQL(f'''INSERT INTO public.users (user_name, passwd)
                             VALUES ('{username}', '{passwd}')''')
        cursor.execute(request)
        self.db.commit()

    def add_session(self, username, passwd) -> str:
        # check if user exist and password matched
        # create session for user, add to db
        # return session uuid
        cursor = self.db.cursor()
        request = sql.SQL(f'''SELECT user_id FROM public.users WHERE user_name = '{username}' and passwd = '{passwd}' ''')
        cursor.execute(request)
        user_id = cursor.fetchall()
        if user_id is None:
            raise Exception(f"user name or password are not exist {username}")

        generated_uuid = uuid.uuid4()
        expiration = datetime.now() + timedelta(days=1)
        request = sql.SQL(f'''INSERT INTO public.sessions (user_id, uuid, expiration_date)
                             VALUES ('{user_id[0][0]}', '{generated_uuid}', '{expiration}')''')
        cursor.execute(request)
        self.db.commit()

        return generated_uuid.__str__()

    def is_authorized(self, user_uuid) -> bool:
        cursor = self.db.cursor()
        request = sql.SQL(f'''SELECT expiration_date FROM public.sessions WHERE UUID = '{user_uuid}' ''')
        cursor.execute(request)
        response = cursor.fetchall()

        return datetime.now() <= response[0][0]

    def logout(self, user_uuid):
        # remove session with uuid
        cursor = self.db.cursor()
        request = sql.SQL(f'''DELETE FROM public.sessions where uuid = '{user_uuid}' ''')
        cursor.execute(request)
        self.db.commit()


'''
-- Table: public.users

DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    user_id serial,
    passwd character varying COLLATE pg_catalog."default",
    user_name character varying COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;


    
-- Table: public.sessions

DROP TABLE IF EXISTS public.sessions;

CREATE TABLE IF NOT EXISTS public.sessions
(
    user_id integer,
    uuid uuid,
    expiration_date TIMESTAMP without time zone,
	CONSTRAINT sessions_pkey PRIMARY KEY (uuid)
)
TABLESPACE pg_default;

CREATE INDEX index_name ON public.sessions(user_id);

ALTER TABLE IF EXISTS public.sessions
    OWNER to postgres;    
'''