import base64
from email.mime.text import MIMEText


def create_draft(service, to, subject, body):
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft = {"message": {"raw": raw}}
    draft = service.users().drafts().create(userId="me", body=draft).execute()
    print("Draft Created Successfully")
