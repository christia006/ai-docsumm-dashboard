from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Konfigurasi DB Anda
DB_CONFIG = {
    "dbname": "neurosordb",
    "user": "neurosord_user",
    "password": "Sayabag",
    "host": "localhost", # <-- Pastikan ini 'localhost'
    "port": "5432"
}

# Membuat URL database dari DB_CONFIG
# postgresql://user:password@host:port/dbname
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)

# Atau, jika Anda menggunakan variabel lingkungan di file .env:
# SQLALCHEMY_DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     (f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
#      f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")
# )


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
