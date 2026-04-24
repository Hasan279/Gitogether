from models.db import *


def create_request(developer_id, project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        INSERT INTO Requests (developer_id, project_id, status)
        VALUES (%s, %s, 'pending')
        RETURNING request_id
    """, (developer_id, project_id))
    
    request_id = cur.fetchone()['request_id']
    
    conn.commit()
    cur.close()
    conn.close()
    
    return request_id


def get_request_by_id(request_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT * FROM Requests
        WHERE request_id = %s
    """, (request_id,))
    
    request = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return request


def get_requests_by_project(project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT r.request_id, r.status, r.created_at,
               dp.developer_id, dp.full_name, dp.bio, dp.location,
               dp.years_experience, dp.contact_link, dp.avatar_url,
               u.email
        FROM Requests r
        JOIN Developer_Profiles dp ON r.developer_id = dp.developer_id
        JOIN Users u ON dp.user_id = u.user_id
        WHERE r.project_id = %s
        AND r.status = 'pending'
        ORDER BY r.created_at DESC
    """, (project_id,))
    
    pending_requests = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return pending_requests


def get_requests_by_developer(developer_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT r.request_id, r.status, r.created_at,
               p.project_id, p.title, p.status AS project_status, p.owner_id
        FROM Requests r
        JOIN Projects p ON r.project_id = p.project_id
        WHERE r.developer_id = %s
        ORDER BY r.created_at DESC
    """, (developer_id,))
    
    requests = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return requests


def update_request_status(request_id, status):
    conn = get_connection()
    cur = get_cursor(conn)
    
    # update request
    cur.execute("""
        UPDATE Requests
        SET status = %s
        WHERE request_id = %s
        RETURNING developer_id, project_id
    """, (status, request_id))
    
    result = cur.fetchone()
    
    if status == 'accepted' and result:
        developer_id = result['developer_id']
        project_id = result['project_id']
        
        # Add the accepted dev to the project
        cur.execute("""
            INSERT INTO Matches (developer_id, project_id, status)
            VALUES (%s, %s, 'active')
        """, (developer_id, project_id))
        
        # NOTE: The auto-reject block has been completely removed so 
        # other developers can still be accepted!
    
    conn.commit()
    cur.close()
    conn.close()


def check_existing_request(developer_id, project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT * FROM Requests
        WHERE developer_id = %s AND project_id = %s
    """, (developer_id, project_id))
    
    request = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return request