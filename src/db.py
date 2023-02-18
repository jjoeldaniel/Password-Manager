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
