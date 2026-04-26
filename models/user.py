import bcrypt
from models.db import *
def create_user(email, password, role = "developer"):
    conn = get_connection()
    cur = get_cursor(conn)
    password_hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    cur.execute("""
                INSERT INTO USERS(email,password_hash,role)
                VALUES(%s, %s, %s)
                RETURNING user_id
                """,(email,password_hashed,role))
    user_id = cur.fetchone()['user_id']
    conn.commit()
    cur.close()
    release_connection(conn)
    return user_id

def delete_user(user_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                DELETE FROM USERS
                WHERE user_id = (%s)
                """,(user_id))
    conn.commit()
    cur.close()
    release_connection(conn)

def get_user_by_email(email):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
               Select * FROM USERS
               WHERE email = (%s)
                """,(email,))
    User = cur.fetchone()
    conn.commit()
    cur.close()
    release_connection(conn)
    return User

def get_user_by_id(user_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
               Select * FROM USERS
               WHERE user_id = (%s)
                """,(user_id))
    User = cur.fetchone()
    conn.commit()
    cur.close()
    release_connection(conn)
    return User

def verify_password(plain_password,hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password.encode('utf-8'))
        
def activate_user(user_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                    update users 
                set is_active = TRUE
                where user_id = %s """, (user_id))
    conn.commit()
    cur.close()
    release_connection(conn)

def deactivate_user(user_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute(""" 
                    update users
                set is_active = FALSE
                where user_id = %s""", (user_id))
    conn.commit()
    cur.close()
    release_connection(conn)

def create_developer_profile(user_id, full_name, bio, location, years_experience, contact_link, avatar_url=None):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                INSERT INTO developer_profiles(user_id, full_name, bio, location, years_experience, contact_link, avatar_url)
                VALUES(%s, %s, %s, %s, %s, %s, %s)
                RETURNING developer_id
                """,(user_id, full_name, bio, location, years_experience, contact_link, avatar_url))
    developer_id = cur.fetchone()['developer_id']
    conn.commit()
    cur.close()
    release_connection(conn)
    return developer_id

def get_developer_by_user_id(user_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                SELECT dp.*, u.email, u.role
                FROM developer_profiles dp
                JOIN users u ON u.user_id = dp.user_id
                where dp.user_id = (%s)
               """,(user_id,))
    developer = cur.fetchone()
    conn.commit()
    cur.close()
    release_connection(conn)
    return developer

def get_developer_by_id(dev_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("SELECT * FROM Developer_Profiles WHERE developer_id = %s", (dev_id,))
    result = cur.fetchone()
    cur.close()
    release_connection(conn)
    return result

def get_developer_id(user_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("SELECT developer_id FROM Developer_Profiles WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    cur.close()
    release_connection(conn)
    return result['developer_id'] if result else None

def get_developer_by_name(full_name, limit=20):
    conn = get_connection()
    cur = get_cursor(conn)
    query = """
        SELECT dp.*, u.email, u.role
        FROM developer_profiles dp
        JOIN users u ON u.user_id = dp.user_id
        WHERE dp.full_name ILIKE %s
        ORDER BY dp.full_name ASC
    """
    params = [f'%{full_name}%']
    if limit is not None:
        query += "\n LIMIT %s"
        params.append(limit)

    cur.execute(query, tuple(params))
    developer = cur.fetchall()
    conn.commit()
    cur.close()
    release_connection(conn)
    return developer 


def update_developer_profile(user_id, full_name, bio, location, years_experience, contact_link, avatar_url=None):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                update developer_profiles
                set full_name = %s, 
                bio = %s,
                location = %s,
                years_experience = %s,
                contact_link = %s,
                avatar_url = %s
                where user_id = %s """, (full_name, bio, location, years_experience, contact_link, avatar_url, user_id))
    conn.commit()
    cur.close()
    release_connection(conn)


def get_all_developers(skill_filter=None, page=1, per_page=10):
    offset = (page - 1) * per_page
    conn = get_connection()
    cur = get_cursor(conn)

    if skill_filter:
        cur.execute("""
            SELECT 
                dp.developer_id,
                dp.full_name,
                dp.bio,
                dp.location,
                dp.years_experience,
                dp.avatar_url,
                COALESCE(AVG(r.score), 0) AS avg_rating,
                ARRAY_AGG(DISTINCT s.skill_name) AS skills
            FROM developer_profiles dp
            LEFT JOIN developer_skills ds ON dp.developer_id = ds.developer_id
            LEFT JOIN skills s ON ds.skill_id = s.skill_id
            LEFT JOIN ratings r ON dp.developer_id = r.rated_id
            
            WHERE dp.developer_id IN (
                SELECT developer_id 
                FROM developer_skills ds2 
                JOIN skills s2 ON ds2.skill_id = s2.skill_id 
                WHERE s2.skill_name = %s
            )
            
            GROUP BY dp.developer_id
            ORDER BY avg_rating DESC, dp.years_experience DESC
            LIMIT %s OFFSET %s
        """, (skill_filter, per_page, offset))
    else:
        
        cur.execute("""
            SELECT 
                dp.developer_id,
                dp.full_name,
                dp.bio,
                dp.location,
                dp.years_experience,
                dp.avatar_url,
                COALESCE(AVG(r.score), 0) AS avg_rating,
                ARRAY_AGG(DISTINCT s.skill_name) AS skills
            FROM developer_profiles dp
            LEFT JOIN developer_skills ds ON dp.developer_id = ds.developer_id
            LEFT JOIN skills s ON ds.skill_id = s.skill_id
            LEFT JOIN ratings r ON dp.developer_id = r.rated_id
            GROUP BY dp.developer_id
            ORDER BY avg_rating DESC, dp.years_experience DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))

    developers = cur.fetchall()
    cur.close()
    release_connection(conn)
    return developers

def delete_developer_profile(user_id):
    conn = get_connection()
    cur= get_cursor(conn)
    cur.execute(""" delete from developer_profiles
                where user_id = %s """, (user_id))
    conn.commit()
    cur.close()
    release_connection(conn)

    
    