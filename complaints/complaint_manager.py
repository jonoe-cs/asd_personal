from database.database import get_connection
from complaints.complaint import Complaint
import pandas as pd

class ComplaintManager:
    @staticmethod
    def add_complaint(complaint: Complaint):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO complaints (complaint_id, customer_name, medicine, category, description, severity, assigned_staff, status, date_submitted, resolution)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', complaint.to_tuple())
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_complaints_df():
        """Returns all complaints as a Pandas DataFrame."""
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM complaints", conn)
        conn.close()
        return df

    @staticmethod
    def update_complaint_status(complaint_id, status, resolution="Pending"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE complaints
            SET status = ?, resolution = ?
            WHERE complaint_id = ?
        ''', (status, resolution, complaint_id))
        conn.commit()
        conn.close()

    @staticmethod
    def assign_staff(complaint_id, staff_member):
        """Allows authorized staff to assign complaints."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE complaints
            SET assigned_staff = ?
            WHERE complaint_id = ?
        ''', (staff_member, complaint_id))
        conn.commit()
        conn.close()
