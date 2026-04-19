import bcrypt
from models.db import get_connection
def create_user(email, password, role = "developer"):
    conn = get_connection()
    cur = conn.cursor()
    password_hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    cur.execute("""
                INSERT INTO USERS(email,password_hash,role)
                VALUES(%s, %s, %s)
                RETURNING user_id
                """,(email,password_hashed,role))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return user_id

def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                DELETE FROM USERS
                WHERE user_id = (%s)
                """,(user_id))
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
               Select * FROM USERS
               WHERE email = (%s)
                """,(email,))
    User = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return User

def get_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
               Select * FROM USERS
               WHERE user_id = (%s)
                """,(user_id))
    User = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return User

def verify_password(plain_password,hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password.encode('utf-8'))
        
def activate_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                    update users 
                set is_active = TRUE
                where user_id = %s """, (user_id))
    conn.commit()
    cur.close()
    conn.close()

def deactivate_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(""" 
                    update users
                set is_active = FALSE
                where user_id = %s""", (user_id))
    conn.commit()
    cur.close()
    conn.close()

def create_developer_profile(user_id, full_name, bio, location, years_experience, contact_link, avatar_url=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO developer_profiles(user_id, full_name, bio, location, years_experience, contact_link, avatar_url)
                VALUES(%s, %s, %s, %s, %s, %s, %s)
                RETURNING developer_id
                """,(user_id, full_name, bio, location, years_experience, contact_link, avatar_url))
    developer_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return developer_id

def get_developer_by_user_id(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                SELECT dp.*, u.email, u.role
                FROM developer_profiles dp
                JOIN users u ON u.user_id = dp.user_id
                where user_id = (%s)
               """,(user_id))
    developer = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return developer 
    
def get_developer_by_name(full_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
               SELECT dp.*, u.email, u.role
                FROM developer_profiles dp
                JOIN users u ON u.user_id = dp.user_id
                where full_name = (%s)
                """,(full_name))
    developer = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return developer 

def update_developer_profile(user_id, full_name, bio, location, years_experience, contact_link, avatar_url=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                update developer_profiles
                set full_name = %s, 
                bio = %s,
                location = %s,
                years_experience = %s,
                contact_link = %s,
                avatar_url = %s,
                where user_id = %s """, (full_name, bio, location, years_experience, contact_link, avatar_url, user_id))
    conn.commit()
    cur.close()
    conn.close()


def delete_developer_profile(user_id):
    conn = get_connection()
    cur= conn.cursor()
    cur.execute(""" delete from developer_profiles
                where user_id = %s """, (user_id))
    conn.commit()
    cur.close()
    conn.close()

    
    