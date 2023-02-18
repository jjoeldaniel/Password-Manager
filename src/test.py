import bcrypt
import db
from dotenv import load_dotenv

load_dotenv()
db.initialize()

username = "kyle"
password = "hunter1234"

salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

print(hashed_password)
db.insert_master_password(username, hashed_password)

new_pw = bytes(db.get_master_password(username)[0])
salt = new_pw[:29]

# Verify the entered password against the stored hash and salt values
if bcrypt.checkpw(password.encode('utf-8'), new_pw):
    print("It Matches!")
else:
    print("Incorrect password")
