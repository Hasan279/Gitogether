import psycopg2
import psycopg2.extras
from config import DATABASE_URL

def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def get_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)