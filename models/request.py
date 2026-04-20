from models.db import get_connection

def create_request(developer_id, project_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                





                    """)

    conn.commit()
    cur.close()
    conn.close()
    return request_id

def get_request_by_id(request_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                





                    """)

    conn.commit()
    cur.close()
    conn.close()
    return request

def get_requests_by_project(project_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                





                    """)

    conn.commit()
    cur.close()
    conn.close()
    return requests

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
                





                    """)

    conn.commit()
    cur.close()
    conn.close()

def check_existing_request(developer_id, project_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                





                    """)

    conn.commit()
    cur.close()
    conn.close()
    return request
