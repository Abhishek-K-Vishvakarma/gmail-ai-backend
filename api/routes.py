import base64
import email as email_lib
from email.mime.text import MIMEText

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from database.db import SessionLocal
from database.models import EmailLog
from ai.classify_email import classify_email
from ai.detect_priority import detect_priority
from ai.summarize_email import summarize_email
from ai.generate_reply import generate_reply


class ApiKeyRequest(BaseModel):
    api_key: str
    model: str


class DraftRequest(BaseModel):
    to: str
    subject: str
    body: str
    gmail_id: str = ""
    category: str = "GENERAL"
    priority: str = "LOW"


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
]


def get_gmail_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("gmail", "v1", credentials=creds)


# ── GET EMAILS ────────────────────────────────────────────────────────────────
@app.get("/emails")
def get_emails():
    try:
        service = get_gmail_service()
        results = (
            service.users()
            .messages()
            .list(userId="me", maxResults=50, labelIds=["INBOX"])
            .execute()
        )
        messages = results.get("messages", [])

        # Load already saved emails from DB
        db = SessionLocal()
        saved = {e.gmail_id: e for e in db.query(EmailLog).all()}
        db.close()

        emails = []
        for msg in messages:
            gmail_id = msg["id"]

            # If already in DB, return from DB (faster, has category/priority)
            if gmail_id in saved:
                e = saved[gmail_id]
                emails.append(
                    {
                        "id": e.id,
                        "gmail_id": e.gmail_id,
                        "sender": e.sender,
                        "subject": e.subject,
                        "summary": e.summary,
                        "preview": e.summary,
                        "category": (e.category or "GENERAL").upper(),
                        "priority": (e.priority or "LOW").upper(),
                        "read": True,
                        "replied": bool(e.reply),
                        "reply": e.reply or "",
                        "date": "Today",
                        "time": (
                            e.created_at.strftime("%I:%M %p") if e.created_at else ""
                        ),
                    }
                )
                continue

            # New email — fetch full details
            full = (
                service.users()
                .messages()
                .get(userId="me", id=gmail_id, format="full")
                .execute()
            )

            headers = full["payload"]["headers"]
            sender = next(
                (h["value"] for h in headers if h["name"] == "From"), "Unknown"
            )
            subject = next(
                (h["value"] for h in headers if h["name"] == "Subject"), "No Subject"
            )
            date_str = next((h["value"] for h in headers if h["name"] == "Date"), "")
            snippet = full.get("snippet", "")
            label_ids = full.get("labelIds", [])
            is_unread = "UNREAD" in label_ids

            # Extract body text
            body_text = snippet
            try:
                parts = full["payload"].get("parts", [])
                for part in parts:
                    if part["mimeType"] == "text/plain":
                        data = part["body"].get("data", "")
                        body_text = base64.urlsafe_b64decode(data).decode(
                            "utf-8", errors="ignore"
                        )
                        break
            except Exception:
                pass

            # AI classify + priority + summary
            category = classify_email(body_text, subject=subject, sender=sender)
            priority = detect_priority(body_text, category=category)
            summary = summarize_email(body_text)

            # Skip IGNORE emails
            if category == "IGNORE":
                continue

            # Save to DB
            db = SessionLocal()
            try:
                new_email = EmailLog(
                    gmail_id=gmail_id,
                    sender=sender,
                    subject=subject,
                    category=category,
                    priority=priority,
                    summary=summary,
                    reply="",
                )
                db.add(new_email)
                db.commit()
                db.refresh(new_email)
                db_id = new_email.id
            except Exception:
                db.rollback()
                db_id = gmail_id
            finally:
                db.close()

            emails.append(
                {
                    "id": db_id,
                    "gmail_id": gmail_id,
                    "sender": sender,
                    "subject": subject,
                    "summary": summary,
                    "preview": snippet,
                    "category": category.upper(),
                    "priority": priority.upper(),
                    "read": not is_unread,
                    "replied": False,
                    "reply": "",
                    "date": "Today",
                    "time": "",
                }
            )

        return emails

    except Exception as e:
        print("Error fetching emails:", e)
        return []


