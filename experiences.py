# experiences.py
from db import get_db_connection

# -------------------- Add --------------------
def add_experience(user_id, company, role, experience_text, difficulty=""):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO experiences
            (user_id, company, role, experience, difficulty)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, company, role, experience_text, difficulty)
        )
        conn.commit()
        cur.close()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        if conn:
            conn.close()


# -------------------- Fetch All --------------------
def fetch_experiences(limit=500):
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT e.id,
                   u.username,
                   e.company,
                   e.role,
                   COALESCE(e.experience,'') AS summary,
                   COALESCE(e.difficulty,'') AS difficulty,
                   e.date_posted
            FROM experiences e
            JOIN users u ON e.user_id = u.id
            ORDER BY e.date_posted DESC
            LIMIT %s
            """, (limit,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        print("fetch_experiences error:", e)
        return []
    finally:
        if conn:
            conn.close()


# -------------------- Search --------------------
def search_experiences(term, limit=500):

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        like = f"%{term}%"
        cur.execute(
            """
            SELECT e.id,
                   u.username,
                   e.company,
                   e.role,
                   COALESCE(e.experience,'') AS summary,
                   COALESCE(e.difficulty,'') AS difficulty,
                   e.date_posted
            FROM experiences e
            JOIN users u ON e.user_id = u.id
            WHERE e.company LIKE %s OR e.role LIKE %s OR e.difficulty LIKE %s
            ORDER BY e.date_posted DESC
            LIMIT %s
            """, (like, like, like, limit)
        )
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        print("search_experiences error:", e)
        return []
    finally:
        if conn:
            conn.close()


# -------------------- Fetch by ID --------------------
def get_experience_by_id(exp_id):
   
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT e.id, u.username, e.company, e.role,
                   e.experience, e.difficulty, e.date_posted
            FROM experiences e
            JOIN users u ON e.user_id = u.id
            WHERE e.id = %s
            """, (exp_id,)
        )
        row = cur.fetchone()
        cur.close()
        return row
    except Exception as e:
        print("get_experience_by_id error:", e)
        return None
    finally:
        if conn:
            conn.close()
