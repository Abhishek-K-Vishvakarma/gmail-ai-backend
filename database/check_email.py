from database.db import SessionLocal
from database.models import EmailLog


def email_exists(gmail_id):

    db = SessionLocal()

    try:

        email = db.query(EmailLog).filter(EmailLog.gmail_id == gmail_id).first()

        return email is not None

    finally:
        db.close()
