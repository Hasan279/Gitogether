from models.db import *


def create_rating(match_id, rater_id, rated_id, score, review):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
                insert into ratings (match_id, rater_id, rated_id, score, review)
                values (%s, %s, %s, %s, %s)
                RETURNING rating_id
    """, (match_id, rater_id, rated_id, score, review))
    
    rating_id = cur.fetchone()['rating_id']
    
    conn.commit()
    cur.close()
    release_connection(conn)
    
    return rating_id

def get_rating_by_id(rating_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
                select * from ratings
                where rating_id = %s
    """, (rating_id,))
    
    rating_details = cur.fetchone()
    
    conn.commit()
    cur.close()
    release_connection(conn)
    return rating_details

def get_ratings_by_developer(developer_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
        SELECT r.*, dp.full_name as reviewer_name
        FROM ratings r
        JOIN developer_profiles dp ON r.rater_id = dp.developer_id
        WHERE r.rated_id = %s
        ORDER BY r.created_at DESC
    """, (developer_id,))

    details = cur.fetchall()
    conn.commit()
    cur.close()
    release_connection(conn)
    return details

def get_average_rating(developer_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
                select COALESCE(AVG(score), 0) as average_rating from ratings 
                where rated_id = %s
    """, (developer_id,))

    average_rating = cur.fetchone()['average_rating']
    
    conn.commit()
    cur.close()
    release_connection(conn)
    if not average_rating:
        return 0
    return float(average_rating)

def check_existing_rating(match_id, rater_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
                select * from ratings
                where match_id = %s and rater_id = %s
    """, (match_id, rater_id))

    rating = cur.fetchone()
    
    conn.commit()
    cur.close()
    release_connection(conn)

    return rating


def get_rated_match_ids(rater_id, match_ids):
    if not match_ids:
        return set()

    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute("""
        SELECT match_id
        FROM Ratings
        WHERE rater_id = %s
          AND match_id = ANY(%s)
    """, (rater_id, match_ids))

    rows = cur.fetchall()
    cur.close()
    release_connection(conn)

    return {row['match_id'] for row in rows}

def get_ratings_by_match(match_id):
    conn = get_connection()
    cur = get_cursor(conn)
    
    cur.execute("""
                select * from ratings
                where match_id = %s
    """, (match_id,))

    rating = cur.fetchall()
    
    conn.commit()
    cur.close()
    release_connection(conn)

    return rating

