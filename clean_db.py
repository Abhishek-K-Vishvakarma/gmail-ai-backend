from database.db import SessionLocal
from database.models import EmailLog

db = SessionLocal()

KEYWORDS = [
    "otp",
    "verify",
    "verification",
    "webinar",
    "newsletter",
    "digest",
    "job alert",
    "weekly update",
    "daily update",
    "promotion",
    "offer",
    "discount",
]

emails = db.query(EmailLog).all()

deleted = 0

for email in emails:

    subject = (email.subject or "").lower()
    sender = (email.sender or "").lower()

    if any(keyword in subject for keyword in KEYWORDS):

        db.delete(email)
        deleted += 1
        continue

    if any(
        domain in sender
        for domain in [
            "linkedin",
            "indeed",
            "naukri",
            "internshala",
            "monster",
            "timesjobs",
            "pinterest",
            "instagram",
            "groww",
            "crio",
            "simplilearn",
            "snaphunt",
            "adobe",
        ]
    ):

        db.delete(email)
        deleted += 1

db.commit()

print(f"{deleted} emails deleted successfully")

db.close()
