from database.database import init_db
from complaint.complaint_view import render_complaint_app


def main():
    init_db()

    render_complaint_app()

if __name__ == "__main__":
    main()