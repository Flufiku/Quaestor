from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories.link_repository import LinkRepository
from schemas.links import (
    UserGroupLinkRequest,
    WithdrawalGroupLinkRequest,
    WithdrawalTagLinkRequest,
    WithdrawalUserLinkRequest,
    WithdrawalUserUpdateRequest,
)


router = APIRouter(prefix="/link", tags=["links"])


@router.post("/user-group", status_code=status.HTTP_204_NO_CONTENT)
def link_user_group(payload: UserGroupLinkRequest, db: Session = Depends(get_db)) -> None:
    try:
        LinkRepository(db).link_user_group(payload.user_id, payload.group_id)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Invalid or duplicate user-group link") from exc


@router.delete("/user-group", status_code=status.HTTP_204_NO_CONTENT)
def unlink_user_group(payload: UserGroupLinkRequest, db: Session = Depends(get_db)) -> None:
    LinkRepository(db).unlink_user_group(payload.user_id, payload.group_id)


@router.post("/withdrawal-group", status_code=status.HTTP_204_NO_CONTENT)
def link_withdrawal_group(payload: WithdrawalGroupLinkRequest, db: Session = Depends(get_db)) -> None:
    try:
        LinkRepository(db).link_withdrawal_group(payload.withdrawal_id, payload.group_id)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Invalid or duplicate withdrawal-group link") from exc


@router.delete("/withdrawal-group", status_code=status.HTTP_204_NO_CONTENT)
def unlink_withdrawal_group(payload: WithdrawalGroupLinkRequest, db: Session = Depends(get_db)) -> None:
    LinkRepository(db).unlink_withdrawal_group(payload.withdrawal_id, payload.group_id)


@router.post("/withdrawal-user", status_code=status.HTTP_204_NO_CONTENT)
def link_withdrawal_user(payload: WithdrawalUserLinkRequest, db: Session = Depends(get_db)) -> None:
    try:
        LinkRepository(db).link_withdrawal_user(payload.withdrawal_id, payload.user_id, payload.paid)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Invalid withdrawal-user link") from exc


@router.patch("/withdrawal-user/{withdrawal_user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_withdrawal_user_status(
    withdrawal_user_id: int,
    payload: WithdrawalUserUpdateRequest,
    db: Session = Depends(get_db),
) -> None:
    success = LinkRepository(db).update_withdrawal_user_by_rowid(withdrawal_user_id, payload.paid)
    if not success:
        raise HTTPException(status_code=404, detail="Withdrawal-user link not found")


@router.delete("/withdrawal-user", status_code=status.HTTP_204_NO_CONTENT)
def unlink_withdrawal_user(payload: WithdrawalUserLinkRequest, db: Session = Depends(get_db)) -> None:
    LinkRepository(db).unlink_withdrawal_user(payload.withdrawal_id, payload.user_id)


@router.post("/withdrawal-tag", status_code=status.HTTP_204_NO_CONTENT)
def link_withdrawal_tag(payload: WithdrawalTagLinkRequest, db: Session = Depends(get_db)) -> None:
    try:
        LinkRepository(db).link_withdrawal_tag(payload.withdrawal_id, payload.tag_id)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Invalid or duplicate withdrawal-tag link") from exc


@router.delete("/withdrawal-tag", status_code=status.HTTP_204_NO_CONTENT)
def unlink_withdrawal_tag(payload: WithdrawalTagLinkRequest, db: Session = Depends(get_db)) -> None:
    LinkRepository(db).unlink_withdrawal_tag(payload.withdrawal_id, payload.tag_id)