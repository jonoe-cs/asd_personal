
from complaints.complaint import Complaint
from complaints.complaint_manager import ComplaintManager
from database.database import init_db


# Initialise the database
init_db()


# Create a complaint with a missing customer name
complaint = Complaint(
    "TEST001",
    "John Smith",  # Empty customer name
    "Paracetamol",
    "Side effect",
    "Customer reports a rash",
    "Urgent",
    "Unassigned",
    "Open",
    "18/11/2026",
    "Pending"
)


# Try to add the complaint
try:
    ComplaintManager.add_complaint(complaint)
    print("Complaint added successfully!")

except ValueError as error:
    print("Validation worked!")
    print(error)
