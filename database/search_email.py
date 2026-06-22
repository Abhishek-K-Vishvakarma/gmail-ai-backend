import sys

from database.db import SessionLocal
from database.models import EmailLog

db = SessionLocal()

if len(sys.argv) < 2:
    print("Usage: python -m search.search_email interview")
    exit()

keyword = sys.argv[1].lower()

emails = db.query(EmailLog).all()

print("\n===== SEARCH RESULTS =====\n")

found = False

for email in emails:

    if (
        keyword in email.subject.lower()
        or keyword in email.sender.lower()
        or keyword in email.category.lower()
    ):

        found = True

        print("-" * 50)
        print("Sender :", email.sender)
        print("Subject :", email.subject)
        print("Category :", email.category)

if not found:
    print("No emails found")

db.close()
