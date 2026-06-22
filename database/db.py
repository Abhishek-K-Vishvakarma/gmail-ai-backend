# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///emails.db"

# engine = create_engine(DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Render persistent disk path ya local
if os.path.exists("/data"):
    DATABASE_URL = "sqlite:////data/emails.db"
else:
    DATABASE_URL = "sqlite:///emails.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
