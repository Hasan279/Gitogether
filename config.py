import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Neon / Heroku-style URLs use postgres://; psycopg2 expects postgresql://
_raw_db = os.getenv("DATABASE_URL")
if _raw_db and _raw_db.startswith("postgres://"):
    DATABASE_URL = _raw_db.replace("postgres://", "postgresql://", 1)
else:
    DATABASE_URL = _raw_db
SECRET_KEY = os.getenv("SECRET_KEY")


CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

DEBUG = os.getenv("DEBUG", "False") == "True"