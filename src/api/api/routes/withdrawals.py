from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from models.entities import User
from repositories.withdrawal_repository import WithdrawalRepository
from schemas.links import WithdrawalUserUpdateRequest
from schemas.withdrawals import WithdrawalCreate, WithdrawalRead, WithdrawalUpdate


router = APIRouter(prefix="/withdrawals", tags=["withdrawals"])


@router.get("", response_model=list[WithdrawalRead])
def list_withdrawals(db: Session = Depends(get_db)) -> list[WithdrawalRead]:
    items = WithdrawalRepository(db).list()
    return [WithdrawalRead.model_validate(item) for item in items]


@router.get("/me", response_model=list[WithdrawalRead])
def my_withdrawals(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[WithdrawalRead]:
    items = WithdrawalRepository(db).by_user(current_user.id)
    return [WithdrawalRead.model_validate(item) for item in items]


@router.get("/{withdrawal_id}", response_model=WithdrawalRead)
def get_withdrawal(withdrawal_id: int, db: Session = Depends(get_db)) -> WithdrawalRead:
    withdrawal = WithdrawalRepository(db).get(withdrawal_id)
    if not withdrawal:
        raise HTTPException(status_code=404, detail="Withdrawal not found")
    return WithdrawalRead.model_validate(withdrawal)


@router.get("/by-user/{user_id}", response_model=list[WithdrawalRead])
def withdrawals_by_user(user_id: int, db: Session = Depends(get_db)) -> list[WithdrawalRead]:
    items = WithdrawalRepository(db).by_user(user_id)
    return [WithdrawalRead.model_validate(item) for item in items]


@router.get("/by-group/{group_id}", response_model=list[WithdrawalRead])
def withdrawals_by_group(group_id: int, db: Session = Depends(get_db)) -> list[WithdrawalRead]:
    items = WithdrawalRepository(db).by_group(group_id)
    return [WithdrawalRead.model_validate(item) for item in items]


@router.get("/by-tag/{tag_id}", response_model=list[WithdrawalRead])
def withdrawals_by_tag(tag_id: int, db: Session = Depends(get_db)) -> list[WithdrawalRead]:
    items = WithdrawalRepository(db).by_tag(tag_id)
    return [WithdrawalRead.model_validate(item) for item in items]


@router.post("", response_model=WithdrawalRead, status_code=status.HTTP_201_CREATED)
def create_withdrawal(payload: WithdrawalCreate, db: Session = Depends(get_db)) -> WithdrawalRead:
    try:
        item = WithdrawalRepository(db).create(payload.model_dump())
        return WithdrawalRead.model_validate(item)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Withdrawal conflicts with existing data") from exc


@router.patch("/{withdrawal_id}", response_model=WithdrawalRead)
def update_withdrawal(
    withdrawal_id: int, payload: WithdrawalUpdate, db: Session = Depends(get_db)
) -> WithdrawalRead:
    repo = WithdrawalRepository(db)
    withdrawal = repo.get(withdrawal_id)
    if not withdrawal:
        raise HTTPException(status_code=404, detail="Withdrawal not found")

    try:
        updated = repo.update(withdrawal, payload.model_dump(exclude_unset=True))
        return WithdrawalRead.model_validate(updated)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Withdrawal conflicts with existing data") from exc


@router.delete("/{withdrawal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_withdrawal(withdrawal_id: int, db: Session = Depends(get_db)) -> None:
    repo = WithdrawalRepository(db)
    withdrawal = repo.get(withdrawal_id)
    if not withdrawal:
        raise HTTPException(status_code=404, detail="Withdrawal not found")
    repo.delete(withdrawal)


@router.post("/{withdrawal_id}/pay/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def pay_withdrawal_for_user(
    withdrawal_id: int,
    user_id: int,
    payload: WithdrawalUserUpdateRequest,
    db: Session = Depends(get_db),
) -> None:
    success = WithdrawalRepository(db).mark_paid(withdrawal_id, user_id, paid=payload.paid)
    if not success:
        raise HTTPException(status_code=404, detail="Withdrawal assignment not found")