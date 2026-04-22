from models.db import *


def create_project(owner_id, title, description, location, slots_needed):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        INSERT INTO Projects (owner_id, title, description, location, slots_needed)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING project_id
    """, (owner_id, title, description, location, slots_needed))
    
    project_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    
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
    conn.close()
    return projects

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
    conn.close()
    
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
    conn.close()
    
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
    conn.close()


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
    conn.close()


def delete_project(project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        DELETE FROM Projects
        WHERE project_id = %s
    """, (project_id,))
    
    conn.commit()
    cur.close()
    conn.close()