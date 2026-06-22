import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import SessionLocal
from database.models import EmailLog

db = SessionLocal()

emails = db.query(EmailLog).all()

print("\n===== EMAIL REPORT =====\n")

for email in emails:

    print("-" * 50)

    print("Sender :", email.sender)
    print("Subject :", email.subject)
    print("Category :", email.category)
    print("Priority :", email.priority)
    print("Created :", email.created_at)

db.close()
