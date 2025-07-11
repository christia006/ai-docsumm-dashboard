from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import endpoints
from .db.database import Base, engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Buat tabel database jika belum ada
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Document Summarizer API",
    description="API for summarizing legal, financial, and insurance documents using AI.",
    version="1.0.0",
)

# Konfigurasi CORS (Penting untuk Frontend)
# Sesuaikan `allow_origins` dengan URL frontend Anda saat deploy
origins = [
    "http://localhost:3000",  # Untuk development frontend React
    # "http://your-frontend-domain.com", # Tambahkan domain frontend Anda di sini
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api/v1", tags=["documents"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Document Summarizer API!"}