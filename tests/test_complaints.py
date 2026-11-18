import pytest

from complaints.complaint import Complaint
from complaints.complaint_manager import ComplaintManager

def test_empty_ID_is_rejected():

    complaint = Complaint(
        "",#
        "John Smith",
        "Paracetamol",
        "Side effect",
        "Customer reports a rash",
        "Medium",
        "Unassigned",
        "Open",
        "18/11/2026",
        "Pending"
    )

    with pytest.raises(ValueError):
        ComplaintManager.add_complaint(complaint)


def test_empty_customer_name_is_rejected():

    complaint = Complaint(
        "TEST002",
        "",#
        "Paracetamol",
        "Side effect",
        "Customer reports a rash",
        "Medium",
        "Unassigned",
        "Open",
        "18/11/2026",
        "Pending"
    )

    with pytest.raises(ValueError):
        ComplaintManager.add_complaint(complaint)

def test_empty_medicine_is_rejected():

    complaint = Complaint(
        "TEST002",
        "John Smith",
        "",#
        "Side effect",
        "Customer reports a rash",
        "Medium",
        "Unassigned",
        "Open",
        "18/11/2026",
        "Pending"
    )

    with pytest.raises(ValueError):
        ComplaintManager.add_complaint(complaint)

def test_empty_description_is_rejected():

    complaint = Complaint(
        "TEST002",
        "John Smith",
        "Paracetamol",
        "Side effect",
        "",#
        "Medium",
        "Unassigned",
        "Open",
        "18/11/2026",
        "Pending"
    )

    with pytest.raises(ValueError):
        ComplaintManager.add_complaint(complaint)

def test_empty_severity_is_rejected():

    complaint = Complaint(
        "TEST002",
        "John Smith",
        "Paracetamol",
        "Side effect",
        "Customer reports a rash",
        "",#
        "Unassigned",
        "Open",
        "18/11/2026",
        "Pending"
    )

    with pytest.raises(ValueError):
        ComplaintManager.add_complaint(complaint)

def test_valid_complaint_is_added():

    complaint = Complaint(
        "TEST006",
        "John Smith",
        "Paracetamol",
        "Side effect",
        "Customer reports a rash",
        "Medium",
        "Unassigned",
        "Open",
        "18/11/2026",
        "Pending"
    )

    ComplaintManager.add_complaint(complaint)
    df = ComplaintManager.get_all_complaints_df()
    assert "TEST006" in df["complaint_id"].values