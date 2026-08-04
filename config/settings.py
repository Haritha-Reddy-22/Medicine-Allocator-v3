from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Project Root Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Application
APP_NAME = os.getenv(
    "APP_NAME",
    "Medicine Allocator"
)

APP_ENV = os.getenv(
    "APP_ENV",
    "development"
)

# Security
SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

# Database
DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "medicine_allocator.db"
)

DATABASE_PATH = BASE_DIR / "data" / DATABASE_NAME

# AI
GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)