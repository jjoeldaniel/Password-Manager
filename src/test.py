import bcrypt
import db
from dotenv import load_dotenv

load_dotenv()
db.initialize()

# Test input
username = "kyle"
password = "hunter1234"

# Hash the password
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

# Store the hashed password and retrieve it
db.insert_master_password(username, hashed_password)
stored_hash = bytes(db.get_master_password(username)[0])

# Verify the entered password against the stored hash
if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
    print("It Matches!")
else:
    print("Incorrect password")
