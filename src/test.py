import bcrypt

password = "hunter1234"
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
    print("It Matches!")
else:
    print("FUCK")
