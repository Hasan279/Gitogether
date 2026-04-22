from models.db import *

def create_match(developer_id, project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                    INSERT INTO Matches (developer_id, project_id, status)
                    VALUES (%s, %s, 'active')
                    RETURNING match_id
                    """, (developer_id, project_id))
    match_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return match_id



def get_match_by_id(match_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                    SELECT * FROM Matches
                    WHERE match_id = %s
                    """, (match_id,))
    match = cur.fetchone()
    cur.close()
    conn.close()
    return match



def get_active_matches_by_developer(developer_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                    SELECT m.* , p.title, p.location, p.owner_id
                    FROM Matches m
                    JOIN Projects p ON m.project_id = p.project_id
                    WHERE m.developer_id = %s AND m.status = 'active'
                    """, (developer_id,))
    matches = cur.fetchall()
    cur.close()
    conn.close()
    return matches



def get_completed_matches_by_developer(developer_id, limit=3):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                    SELECT m.* , p.title, p.location, p.owner_id
                    FROM Matches m
                    JOIN Projects p ON m.project_id = p.project_id
                    WHERE m.developer_id = %s AND m.status = 'completed'
                    ORDER BY m.completed_at DESC
                    LIMIT %s
                    """, (developer_id, limit))
    
    matches = cur.fetchall()
    cur.close()
    conn.close()
    return matches



def complete_match(match_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                    UPDATE Matches
                    SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                    WHERE match_id = %s
                    """, (match_id,))
    conn.commit()
    cur.close()
    conn.close()



def check_existing_match(developer_id, project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                    SELECT * FROM Matches
                    WHERE developer_id = %s AND project_id = %s
                    """, (developer_id, project_id))
    match = cur.fetchone()
    cur.close()
    conn.close()
    return match