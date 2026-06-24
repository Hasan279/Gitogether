import bcrypt

# Change these to your desired admin credentials
email = "admin@example.com"
password = "secure_password123"

# Encrypt the password exactly how the app does
password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Generate the SQL query
sql_query = f"""
-- SQL Query to insert a new admin user
INSERT INTO Users (email, password_hash, role)
VALUES ('{email}', '{password_hashed}', 'admin');
"""

print(sql_query)
