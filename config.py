import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("postgresql://postgres:Jtt$.S4hhEDhnG2@db.hobwhojtlwfahzwhtckf.supabase.co:5432/postgres")
SECRET_KEY = os.getenv("43cae493238383fe75e23450ceeca0d569fa37fb12833895cf98ea254591e17d")
DEBUG = os.getenv("DEBUG", "False") == "True"