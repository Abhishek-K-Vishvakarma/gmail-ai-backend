import re

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from ai.classify_email import classify_email
from ai.generate_reply import generate_reply
from ai.detect_priority import detect_priority
from ai.ignore_email import is_ignore_email
from ai.summarize_email import summarize_email

from gmail.create_draft import create_draft
from gmail.email_utils import get_email_body
from gmail.gmail_labels import get_or_create_label

from database.save_email import save_email
from database.db import SessionLocal
from database.models import EmailLog

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build("gmail", "v1", credentials=creds)

results = (
    service.users()
    .messages()
    .list(userId="me", labelIds=["UNREAD"], maxResults=10)
    .execute()
)

messages = results.get("messages", [])

if not messages:
    print("No unread emails found")
    exit()

blocked_domains = [
    "indeed",
    "linkedin",
    "naukri",
    "internshala",
    "monster",
    "timesjobs",
    "crio",
    "pinterest",
    "snaphunt",
    "adobe",
    "simplilearn",
]

for msg in messages:
    try:
        msg_id = msg["id"]

        # ── Get Email ─────────────────────────────────────────────────────────
        email = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="full")
            .execute()
        )

        headers = email["payload"]["headers"]
        sender = ""
        subject = ""

        for header in headers:
            if header["name"] == "From":
                sender = header["value"]
            elif header["name"] == "Subject":
                subject = header["value"]

        # ── Blocked Newsletter Senders ────────────────────────────────────────
        if any(domain in sender.lower() for domain in blocked_domains):
            print(f"\nSkipping Newsletter: {sender}")
            service.users().messages().modify(
                userId="me",
                id=msg_id,
                body={"removeLabelIds": ["UNREAD"]},
            ).execute()
            continue

        # ── Extract Sender Email ──────────────────────────────────────────────
        match = re.search(r"<(.+?)>", sender)
        sender_email = match.group(1) if match else sender

        # ── Get Email Body ────────────────────────────────────────────────────
        email_text = get_email_body(email["payload"])
        if not email_text:
            email_text = email.get("snippet", "")

        # ── Ignore Check ──────────────────────────────────────────────────────
        if is_ignore_email(subject, sender_email, email_text):
            print("\nIgnored Email")
            service.users().messages().modify(
                userId="me",
                id=msg_id,
                body={"removeLabelIds": ["UNREAD"]},
            ).execute()
            continue

        # ── Classification ────────────────────────────────────────────────────
        category = classify_email(
            email_text=email_text,
            subject=subject,
            sender=sender_email,
        )

        # ── Priority ──────────────────────────────────────────────────────────
        priority = detect_priority(
            email_text=email_text,
            category=category,
        )

        # ── Summary ───────────────────────────────────────────────────────────
        summary = summarize_email(email_text)

        print("\n===================================")
        print("FROM:", sender_email)
        print("SUBJECT:", subject)
        print("CATEGORY:", category)
        print("PRIORITY:", priority)
        print("SUMMARY:", summary)
        print("\nEMAIL:")
        print(email_text[:500])

        # ── Skip IGNORE category ──────────────────────────────────────────────
        if category == "IGNORE":
            print("\nIgnoring System Email")
            service.users().messages().modify(
                userId="me",
                id=msg_id,
                body={"removeLabelIds": ["UNREAD"]},
            ).execute()
            continue

        # ── Skip NEWSLETTER category ──────────────────────────────────────────
        if category == "NEWSLETTER":
            print("\nAI Classified as Newsletter")
            service.users().messages().modify(
                userId="me",
                id=msg_id,
                body={"removeLabelIds": ["UNREAD"]},
            ).execute()
            continue

        # ── Generate Reply ────────────────────────────────────────────────────
        print("\nGenerating Reply...\n")
        reply = generate_reply(email_text, category)

        if reply == "SKIP_EMAIL":
            print("AI skipped this email")
            service.users().messages().modify(
                userId="me",
                id=msg_id,
                body={"removeLabelIds": ["UNREAD"]},
            ).execute()
            continue

        if reply == "AI_ERROR":
            print("AI quota exceeded or API failed. Draft NOT created.")
            continue

        print(reply)

        # ── Duplicate Check Before Draft ──────────────────────────────────────
        db = SessionLocal()
        try:
            existing = db.query(EmailLog).filter(EmailLog.gmail_id == msg_id).first()
            if existing and existing.reply:
                print("\nEmail already processed. Skipping draft creation.")
                service.users().messages().modify(
                    userId="me",
                    id=msg_id,
                    body={"removeLabelIds": ["UNREAD"]},
                ).execute()
                continue
        finally:
            db.close()

        # ── Create Draft ──────────────────────────────────────────────────────
        create_draft(
            service=service,
            to=sender_email,
            subject=f"Re: {subject}",
            body=reply,
        )
        print("Draft Created Successfully")

        # ── Save To Database ──────────────────────────────────────────────────
        save_email(
            gmail_id=msg_id,
            sender=sender_email,
            subject=subject,
            category=category,
            priority=priority,
            summary=summary,
            reply=reply,
        )
        print("Email Saved Successfully")

        # ── Gmail Labels ──────────────────────────────────────────────────────
        label_id = get_or_create_label(service, category)
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"addLabelIds": [label_id]},
        ).execute()
        print(f"{category} Label Added")

        # ── Mark as Read ──────────────────────────────────────────────────────
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"]},
        ).execute()
        print("Email marked as read")

    except Exception as e:
        print(f"\nError Processing Email: {e}")
