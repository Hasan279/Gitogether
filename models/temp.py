import bcrypt

password = "systemadmin"
password_hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

print(password_hashed)