import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'pharmacy.db')

def get_connection(db_path=None):
    if db_path is None:
        db_path = DB_PATH

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=None):
    """Initialises the database and creates the complaints table."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id TEXT PRIMARY KEY,
            customer_name TEXT,
            medicine TEXT,
            category TEXT,
            description TEXT,
            severity TEXT,
            assigned_staff TEXT,
            status TEXT,
            date_submitted TEXT,
            resolution TEXT
        )
    ''')

    conn.commit()
    conn.close()
