from datetime import datetime, timedelta, timezone
from jose import jwt
from pwdlib import PasswordHash
from app.core.config import settings


datetime.now(timezone.utc)

timedelta(minutes=30)

settings.SECRET_KEY
