from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class EmailLog(Base):

    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)

    gmail_id = Column(String, unique=True)

    sender = Column(String)

    subject = Column(String)

    category = Column(String)

    priority = Column(String)

    summary = Column(Text)

    reply = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
