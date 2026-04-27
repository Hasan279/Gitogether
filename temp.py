import subprocess
import sys

packages = [
    "flask",
    "psycopg2-binary",
    "python-dotenv",
    "flask-bcrypt"
]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for package in packages:
    install(package)

print("All packages installed successfully!")