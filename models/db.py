# db.py
import psycopg2
from psycopg2 import pool
import psycopg2.extras
from config import DATABASE_URL


try:
    db_pool = psycopg2.pool.ThreadedConnectionPool(1, 20, DATABASE_URL)
except Exception as e:
    print("Error creating connection pool:", e)

def get_connection():
    return db_pool.getconn()

def release_connection(conn):
    if db_pool:
        db_pool.putconn(conn)

def get_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)