from db import get_db_connection
import mysql.connector
def register_user(username, password):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        user_id = cur.lastrowid
        cur.close()
        return True, user_id
    except mysql.connector.IntegrityError:
        return False, "Username already exists."
    except Exception as e:
        return False, f"DB error: {e}"
    finally:
        if conn:
            conn.close()
def login_user(username, password):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
        row = cur.fetchone()
        cur.close()
        if row:
            return True, row[0]
        return False, None
    except Exception:
        return False, None
    finally:
        if conn:
            conn.close()
