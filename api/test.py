import bcrypt
import db
import unittest
from dotenv import load_dotenv


class TestPasswordMethods(unittest.TestCase):

    load_dotenv()
    db.initialize()

    # Test input
    global username
    username = "kyle"

    global password
    password = "hunter1234"

    # Store the hashed password and retrieve it
    db.insert_master_password(username, password)
    global stored_hash
    stored_hash = bytes(db.get_master_password(username)[0])

    # Verify initializations pass
    def test_init(self):
        self.assertNoLogs(db.initialize())

    # Verify the entered password against the stored hash
    def test_password(self):
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), stored_hash))

    # Verify user actions
    def test_user(self):
        self.assertTrue(db.user_is_registered(username))
        self.assertIsNotNone(db.get_passwords(username, password))


if __name__ == '__main__':
    unittest.main()
