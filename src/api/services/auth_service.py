import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone


JWT_SECRET = os.getenv("QUAESTOR_JWT_SECRET", "change-me-in-production")
JWT_ALGO = "HS256"
JWT_EXP_MINUTES = int(os.getenv("QUAESTOR_JWT_EXPIRE_MINUTES", "60"))


def hash_password(password: str) -> str:
    iterations = 100000
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    value = base64.urlsafe_b64encode(salt + digest).decode("ascii")
    return f"pbkdf2_sha256${iterations}${value}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, iteration_text, value = stored.split("$", 2)
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iteration_text)
        raw = base64.urlsafe_b64decode(value.encode("ascii"))
        salt, original_digest = raw[:16], raw[16:]
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(digest, original_digest)
    except (ValueError, TypeError):
        return False


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    now = datetime.now(timezone.utc)
    expire_delta = timedelta(minutes=expires_minutes or JWT_EXP_MINUTES)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + expire_delta).timestamp()),
    }
    return _encode_jwt(payload)


def decode_access_token(token: str) -> dict:
    header_b64, payload_b64, signature_b64 = token.split(".")
    message = f"{header_b64}.{payload_b64}".encode("ascii")
    expected_signature = _sign(message)
    actual_signature = _urlsafe_b64decode(signature_b64)

    if not hmac.compare_digest(expected_signature, actual_signature):
        raise ValueError("Invalid token signature")

    payload = json.loads(_urlsafe_b64decode(payload_b64).decode("utf-8"))
    if "exp" not in payload or int(payload["exp"]) < int(datetime.now(timezone.utc).timestamp()):
        raise ValueError("Token expired")
    return payload


def _encode_jwt(payload: dict) -> str:
    if JWT_ALGO != "HS256":
        raise ValueError("Unsupported JWT algorithm")

    header = {"alg": JWT_ALGO, "typ": "JWT"}
    header_b64 = _urlsafe_b64encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    )
    message = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = _urlsafe_b64encode(_sign(message))
    return f"{header_b64}.{payload_b64}.{signature}"


def _sign(message: bytes) -> bytes:
    return hmac.new(JWT_SECRET.encode("utf-8"), message, hashlib.sha256).digest()


def _urlsafe_b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _urlsafe_b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))
