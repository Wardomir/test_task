import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Nylas API configuration with environment variable support
NYLAS_BASE_URL = os.environ.get("NYLAS_BASE_URL", "http://15.204.46.122:8056")
NYLAS_AUTH_ENDPOINT = f"{NYLAS_BASE_URL}/mock-nylas/auth/token"
NYLAS_MESSAGES_ENDPOINT = f"{NYLAS_BASE_URL}/mock-nylas/messages"
NYLAS_CLIENT_ID = os.environ.get("NYLAS_CLIENT_ID", "valid_client")
NYLAS_CLIENT_SECRET = os.environ.get("NYLAS_CLIENT_SECRET", "valid_secret")

# Database configuration with environment variable support
DB_HOST = os.environ.get("DB_HOST", "15.204.46.122")
DB_PORT = int(os.environ.get("DB_PORT", "5435"))
DB_NAME = os.environ.get("DB_NAME", "testdb")
DB_USER = os.environ.get("DB_USER", "testuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "testpass")
DB_TABLE = os.environ.get("DB_TABLE", "nylas_messages")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"