# ── CREATE DRAFT ──────────────────────────────────────────────────────────────
@app.post("/create-draft")
def create_draft(data: DraftRequest):
    try:
        service = get_gmail_service()

        # 1. Create draft
        message = MIMEText(data.body)
        message["to"] = data.to
        message["subject"] = data.subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        draft = (
            service.users()
            .drafts()
            .create(userId="me", body={"message": {"raw": raw}})
            .execute()
        )

        # 2. Mark original email as read + add labels
        if data.gmail_id:
            try:
                # Get or create category label
                cat = data.category.upper()
                pri = data.priority.upper()

                # Fetch existing labels
                all_labels = (
                    service.users()
                    .labels()
                    .list(userId="me")
                    .execute()
                    .get("labels", [])
                )
                label_map = {l["name"]: l["id"] for l in all_labels}

                add_label_ids = []

                # Category label
                if cat not in label_map:
                    new_label = (
                        service.users()
                        .labels()
                        .create(
                            userId="me",
                            body={
                                "name": cat,
                                "labelListVisibility": "labelShow",
                                "messageListVisibility": "show",
                            },
                        )
                        .execute()
                    )
                    add_label_ids.append(new_label["id"])
                else:
                    add_label_ids.append(label_map[cat])

                # Priority label
                pri_label_name = f"PRIORITY/{pri}"
                if pri_label_name not in label_map:
                    new_pri = (
                        service.users()
                        .labels()
                        .create(
                            userId="me",
                            body={
                                "name": pri_label_name,
                                "labelListVisibility": "labelShow",
                                "messageListVisibility": "show",
                            },
                        )
                        .execute()
                    )
                    add_label_ids.append(new_pri["id"])
                else:
                    add_label_ids.append(label_map[pri_label_name])

                # Apply labels + mark as read (remove UNREAD)
                service.users().messages().modify(
                    userId="me",
                    id=data.gmail_id,
                    body={"addLabelIds": add_label_ids, "removeLabelIds": ["UNREAD"]},
                ).execute()

            except Exception as label_err:
                print("Label/Read Error:", label_err)

        return {"success": True, "draft_id": draft["id"], "message": "Draft created!"}

    except Exception as e:
        print("Draft Error:", e)
        return {"success": False, "message": str(e)}


# ── SEND EMAIL ────────────────────────────────────────────────────────────────
@app.post("/send-email")
def send_email(data: DraftRequest):
    try:
        service = get_gmail_service()

        message = MIMEText(data.body)
        message["to"] = data.to
        message["subject"] = data.subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        sent = service.users().messages().send(userId="me", body={"raw": raw}).execute()

        return {"success": True, "message_id": sent["id"], "message": "Email sent!"}

    except Exception as e:
        print("Send Error:", e)
        return {"success": False, "message": str(e)}


# ── GENERATE AI REPLY ─────────────────────────────────────────────────────────
@app.post("/generate-reply")
def get_ai_reply(data: dict):
    try:
        email_text = data.get("email_text", "")
        category = data.get("category", "GENERAL")
        gmail_id = data.get("gmail_id", "")

        # Fetch full email body if needed
        if gmail_id and len(email_text.strip()) < 100:
            try:
                service = get_gmail_service()

                full = (
                    service.users()
                    .messages()
                    .get(userId="me", id=gmail_id, format="full")
                    .execute()
                )

                parts = full.get("payload", {}).get("parts", [])

                for part in parts:
                    if part.get("mimeType") == "text/plain":
                        raw = part.get("body", {}).get("data", "")
                        if raw:
                            email_text = base64.urlsafe_b64decode(raw).decode(
                                "utf-8",
                                errors="ignore",
                            )
                            break

                if not email_text:
                    email_text = full.get("snippet", "")

            except Exception as fe:
                print("Full body fetch error:", fe)

        # Generate reply
        reply = generate_reply(email_text, category)

        # If Gemini quota exceeded or email skipped
        if not reply or reply == "SKIP_EMAIL":
            return {
                "success": False,
                "reply": "",
                "message": "AI reply not available",
            }

        return {
            "success": True,
            "reply": reply,
        }

    except Exception as e:
        print("Generate Reply Error:", e)

        return {
            "success": False,
            "reply": "",
            "message": str(e),
        }


# ── SAVE API KEY ──────────────────────────────────────────────────────────────
@app.post("/save-api-key")
def save_api_key(data: ApiKeyRequest):
    try:
        # Read existing .env
        with open(".env", "r") as f:
            lines = f.readlines()

        # Update or add keys
        new_lines = []
        found_key = False
        found_model = False
        for line in lines:
            if line.startswith("GEMINI_API_KEY="):
                new_lines.append(f"GEMINI_API_KEY={data.api_key}\n")
                found_key = True
            elif line.startswith("GEMINI_MODEL="):
                new_lines.append(f"GEMINI_MODEL={data.model}\n")
                found_model = True
            else:
                new_lines.append(line)

        if not found_key:
            new_lines.append(f"GEMINI_API_KEY={data.api_key}\n")
        if not found_model:
            new_lines.append(f"GEMINI_MODEL={data.model}\n")

        with open(".env", "w") as f:
            f.writelines(new_lines)

        return {"success": True, "message": "API Key Saved Successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}
