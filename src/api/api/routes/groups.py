from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from models.entities import User
from repositories.group_repository import GroupRepository
from schemas.groups import GroupCreate, GroupRead, GroupUpdate


router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("", response_model=list[GroupRead])
def list_groups(db: Session = Depends(get_db)) -> list[GroupRead]:
    groups = GroupRepository(db).list()
    return [GroupRead.model_validate(group) for group in groups]


@router.get("/me", response_model=list[GroupRead])
def my_groups(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[GroupRead]:
    groups = GroupRepository(db).by_user(current_user.id)
    return [GroupRead.model_validate(group) for group in groups]


@router.get("/{group_id}", response_model=GroupRead)
def get_group(group_id: int, db: Session = Depends(get_db)) -> GroupRead:
    group = GroupRepository(db).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return GroupRead.model_validate(group)


@router.get("/by-user/{user_id}", response_model=list[GroupRead])
def groups_by_user(user_id: int, db: Session = Depends(get_db)) -> list[GroupRead]:
    groups = GroupRepository(db).by_user(user_id)
    return [GroupRead.model_validate(group) for group in groups]


@router.get("/by-deposit/{deposit_id}", response_model=list[GroupRead])
def groups_by_deposit(deposit_id: int, db: Session = Depends(get_db)) -> list[GroupRead]:
    groups = GroupRepository(db).by_deposit(deposit_id)
    return [GroupRead.model_validate(group) for group in groups]


@router.post("", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
def create_group(payload: GroupCreate, db: Session = Depends(get_db)) -> GroupRead:
    try:
        group = GroupRepository(db).create(payload.model_dump())
        return GroupRead.model_validate(group)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Group conflicts with existing data") from exc


@router.patch("/{group_id}", response_model=GroupRead)
def update_group(group_id: int, payload: GroupUpdate, db: Session = Depends(get_db)) -> GroupRead:
    repo = GroupRepository(db)
    group = repo.get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    try:
        updated = repo.update(group, payload.model_dump(exclude_unset=True))
        return GroupRead.model_validate(updated)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Group conflicts with existing data") from exc


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)) -> None:
    repo = GroupRepository(db)
    group = repo.get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    repo.delete(group)
