from models.db import *


def create_project(owner_id, title, description, location, slots_needed):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        INSERT INTO Projects (owner_id, title, description, location, slots_needed)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING project_id
    """, (owner_id, title, description, location, slots_needed))
    
    project_id = cur.fetchone()['project_id']
    
    conn.commit()
    cur.close()
    release_connection(conn)
    
    return project_id


def get_all_open_projects(skill_filter=None, page=1, per_page=10):
    offset = (page - 1) * per_page

    conn = get_connection()
    cur = get_cursor(conn)

    if skill_filter:
        cur.execute("""
            SELECT p.*, dp.full_name,
                   COALESCE(AVG(r.score), 0) AS avg_rating
            FROM Projects p
            JOIN Developer_Profiles dp ON p.owner_id = dp.developer_id
            LEFT JOIN Ratings r ON dp.developer_id = r.rated_id
            JOIN Project_Skills ps ON p.project_id = ps.project_id
            JOIN Skills s ON ps.skill_id = s.skill_id
            WHERE p.status = 'open' AND s.skill_name = %s
            GROUP BY p.project_id, dp.developer_id
            ORDER BY avg_rating DESC, p.created_at DESC
            LIMIT %s OFFSET %s
        """, (skill_filter, per_page, offset))
    else:
        cur.execute("""
            SELECT p.*, dp.full_name,
                   COALESCE(AVG(r.score), 0) AS avg_rating
            FROM Projects p
            JOIN Developer_Profiles dp ON p.owner_id = dp.developer_id
            LEFT JOIN Ratings r ON dp.developer_id = r.rated_id
            WHERE p.status = 'open'
            GROUP BY p.project_id, dp.developer_id
            ORDER BY avg_rating DESC, p.created_at DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))

    projects = cur.fetchall()
    cur.close()
    release_connection(conn)
    return projects
def get_dashboard_projects(owner_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
        SELECT * FROM projects 
        WHERE owner_id = %s AND status = 'open'
        ORDER BY created_at DESC
    """, (owner_id,))
    projects = cur.fetchall()
    cur.close()
    release_connection(conn)
    return projects

def get_incoming_requests(owner_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
        SELECT r.*, p.title, dp.full_name, dp.developer_id
        FROM requests r
        JOIN projects p ON r.project_id = p.project_id
        JOIN developer_profiles dp ON r.developer_id = dp.developer_id
        WHERE p.owner_id = %s AND r.status = 'pending'
        ORDER BY r.created_at DESC
    """, (owner_id,))
    requests = cur.fetchall()
    cur.close()
    release_connection(conn)
    return requests

def get_sent_requests(developer_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
        SELECT r.*, p.title
        FROM requests r
        JOIN projects p ON r.project_id = p.project_id
        WHERE r.developer_id = %s AND r.status IN ('pending', 'rejected')
        ORDER BY r.created_at DESC
    """, (developer_id,))
    requests = cur.fetchall()
    cur.close()
    release_connection(conn)
    return requests

def get_project_by_id(project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT p.*, dp.full_name, dp.bio, dp.avatar_url
        FROM Projects p
        JOIN Developer_Profiles dp ON p.owner_id = dp.developer_id
        WHERE p.project_id = %s
    """, (project_id,))
    
    project = cur.fetchone()
    
    cur.close()
    release_connection(conn)
    
    return project


def get_projects_by_owner(owner_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT * FROM Projects
        WHERE owner_id = %s
        ORDER BY created_at DESC
    """, (owner_id,))
    
    projects = cur.fetchall()
    
    cur.close()
    release_connection(conn)
    
    return projects

def get_projects_by_name(search_term):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT p.*, dp.full_name as owner_name
        FROM Projects p
        JOIN Developer_Profiles dp ON p.owner_id = dp.developer_id
        WHERE p.title ILIKE %s AND p.status = 'open'
        ORDER BY p.created_at DESC
    """, (f'%{search_term}%',))
    
    projects = cur.fetchall()
    cur.close()
    release_connection(conn)
    return projects

def update_project(project_id, title, description, location, slots_needed):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        UPDATE Projects
        SET title = %s,
            description = %s,
            location = %s,
            slots_needed = %s
        WHERE project_id = %s
    """, (title, description, location, slots_needed, project_id))
    
    conn.commit()
    cur.close()
    release_connection(conn)


def update_project_status(project_id, status):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        UPDATE Projects
        SET status = %s
        WHERE project_id = %s
    """, (status, project_id))
    
    conn.commit()
    cur.close()
    release_connection(conn)


def delete_project(project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        DELETE FROM Projects
        WHERE project_id = %s
    """, (project_id,))
    
    conn.commit()
    cur.close()
    release_connection(conn)