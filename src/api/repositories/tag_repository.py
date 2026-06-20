from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.entities import Tag, Withdrawal, withdrawals_tags


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Tag]:
        return list(self.db.scalars(select(Tag).order_by(Tag.id)).all())

    def get(self, tag_id: int) -> Tag | None:
        return self.db.get(Tag, tag_id)

    def by_withdrawal(self, withdrawal_id: int) -> list[Tag]:
        statement = (
            select(Tag)
            .join(withdrawals_tags, withdrawals_tags.c.tag_id == Tag.id)
            .where(withdrawals_tags.c.withdrawal_id == withdrawal_id)
            .order_by(Tag.id)
        )
        return list(self.db.scalars(statement).all())

    def create(self, payload: dict) -> Tag:
        tag = Tag(**payload)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def update(self, tag: Tag, payload: dict) -> Tag:
        for key, value in payload.items():
            setattr(tag, key, value)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def delete(self, tag: Tag) -> None:
        self.db.delete(tag)
        self.db.commit()