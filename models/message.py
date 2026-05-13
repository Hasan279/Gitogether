from models.db import get_connection, get_cursor, release_connection

def create_message(project_id, sender_id, content):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
        INSERT INTO Project_Messages (project_id, sender_id, content)
        VALUES (%s, %s, %s)
        RETURNING message_id
    """, (project_id, sender_id, content))
    message_id = cur.fetchone()['message_id']
    conn.commit()
    cur.close()
    release_connection(conn)
    return message_id

def get_project_messages(project_id, limit=50):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
        SELECT m.message_id, m.content, m.created_at, m.sender_id, d.full_name as sender_name
        FROM Project_Messages m
        JOIN Developer_Profiles d ON m.sender_id = d.developer_id
        WHERE m.project_id = %s
        ORDER BY m.created_at ASC
        LIMIT %s
    """, (project_id, limit))
    messages = cur.fetchall()
    cur.close()
    release_connection(conn)
    return messages
