import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import SessionLocal
from database.models import EmailLog

db = SessionLocal()

total = db.query(EmailLog).count()

job_count = db.query(EmailLog).filter(EmailLog.category == "JOB").count()

interview_count = db.query(EmailLog).filter(EmailLog.category == "INTERVIEW").count()

client_count = db.query(EmailLog).filter(EmailLog.category == "CLIENT").count()

meeting_count = db.query(EmailLog).filter(EmailLog.category == "MEETING").count()

general_count = db.query(EmailLog).filter(EmailLog.category == "GENERAL").count()

print("\n===== EMAIL ANALYTICS =====\n")

print("Total Emails :", total)
print("JOB :", job_count)
print("INTERVIEW :", interview_count)
print("CLIENT :", client_count)
print("MEETING :", meeting_count)
print("GENERAL :", general_count)

db.close()
