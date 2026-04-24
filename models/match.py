from models.db import *

def create_match(developer_id, project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                    INSERT INTO Matches (developer_id, project_id, status)
                    VALUES (%s, %s, 'active')
                    RETURNING match_id
                    """, (developer_id, project_id))
    match_id = cur.fetchone()['match_id']
    conn.commit()
    cur.close()
    release_connection(conn)
    return match_id



def get_match_by_id(match_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
        SELECT m.*, p.owner_id, p.title 
        FROM Matches m
        JOIN Projects p ON m.project_id = p.project_id
        WHERE m.match_id = %s
    """, (match_id,))
    match = cur.fetchone()
    cur.close()
    release_connection(conn)
    return match

def get_active_match_count(project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
        SELECT COUNT(*) as member_count 
        FROM Matches 
        WHERE project_id = %s AND status = 'active'
    """, (project_id,))
    result = cur.fetchone()
    cur.close()
    release_connection(conn)
    
    return result['member_count'] if result else 0

def get_active_matches_by_developer(developer_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    query = """
        SELECT 
            p.project_id,
            lead_dp.full_name as owner_name,
            MAX(CASE WHEN m.developer_id = %s THEN m.match_id ELSE m.match_id END) as match_id, 
            p.title,
            p.location,
            p.owner_id,
            MIN(m.matched_at) as matched_at,
            json_agg(
                json_build_object(
                    'name', dp.full_name,
                    'avatar', dp.avatar_url,
                    'id', dp.developer_id
                )
            ) as team_members
        FROM Matches m
        JOIN Projects p ON m.project_id = p.project_id
        JOIN developer_profiles dp ON m.developer_id = dp.developer_id
        JOIN developer_profiles lead_dp ON p.owner_id = lead_dp.developer_id
        WHERE p.project_id IN (
            SELECT project_id FROM Projects WHERE owner_id = %s
            UNION
            SELECT project_id FROM Matches WHERE developer_id = %s AND status = 'active'
        )
        AND m.status = 'active'
        GROUP BY p.project_id, p.title, p.location, p.owner_id,lead_dp.full_name
        ORDER BY matched_at DESC
    """
    # Notice we pass the ID three times now
    cur.execute(query, (developer_id, developer_id, developer_id))
    matches = cur.fetchall()
    cur.close()
    release_connection(conn)
    return matches


def get_completed_matches_by_developer(developer_id, limit=10):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT 
            p.project_id,
            MAX(CASE WHEN m.developer_id = %s THEN m.match_id ELSE m.match_id END) as match_id,
            p.title,
            p.location,
            p.owner_id,
            MAX(m.completed_at) as completed_at,
            json_agg(
                json_build_object(
                    'name', dp.full_name,
                    'avatar', dp.avatar_url,
                    'id', dp.developer_id
                )
            ) as team_members
        FROM Matches m
        JOIN Projects p ON m.project_id = p.project_id
        JOIN developer_profiles dp ON m.developer_id = dp.developer_id
        WHERE p.project_id IN (
            SELECT project_id FROM Projects WHERE owner_id = %s
            UNION
            SELECT project_id FROM Matches WHERE developer_id = %s AND status = 'completed'
        )
        AND m.status = 'completed'
        GROUP BY p.project_id, p.title, p.location, p.owner_id
        ORDER BY completed_at DESC
        LIMIT %s
    """, (developer_id, developer_id, developer_id, limit))
    
    matches = cur.fetchall()
    cur.close()
    release_connection(conn)
    return matches


def complete_match(match_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                    UPDATE Matches
                    SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                    WHERE match_id = %s
                    """, (match_id,))
    conn.commit()
    cur.close()
    release_connection(conn)



def check_existing_match(developer_id, project_id):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("""
                    SELECT * FROM Matches
                    WHERE developer_id = %s AND project_id = %s
                    """, (developer_id, project_id))
    match = cur.fetchone()
    cur.close()
    release_connection(conn)
    return match

def get_unrated_team_members(project_id, rater_id):
    """
    Finds one active developer on a project who hasn't been rated by the Leader yet.
    """
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT 
            m.match_id, 
            m.developer_id, 
            dp.full_name
        FROM Matches m
        JOIN developer_profiles dp ON m.developer_id = dp.developer_id
        WHERE m.project_id = %s 
          AND m.status = 'active'
          AND NOT EXISTS (
              SELECT 1 FROM Ratings r 
              WHERE r.match_id = m.match_id 
                AND r.rater_id = %s
          )
        LIMIT 1
    """, (project_id, rater_id))
    
    unrated_dev = cur.fetchone() 
    cur.close()
    release_connection(conn)
    
    return unrated_dev

def complete_project_matches(project_id):
    """
    Marks all active matches for a project as completed once all ratings are done.
    Also updates the main project status to 'completed'.
    """
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        UPDATE Matches
        SET status = 'completed', completed_at = CURRENT_TIMESTAMP
        WHERE project_id = %s AND status = 'active'
    """, (project_id,))
    
    cur.execute("""
        UPDATE Projects
        SET status = 'completed'
        WHERE project_id = %s
    """, (project_id,))
    
    conn.commit()
    cur.close()
    release_connection(conn)