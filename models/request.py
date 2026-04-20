from models.db import get_connection

def create_request(developer_id, project_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                insert into requests(developer_id, project_id, status)
                values (%s, %s, 'pending')
                RETURNING request_id
                    """, (developer_id, project_id))
    request_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return request_id

def get_request_by_id(request_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                select * from requests 
                where request_id = %s
                    """, (request_id))
    request = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return request

def get_requests_by_project(project_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(""" SELECT r.request_id, r.status, r.created_at,

    dp.developer_id,dp.full_name,dp.bio,dp.location,dp.years_experience,dp.contact_link,dp.avatar_url,

    u.email

    FROM Requests r
    JOIN Developer_Profiles dp 
    ON r.developer_id = dp.developer_id
    JOIN Users u 
    ON dp.user_id = u.user_id

    WHERE r.project_id = (%s)
    AND r.status = (%s)

    ORDER BY r.created_at DESC""",(project_id,'pending'))
    pending_requests = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return pending_requests

def get_requests_by_developer(developer_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                





                    """)

    conn.commit()
    cur.close()
    conn.close()
    return requests

def update_request_status(request_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                UPDATE Requests
                SET status = %s
                WHERE request_id = %s
                    """, (status, request_id))
    conn.commit()
    cur.close()
    conn.close()

def check_existing_request(developer_id, project_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                SELECT * FROM Requests
                WHERE developer_id = %s AND project_id = %s
                    """, (developer_id, project_id))
    request = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return request
