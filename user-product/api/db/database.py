import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Load environment variables from the .env file
load_dotenv()
DB_HOST = os.getenv("DATABASE_HOST")

DB_USER = os.environ.get("DATABASE_USERNAME")
DB_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DB_NAME = os.environ.get("DATABASE")
DATABASE_SOCKET = os.environ.get("DATABASE_SOCKET")
DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DATABASE_SOCKET}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
# Create a DeclarativeMeta instance
Base = declarative_base()
print("DB connected")
