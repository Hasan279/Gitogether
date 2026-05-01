from models.db import *

def get_global_stats():
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
        SELECT 
            (SELECT COUNT(*) FROM users) as total_users,
            (SELECT COUNT(*) FROM projects WHERE status = 'open') as active_projects,
            (SELECT COUNT(*) FROM matches WHERE status = 'completed') as completed_matches,
            (SELECT COALESCE(AVG(score), 0) FROM ratings) as global_avg
    """)
    stats = cur.fetchone()
    cur.close()
    release_connection(conn)
    return stats

def get_all_projects_oversight(search_term=None, limit=100):
    conn = get_connection()
    cur = get_cursor(conn)
    query = """
        SELECT p.*, dp.full_name
        FROM projects p
        JOIN developer_profiles dp ON p.owner_id = dp.developer_id
    """
    params = []
    if search_term:
        query += " WHERE p.title ILIKE %s OR dp.full_name ILIKE %s"
        params.extend([f'%{search_term}%', f'%{search_term}%'])
        
    query += " ORDER BY p.created_at DESC"
    if limit is not None:
        query += " LIMIT %s"
        params.append(limit)
    cur.execute(query, tuple(params))
    projects = cur.fetchall()
    cur.close()
    release_connection(conn)
    return projects

def get_all_ratings_oversight(search_term=None, limit=100):
    conn = get_connection()
    cur = get_cursor(conn)
    query = """
        SELECT r.*, rater.full_name as reviewer_name, rated.full_name as rated_name
        FROM ratings r
        JOIN developer_profiles rater ON r.rater_id = rater.developer_id
        JOIN developer_profiles rated ON r.rated_id = rated.developer_id
    """
    params = []
    if search_term:
        query += " WHERE rater.full_name ILIKE %s OR rated.full_name ILIKE %s OR r.review ILIKE %s"
        params.extend([f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'])
        
    query += " ORDER BY r.created_at DESC"
    if limit is not None:
        query += " LIMIT %s"
        params.append(limit)
    cur.execute(query, tuple(params))
    ratings = cur.fetchall()
    cur.close()
    release_connection(conn)
    return ratings

def get_all_developers_oversight(search_term=None, limit=100):
    conn = get_connection()
    cur = get_cursor(conn)
    query = """
        SELECT u.user_id, u.email, u.is_active, dp.full_name, dp.avatar_url
        FROM users u
        LEFT JOIN developer_profiles dp ON u.user_id = dp.user_id
        WHERE u.role = 'developer'
    """
    params = []
    if search_term:
        query += " AND (dp.full_name ILIKE %s OR u.email ILIKE %s)"
        params.extend([f'%{search_term}%', f'%{search_term}%'])
        
    query += " ORDER BY u.created_at DESC"
    if limit is not None:
        query += " LIMIT %s"
        params.append(limit)
    cur.execute(query, tuple(params))
    devs = cur.fetchall()
    cur.close()
    release_connection(conn)
    return devs

def toggle_user_status_admin(user_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
        UPDATE users 
        SET is_active = NOT is_active 
        WHERE user_id = %s AND role != 'admin'
    """, (user_id,))
    conn.commit()
    cur.close()
    release_connection(conn)

def delete_rating_admin(rating_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("DELETE FROM ratings WHERE rating_id = %s", (rating_id,))
    conn.commit()
    cur.close()
    release_connection(conn)

def delete_project_admin(project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("DELETE FROM projects WHERE project_id = %s", (project_id,))
    conn.commit()
    cur.close()
    release_connection(conn)