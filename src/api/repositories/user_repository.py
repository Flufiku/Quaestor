from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.entities import User, Withdrawal, WithdrawalUser, users_groups


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[User]:
        return list(self.db.scalars(select(User).order_by(User.id)).all())

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        return self.db.scalar(select(User).where(User.username == username))

    def by_group(self, group_id: int) -> list[User]:
        statement = (
            select(User)
            .join(users_groups, users_groups.c.user_id == User.id)
            .where(users_groups.c.group_id == group_id)
            .order_by(User.id)
        )
        return list(self.db.scalars(statement).all())

    def by_withdrawal(self, withdrawal_id: int) -> list[User]:
        statement = (
            select(User)
            .join(WithdrawalUser, WithdrawalUser.user_id == User.id)
            .where(WithdrawalUser.withdrawal_id == withdrawal_id)
            .order_by(User.id)
        )
        return list(self.db.scalars(statement).all())

    def create(self, payload: dict) -> User:
        user = User(**payload)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, payload: dict) -> User:
        for key, value in payload.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
        