import psycopg2.extras
from models.db import get_connection, release_connection, get_cursor

def create_query(sender_id, subject, message):
    conn = get_connection()
    try:
        with conn:
            with get_cursor(conn) as cur:
                cur.execute(
                    """
                    INSERT INTO Developer_Queries (sender_id, subject, message)
                    VALUES (%s, %s, %s)
                    RETURNING query_id;
                    """,
                    (sender_id, subject, message)
                )
                return cur.fetchone()['query_id']
    except Exception as e:
        print("Error creating query:", e)
        return None
    finally:
        release_connection(conn)

def get_all_queries(status=None):
    conn = get_connection()
    try:
        with get_cursor(conn) as cur:
            if status:
                cur.execute("""
                    SELECT q.*, d.full_name, d.avatar_url, u.email 
                    FROM Developer_Queries q
                    JOIN Developer_Profiles d ON q.sender_id = d.developer_id
                    JOIN Users u ON d.user_id = u.user_id
                    WHERE q.status = %s
                    ORDER BY q.created_at DESC;
                """, (status,))
            else:
                cur.execute("""
                    SELECT q.*, d.full_name, d.avatar_url, u.email 
                    FROM Developer_Queries q
                    JOIN Developer_Profiles d ON q.sender_id = d.developer_id
                    JOIN Users u ON d.user_id = u.user_id
                    ORDER BY CASE WHEN q.status = 'open' THEN 0 ELSE 1 END, q.created_at DESC;
                """)
            return cur.fetchall()
    finally:
        release_connection(conn)

def mark_query_resolved(query_id):
    conn = get_connection()
    try:
        with conn:
            with get_cursor(conn) as cur:
                cur.execute(
                    "UPDATE Developer_Queries SET status = 'resolved' WHERE query_id = %s;",
                    (query_id,)
                )
    except Exception as e:
        print("Error resolving query:", e)
    finally:
        release_connection(conn)
