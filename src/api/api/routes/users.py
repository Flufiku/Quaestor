from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from models.entities import User
from repositories.user_repository import UserRepository
from schemas.users import UserCreate, UserRead, UserUpdate
from services.auth_service import hash_password


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)) -> list[UserRead]:
    users = UserRepository(db).list()
    return [UserRead.model_validate(user) for user in users]


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserRead:
    user = UserRepository(db).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.get("/by-group/{group_id}", response_model=list[UserRead])
def users_by_group(group_id: int, db: Session = Depends(get_db)) -> list[UserRead]:
    users = UserRepository(db).by_group(group_id)
    return [UserRead.model_validate(user) for user in users]


@router.get("/by-withdrawal/{withdrawal_id}", response_model=list[UserRead])
def users_by_withdrawal(withdrawal_id: int, db: Session = Depends(get_db)) -> list[UserRead]:
    users = UserRepository(db).by_withdrawal(withdrawal_id)
    return [UserRead.model_validate(user) for user in users]


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    repo = UserRepository(db)
    try:
        user = repo.create(
            {
                "firstname": payload.firstname,
                "lastname": payload.lastname,
                "username": payload.username,
                "password_hash": hash_password(payload.password),
                "privilege": payload.privilege,
            }
        )
        return UserRead.model_validate(user)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="User conflicts with existing data") from exc


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)) -> UserRead:
    repo = UserRepository(db)
    user = repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    values = payload.model_dump(exclude_unset=True)
    if "password" in values:
        values["password_hash"] = hash_password(values.pop("password"))

    try:
        updated = repo.update(user, values)
        return UserRead.model_validate(updated)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="User conflicts with existing data") from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    repo = UserRepository(db)
    user = repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    repo.delete(user)