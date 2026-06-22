from collections import Counter

from database.db import SessionLocal
from database.models import EmailLog

db = SessionLocal()

emails = db.query(EmailLog).all()

print("\n========== EMAIL ANALYTICS ==========\n")

print("Total Emails:", len(emails))

# Category Count
categories = Counter()

for email in emails:
    categories[email.category] += 1

print("\nCategory Wise:")

for category, count in categories.items():
    print(f"{category}: {count}")

# Top Senders
senders = Counter()

for email in emails:
    senders[email.sender] += 1

print("\nTop Senders:")

for sender, count in senders.most_common(10):
    print(f"{sender} -> {count}")

db.close()
