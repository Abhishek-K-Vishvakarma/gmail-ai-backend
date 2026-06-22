from database.db import SessionLocal
from database.models import EmailLog

db = SessionLocal()

emails = db.query(EmailLog).all()

for email in emails:

    print("\n-------------------")
    print("Sender:", email.sender)
    print("Subject:", email.subject)
    print("Category:", email.category)
    print("Reply:", email.reply)

db.close()
