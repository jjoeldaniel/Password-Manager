import bcrypt
import psycopg2
import os
import urllib.parse as urlparse


def connect() -> psycopg2.connect:
    """
    Connect to PostgreSQL database
    """

    url = urlparse.urlparse(os.getenv("DB_URL"))
    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )


def validate_master_password(user_name, master_password) -> bool:
    """
    Returns True if the master password is correct
    """

    stored_hash = bytes(get_master_password(user_name)[0])
    return bcrypt.checkpw(master_password.encode('utf-8'), stored_hash)


def get_passwords(user_name, master_password) -> list:
    """
    Returns a list of passwords for the given user
    """

    if validate_master_password(
        user_name=user_name,
        master_password=master_password
    ):
        with connect() as conn:
            with conn.cursor() as cur:

                get_master_password = '''
                SELECT passwords FROM users WHERE user_name = %s
                '''

                cur.execute(get_master_password, (user_name,))
                return cur.fetchone()

    return None


def user_is_registered(user_name) -> bool:
    """
    Returns True if the user is registered
    """

    with connect() as conn:
        with conn.cursor() as cur:

            user_is_registered = '''
            SELECT EXISTS(
                SELECT 1
                FROM users
                WHERE user_name = %s
            )
            '''

            cur.execute(user_is_registered, (user_name,))
            return cur.fetchone()[0]


def get_master_password(user_name) -> bytes:
    """
    Return the master password for the given user
    """

    with connect() as conn:
        with conn.cursor() as cur:
            get_master_password = '''
            SELECT master_password
            FROM users
            WHERE user_name = %s
            '''

            cur.execute(get_master_password, (user_name,))
            return cur.fetchone()


def insert_password(user, password) -> None:
    """
    Insert a new password for the given user
    """

    with connect().cursor() as cur:

        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Append the new password to the array of passwords
        insert_password = '''
        UPDATE users
        SET passwords = array_append(passwords, %s)
        WHERE user_name = %s
        ON CONFLICT (user_name) DO NOTHING
        '''

        cur.execute(insert_password, (hashed_password, user))


def initialize_user(user_name, master_password) -> None:
    """
    Initialize a new user with a master password
    """

    with connect() as conn:
        with conn.cursor() as cur:

            # Hash the password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(
                master_password.encode('utf-8'),
                salt
            )

            insert_master_password = '''
            INSERT INTO users (user_name, master_password)
            VALUES (%s, %s)
            ON CONFLICT (user_name)
            DO NOTHING
            '''

            cur.execute(insert_master_password, (user_name, hashed_password))


def insert_master_password(user_name, master_password) -> None:
    """
    Insert a new master password for the given user
    """

    with connect() as conn:
        with conn.cursor() as cur:

            # Hash the password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(
                master_password.encode('utf-8'),
                salt
            )

            insert_master_password = '''
            INSERT INTO users (user_name, master_password)
            VALUES (%s, %s)
            ON CONFLICT (user_name)
            DO UPDATE SET master_password = %s
            '''

            cur.execute(
                insert_master_password, (
                    user_name,
                    hashed_password,
                    hashed_password
                )
            )


def initialize() -> None:
    """
    Initializes PostgreSQL database
    """

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
