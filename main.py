from database.database import init_db
import complaints.complaint
print(">>> COMPLAINT CLASS LOADED FROM:", complaints.complaint.__file__)

from database.database import init_db
from complaints.complaint_view import render_complaint_app


def main():
    init_db()

    render_complaint_app()

if __name__ == "__main__":
    main()