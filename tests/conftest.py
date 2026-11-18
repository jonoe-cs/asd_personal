
import pytest

from database.database import init_db
from complaints.complaint_manager import ComplaintManager


@pytest.fixture(autouse=True)
def use_test_database(tmp_path):

    # Create a separate temporary database
    test_db = tmp_path / "test_pharmacy.db"

    # Initialise its complaints table
    init_db(test_db)

    # Tell ComplaintManager to use this database
    ComplaintManager.set_database(test_db)

    yield

    # Reset to the normal database afterwards
    ComplaintManager.set_database(None)
