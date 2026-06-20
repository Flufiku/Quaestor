from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from models.entities import User
from repositories.deposit_repository import DepositRepository
from schemas.deposits import DepositCreate, DepositRead, DepositUpdate


router = APIRouter(prefix="/deposits", tags=["deposits"])


@router.get("", response_model=list[DepositRead])
def list_deposits(db: Session = Depends(get_db)) -> list[DepositRead]:
    deposits = DepositRepository(db).list()
    return [DepositRead.model_validate(item) for item in deposits]


@router.get("/me", response_model=list[DepositRead])
def my_deposits(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[DepositRead]:
    deposits = DepositRepository(db).by_user(current_user.id)
    return [DepositRead.model_validate(item) for item in deposits]


@router.get("/{deposit_id}", response_model=DepositRead)
def get_deposit(deposit_id: int, db: Session = Depends(get_db)) -> DepositRead:
    deposit = DepositRepository(db).get(deposit_id)
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    return DepositRead.model_validate(deposit)


@router.get("/by-user/{user_id}", response_model=list[DepositRead])
def deposits_by_user(user_id: int, db: Session = Depends(get_db)) -> list[DepositRead]:
    deposits = DepositRepository(db).by_user(user_id)
    return [DepositRead.model_validate(item) for item in deposits]


@router.post("", response_model=DepositRead, status_code=status.HTTP_201_CREATED)
def create_deposit(payload: DepositCreate, db: Session = Depends(get_db)) -> DepositRead:
    try:
        deposit = DepositRepository(db).create(payload.model_dump())
        return DepositRead.model_validate(deposit)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Deposit conflicts with existing data") from exc


@router.patch("/{deposit_id}", response_model=DepositRead)
def update_deposit(deposit_id: int, payload: DepositUpdate, db: Session = Depends(get_db)) -> DepositRead:
    repo = DepositRepository(db)
    deposit = repo.get(deposit_id)
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")

    try:
        updated = repo.update(deposit, payload.model_dump(exclude_unset=True))
        return DepositRead.model_validate(updated)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Deposit conflicts with existing data") from exc


@router.delete("/{deposit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deposit(deposit_id: int, db: Session = Depends(get_db)) -> None:
    repo = DepositRepository(db)
    deposit = repo.get(deposit_id)
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    repo.delete(deposit)

