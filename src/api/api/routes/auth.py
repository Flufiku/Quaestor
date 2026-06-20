from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories.user_repository import UserRepository
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from schemas.users import UserRead
from services.auth_service import create_access_token, hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserRead:
    users = UserRepository(db)
    existing = users.get_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")

    user = users.create(
        {
            "firstname": payload.firstname,
            "lastname": payload.lastname,
            "username": payload.username,
            "password_hash": hash_password(payload.password),
            "privilege": payload.privilege,
        }
    )
    return UserRead.model_validate(user)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    users = UserRepository(db)
    user = users.get_by_username(payload.username)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)
