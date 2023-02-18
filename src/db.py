import psycopg2
import os
import urllib.parse as urlparse


def connect():
    url = urlparse.urlparse(os.getenv("DB_URL"))
    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )


def get_master_password(user_name):
    with connect() as conn:
        with conn.cursor() as cur:
            get_master_password = '''
            SELECT master_password FROM users WHERE user_name = %s
            '''

            cur.execute(get_master_password, (user_name,))
            return cur.fetchone()


def insert_password(user, hashed_password):
    with connect().cursor as cur:

        # Append the new password to the array of passwords
        insert_password = '''
        UPDATE users SET passwords = array_append(passwords, %s) WHERE user_name = %s
        ON CONFLICT (user_name) DO NOTHING
        '''

        cur.execute(insert_password, (hashed_password, user))


def initialize_user(user_name, master_password):
    with connect() as conn:
        with conn.cursor() as cur:
            insert_master_password = '''
            INSERT INTO users (user_name, master_password) VALUES (%s, %s)
            ON CONFLICT (user_name) DO NOTHING
            '''

            cur.execute(insert_master_password, (user_name, master_password))


def insert_master_password(user_name, master_password):
    with connect() as conn:
        with conn.cursor() as cur:
            insert_master_password = '''
            INSERT INTO users (user_name, master_password) VALUES (%s, %s)
            ON CONFLICT (user_name) DO UPDATE SET master_password = %s
            '''

            cur.execute(insert_master_password, (user_name, master_password, master_password))


def initialize():
    with connect() as conn:
        with conn.cursor() as cur:
            initialize_db = '''
            CREATE TABLE IF NOT EXISTS users(
                user_name text PRIMARY KEY NOT NULL,
                master_password bytea NOT NULL,
                passwords bytea[]
            )
            '''

            cur.execute(initialize_db)
