from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.session import SessionLocal
from repositories.user_repository import UserRepository
from services.auth_service import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	credentials_error = HTTPException(status_code=401, detail="Invalid authentication credentials")
	try:
		payload = decode_access_token(token)
		user_id = int(payload.get("sub", "0"))
	except (ValueError, TypeError):
		raise credentials_error

	user = UserRepository(db).get(user_id)
	if not user:
		raise credentials_error
	return user

