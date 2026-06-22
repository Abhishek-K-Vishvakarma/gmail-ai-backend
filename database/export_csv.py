import pandas as pd

from database.db import SessionLocal
from database.models import EmailLog

db = SessionLocal()

emails = db.query(EmailLog).all()

data = []

for email in emails:

    data.append(
        {
            "Sender": email.sender,
            "Subject": email.subject,
            "Category": email.category,
            "Reply": email.reply,
        }
    )

df = pd.DataFrame(data)

df.to_csv("emails.csv", index=False)

print("emails.csv exported successfully")

db.close()
