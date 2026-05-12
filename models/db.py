# db.py
import os

import psycopg2
from psycopg2 import pool
import psycopg2.extras
from config import DATABASE_URL

# On Vercel each instance is short-lived; keep the pool small to avoid exhausting DB connections.
_max_conn = 2 if os.environ.get("VERCEL") == "1" else 20

try:
    db_pool = (
        psycopg2.pool.ThreadedConnectionPool(1, _max_conn, DATABASE_URL)
        if DATABASE_URL
        else None
    )
except Exception as e:
    print("Error creating connection pool:", e)
    db_pool = None

def get_connection():
    if not db_pool:
        raise RuntimeError("Database is not configured (missing DATABASE_URL).")
    return db_pool.getconn()

def release_connection(conn):
    if db_pool:
        db_pool.putconn(conn)

def get_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)