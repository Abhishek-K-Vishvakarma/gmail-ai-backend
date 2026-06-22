from database.db import SessionLocal
from database.models import EmailLog


def save_email(
    gmail_id,
    sender,
    subject,
    category,
    priority,
    summary,
    reply,
):

    print("Saving Email To Database...")

    db = SessionLocal()

    try:

        # Check if email already exists
        existing_email = (
            db.query(EmailLog).filter(EmailLog.gmail_id == gmail_id).first()
        )

        if existing_email:

            print("Email already exists. Updating record...")

            existing_email.sender = sender
            existing_email.subject = subject
            existing_email.category = category
            existing_email.priority = priority
            existing_email.summary = summary

            # Update reply only if new reply exists
            if reply and reply != "SKIP_EMAIL":
                existing_email.reply = reply

            db.commit()

            print("Email Updated Successfully")
            return existing_email

        # New Email
        email = EmailLog(
            gmail_id=gmail_id,
            sender=sender,
            subject=subject,
            category=category,
            priority=priority,
            summary=summary,
            reply=reply,
        )

        db.add(email)
        db.commit()
        db.refresh(email)

        print("Email Saved Successfully")
        return email

    except Exception as e:

        db.rollback()
        print("Database Error:", e)

    finally:
        db.close()
