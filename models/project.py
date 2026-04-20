from models.db import get_connection

def create_project(owner_id, title, description, location, slots_needed, status, created_at):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                    INSERT INTO projects (owner_id, title, description, location, slots_needed, status, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING project_id
                    """, (owner_id, title, description, location, slots_needed, status, created_at))
    project_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return project_id

def get_all_open_projects (skill_filter=None, page=1, per_page=10):
    offset = (page - 1) * per_page
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            if skill_filter:
                cur.execute("""
                            SELECT p.*, dp.full_name AS owner_name, COALESCE(dp.average_rating, 0) AS owner_rating
                            FROM projects p
                            JOIN developer_profiles dp ON p.owner_id = dp.user_id
                            JOIN project_skills ps ON p.project_id = ps.project_id
                            JOIN skills s ON ps.skill_id = s.skill_id
                            WHERE p.status = 'open' AND s.skill_name = %s
                            ORDER BY owner_rating DESC, p.created_at DESC
                            LIMIT %s OFFSET %s
                            """, (skill_filter, per_page, offset))
            return cur.fetchall()

def get_project_by_id (project_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                SELECT p.*, d.full_name as Owner_Name, d.bio as Owner_Bio, d.avatar_url
                from projects p
                JOIN Developer_Profiles ON p.owner_id = d.user_id
                WHERE p.project_id = %s
                """, (project_id))
    project = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return project

def get_projects_by_onwer(owner_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                    SELECT * FROM Projects
                    WHERE owner_id = %s
                    ORDER BY created_at DESC
                    """, (owner_id))
    projects = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return projects

def update_project(project_id, title, description, location, slots_needed):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                    UPDATE Projects
                    SET title = %s, description = %s, location = %s, slots_needed = %s
                    WHERE project_id = %s
                    """, (title, description, location, slots_needed, project_id))
    conn.commit()
    cur.close()
    conn.close()

def update_project_status(project_id, status):
    conn = get_connection()
    cur = conn.cursor()
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
    cur = conn.cursor()
    cur.execute("""
                    DELETE FROM Projects
                    WHERE project_id = %s
                    """, (project_id))
    conn.commit()
    cur.close()
    conn.close()
