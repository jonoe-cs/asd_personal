from database.database import get_connection
from complaints.complaint import Complaint
import pandas as pd

class ComplaintManager:

    db_path = None

    @staticmethod
    def set_database(db_path=None):
        ComplaintManager.db_path = db_path

    @staticmethod
    def add_complaint(complaint: Complaint):
        conn = get_connection(ComplaintManager.db_path)

        if not complaint.complaint_id or not complaint.complaint_id.strip():
            raise ValueError("Complaint ID is required.")

        if not complaint.customer_name or not complaint.customer_name.strip():
            raise ValueError("Customer name is required.")

        if not complaint.medicine or not complaint.medicine.strip():
            raise ValueError("Medicine is required.")

        if not complaint.description or not complaint.description.strip():
            raise ValueError("Complaint description is required.")

        allowed_severities = ["Low", "Medium", "High", "Critical"]

        if complaint.severity not in allowed_severities:
            raise ValueError("Please select a valid severity.")

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
        conn = get_connection(ComplaintManager.db_path)
        df = pd.read_sql_query("SELECT * FROM complaints", conn)
        conn.close()
        return df

    @staticmethod
    def update_complaint_status(complaint_id, status, resolution="Pending"):
        conn = get_connection(ComplaintManager.db_path)
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
        conn = get_connection(ComplaintManager.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE complaints
            SET assigned_staff = ?
            WHERE complaint_id = ?
        ''', (staff_member, complaint_id))
        conn.commit()
        conn.close()
