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


def get_all_open_projects(skill_filter=None, page=1, per_page=10, exclude_owner_id=None):
    offset = (page - 1) * per_page

    conn = get_connection()
    cur = get_cursor(conn)

    if skill_filter:
        query = """
            SELECT p.*, dp.full_name, dp.avatar_url,
                   COALESCE(AVG(r.score), 0) AS avg_rating,
                   ARRAY_REMOVE(ARRAY_AGG(DISTINCT s_all.skill_name), NULL) AS required_skills
            FROM Projects p
            JOIN Developer_Profiles dp ON p.owner_id = dp.developer_id
            LEFT JOIN Ratings r ON dp.developer_id = r.rated_id
            JOIN Project_Skills ps ON p.project_id = ps.project_id
            JOIN Skills s ON ps.skill_id = s.skill_id
            LEFT JOIN Project_Skills ps_all ON p.project_id = ps_all.project_id
            LEFT JOIN Skills s_all ON ps_all.skill_id = s_all.skill_id
            WHERE p.status = 'open' AND s.skill_name = %s
        """
        params = [skill_filter]
        if exclude_owner_id is not None:
            query += " AND p.owner_id != %s"
            params.append(exclude_owner_id)
        query += """
            GROUP BY p.project_id, dp.developer_id
            ORDER BY avg_rating DESC, p.created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([per_page, offset])
        cur.execute(query, tuple(params))
    else:
        query = """
            SELECT p.*, dp.full_name, dp.avatar_url,
                   COALESCE(AVG(r.score), 0) AS avg_rating,
                   ARRAY_REMOVE(ARRAY_AGG(DISTINCT s_all.skill_name), NULL) AS required_skills
            FROM Projects p
            JOIN Developer_Profiles dp ON p.owner_id = dp.developer_id
            LEFT JOIN Ratings r ON dp.developer_id = r.rated_id
            LEFT JOIN Project_Skills ps_all ON p.project_id = ps_all.project_id
            LEFT JOIN Skills s_all ON ps_all.skill_id = s_all.skill_id
            WHERE p.status = 'open'
        """
        params = []
        if exclude_owner_id is not None:
            query += " AND p.owner_id != %s"
            params.append(exclude_owner_id)
        query += """
            GROUP BY p.project_id, dp.developer_id
            ORDER BY avg_rating DESC, p.created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([per_page, offset])
        cur.execute(query, tuple(params))

    projects = cur.fetchall()
    cur.close()
    release_connection(conn)
    return projects


def count_open_projects(skill_filter=None, exclude_owner_id=None):
    conn = get_connection()
    cur = get_cursor(conn)

    query = """
        SELECT COUNT(DISTINCT p.project_id) AS total
        FROM Projects p
    """
    params = []

    if skill_filter:
        query += """
            JOIN Project_Skills ps ON p.project_id = ps.project_id
            JOIN Skills s ON ps.skill_id = s.skill_id
        """

    query += " WHERE p.status = 'open'"

    if skill_filter:
        query += " AND s.skill_name = %s"
        params.append(skill_filter)

    if exclude_owner_id is not None:
        query += " AND p.owner_id != %s"
        params.append(exclude_owner_id)

    cur.execute(query, tuple(params))
    row = cur.fetchone()
    cur.close()
    release_connection(conn)
    return row['total'] if row else 0

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

def get_projects_by_name(search_term, skill_filter=None, limit=20, exclude_owner_id=None):
    conn = get_connection()
    cur = get_cursor(conn)

    query = """
        SELECT p.*, dp.full_name, dp.full_name as owner_name, dp.avatar_url,
               ARRAY_REMOVE(ARRAY_AGG(DISTINCT s_all.skill_name), NULL) AS required_skills
        FROM Projects p
        JOIN Developer_Profiles dp ON p.owner_id = dp.developer_id
        LEFT JOIN Project_Skills ps_all ON p.project_id = ps_all.project_id
        LEFT JOIN Skills s_all ON ps_all.skill_id = s_all.skill_id
        WHERE (p.title ILIKE %s OR dp.full_name ILIKE %s) AND p.status = 'open'
    """
    params = [f'%{search_term}%', f'%{search_term}%']

    if skill_filter:
        query += """
        AND EXISTS (
            SELECT 1
            FROM Project_Skills ps_filter
            JOIN Skills s_filter ON ps_filter.skill_id = s_filter.skill_id
            WHERE ps_filter.project_id = p.project_id
              AND s_filter.skill_name = %s
        )
        """
        params.append(skill_filter)

    if exclude_owner_id is not None:
        query += " AND p.owner_id != %s"
        params.append(exclude_owner_id)

    query += """
        GROUP BY p.project_id, dp.developer_id
        ORDER BY p.created_at DESC
    """
    if limit is not None:
        query += "\n LIMIT %s"
        params.append(limit)

    cur.execute(query, tuple(params))
    
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