from models.db import get_connection

def get_all_skills():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(""" 
                select * from skills""")
    all_skills = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return all_skills

def add_skill(skill_name, category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                insert into skills (skill_name, category)
                values (%s, %s)
                RETURNING skill_id 
                """, (skill_name , category))
    skill_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return skill_id

def get_developer_skill(developer_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                select s.skill_id, s.skill_name, s.category, ds.proficiency_level
                from developer_skills ds
                join skills s
                on s.skill_id = ds.skill_id
                where ds.developer_id = %s
                """, (developer_id))
    dev_skills = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return dev_skills

def add_developer_skill(developer_id, skill_id, proficiency_level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                insert into developer_skills (developer_id, skill_id, proficiency_level)
                values (%s, %s, %s)
                """, (developer_id, skill_id, proficiency_level))
    conn.commit()
    cur.close()
    conn.close()

def remove_developer_skill (developer_id, skill_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                delete from developer_skills
                where developer_id = %s and skill_id = %s
                """, (developer_id, skill_id))
    conn.commit()
    cur.close()
    conn.close()

def get_project_skill (project_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                select s.skill_id, s.skill_name, s.catergory, ps.is_required
                from project_skills ps
                join skills s
                on s.kill_id = ps.skill_id
                where ps.project_id = %s
                """, (project_id))
    proj_skills = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return proj_skills

def add_project_skill (project_id, skill_id, is_required):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                insert into project_skills (project_id, skill_id, is_required)
                values (%s,%s, %s)
                """, (project_id, skill_id, is_required))
    conn.commit()
    cur.close()
    conn.close()

def remove_project_skill (project_id, skill_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                delete from project_skills 
                where project_id = %s and skill_id = %s
                """, (project_id, skill_id))
    conn.commit()
    cur.close()
    conn.close()
