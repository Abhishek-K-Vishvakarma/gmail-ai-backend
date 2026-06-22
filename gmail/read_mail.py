from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)

service = build("gmail", "v1", credentials=creds)

results = service.users().messages().list(userId="me", maxResults=5).execute()

messages = results.get("messages", [])

for msg in messages:

    email = service.users().messages().get(userId="me", id=msg["id"]).execute()

    headers = email["payload"]["headers"]

    sender = ""
    subject = ""

    for header in headers:
        if header["name"] == "From":
            sender = header["value"]

        if header["name"] == "Subject":
            subject = header["value"]

    print("\n========================")
    print("FROM :", sender)
    print("SUBJECT :", subject)
    print("SNIPPET :", email["snippet"])
