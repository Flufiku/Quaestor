from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories.tag_repository import TagRepository
from schemas.tags import TagCreate, TagRead, TagUpdate


router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=list[TagRead])
def list_tags(db: Session = Depends(get_db)) -> list[TagRead]:
    tags = TagRepository(db).list()
    return [TagRead.model_validate(tag) for tag in tags]


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(tag_id: int, db: Session = Depends(get_db)) -> TagRead:
    tag = TagRepository(db).get(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagRead.model_validate(tag)


@router.get("/by-withdrawal/{withdrawal_id}", response_model=list[TagRead])
def tags_by_withdrawal(withdrawal_id: int, db: Session = Depends(get_db)) -> list[TagRead]:
    tags = TagRepository(db).by_withdrawal(withdrawal_id)
    return [TagRead.model_validate(tag) for tag in tags]


@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)) -> TagRead:
    try:
        tag = TagRepository(db).create(payload.model_dump())
        return TagRead.model_validate(tag)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Tag already exists") from exc


@router.patch("/{tag_id}", response_model=TagRead)
def update_tag(tag_id: int, payload: TagUpdate, db: Session = Depends(get_db)) -> TagRead:
    repo = TagRepository(db)
    tag = repo.get(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    try:
        updated = repo.update(tag, payload.model_dump(exclude_unset=True))
        return TagRead.model_validate(updated)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Tag already exists") from exc


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db)) -> None:
    repo = TagRepository(db)
    tag = repo.get(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    repo.delete(tag)