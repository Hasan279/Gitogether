from models.db import *


def get_all_skills():
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT * FROM Skills
    """)
    
    all_skills = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return all_skills


def add_skill(skill_name, category):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        INSERT INTO Skills (skill_name, category)
        VALUES (%s, %s)
        ON CONFLICT (skill_name) DO NOTHING
        RETURNING skill_id
    """, (skill_name, category))
    
    result = cur.fetchone()
    
    if result:
        skill_id = result[0]
    else:
        cur.execute("""
            SELECT skill_id FROM Skills WHERE skill_name = %s
        """, (skill_name,))
        skill_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    
    return skill_id


def get_developer_skills(developer_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT s.skill_id, s.skill_name, s.category, ds.proficiency_level
        FROM Developer_Skills ds
        JOIN Skills s ON s.skill_id = ds.skill_id
        WHERE ds.developer_id = %s
    """, (developer_id,))
    
    dev_skills = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return dev_skills


def add_developer_skill(developer_id, skill_id, proficiency_level):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        INSERT INTO Developer_Skills (developer_id, skill_id, proficiency_level)
        VALUES (%s, %s, %s)
        ON CONFLICT (developer_id, skill_id) DO NOTHING
    """, (developer_id, skill_id, proficiency_level))
    
    conn.commit()
    cur.close()
    conn.close()


def remove_developer_skill(developer_id, skill_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        DELETE FROM Developer_Skills
        WHERE developer_id = %s AND skill_id = %s
    """, (developer_id, skill_id))
    
    conn.commit()
    cur.close()
    conn.close()


def get_project_skills(project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT s.skill_id, s.skill_name, s.category, ps.is_required
        FROM Project_Skills ps
        JOIN Skills s ON s.skill_id = ps.skill_id
        WHERE ps.project_id = %s
    """, (project_id,))
    
    proj_skills = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return proj_skills


def add_project_skill(project_id, skill_id, is_required):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        INSERT INTO Project_Skills (project_id, skill_id, is_required)
        VALUES (%s, %s, %s)
        ON CONFLICT (project_id, skill_id) DO NOTHING
    """, (project_id, skill_id, is_required))
    
    conn.commit()
    cur.close()
    conn.close()


def remove_project_skill(project_id, skill_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        DELETE FROM Project_Skills
        WHERE project_id = %s AND skill_id = %s
    """, (project_id, skill_id))
    
    conn.commit()
    cur.close()
    conn.close()