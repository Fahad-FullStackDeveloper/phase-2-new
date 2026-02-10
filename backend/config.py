import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")