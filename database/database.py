import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'pharmacy.db')

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
    return conn

def init_db():
    """Initializes the database and creates the complaints table."""
    conn = get_connection()
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