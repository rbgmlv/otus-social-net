import bcrypt
import jwt
import uuid
from datetime import datetime, timedelta, timezone
from config import Config


def hash_password(password: str) -> str:
    """Хэширование пароля."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Провека пароля по хэшу."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def generate_token(user_id: str) -> str:
    """Генерация JWT-токена."""
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=24),
        'iat': datetime.now(timezone.utc),
        'jti': str(uuid.uuid4())
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')


def generate_user_id() -> str:
    """Генерация уникального идентификатора пользователя."""
    return str(uuid.uuid4())
