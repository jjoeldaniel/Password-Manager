import psycopg2
import os
from dotenv import load_dotenv
import urllib.parse as urlparse

load_dotenv()


def connect():
    url = urlparse.urlparse(os.getenv("DB_URL"))
    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )


def insert_password(password):
    with connect().cursor as cur:
        insert_password = f'''
        INSERT INTO users (passwords) VALUES ({password})
        '''

        cur.execute(insert_password, (password,))
        cur.commit()


def insert_master_password(master_password):
    with connect().cursor as cur:
        insert_master_password = f'''
        INSERT INTO users (master_password) VALUES ({master_password})
        '''

        cur.execute(insert_master_password, (master_password,))
        cur.commit()


def initialize():
    with connect().cursor as cur:

        initialize_db = '''
        CREATE TABLE IF NOT EXISTS users(
            master_password text PRIMARY KEY,
            passwords text[]
        )
        '''

        cur.execute(initialize_db)
        cur.commit()
