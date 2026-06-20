from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.entities import Deposit, Group, User, users_groups, withdrawals_groups


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Group]:
        return list(self.db.scalars(select(Group).order_by(Group.id)).all())

    def get(self, group_id: int) -> Group | None:
        return self.db.get(Group, group_id)

    def by_user(self, user_id: int) -> list[Group]:
        statement = (
            select(Group)
            .join(users_groups, users_groups.c.group_id == Group.id)
            .where(users_groups.c.user_id == user_id)
            .order_by(Group.id)
        )
        return list(self.db.scalars(statement).all())

    def by_deposit(self, deposit_id: int) -> list[Group]:
        statement = (
            select(Group)
            .join(users_groups, users_groups.c.group_id == Group.id)
            .join(User, User.id == users_groups.c.user_id)
            .join(Deposit, Deposit.user_id == User.id)
            .where(Deposit.id == deposit_id)
            .order_by(Group.id)
        )
        return list(self.db.scalars(statement).all())

    def by_withdrawal(self, withdrawal_id: int) -> list[Group]:
        statement = (
            select(Group)
            .join(withdrawals_groups, withdrawals_groups.c.group_id == Group.id)
            .where(withdrawals_groups.c.withdrawal_id == withdrawal_id)
            .order_by(Group.id)
        )
        return list(self.db.scalars(statement).all())

    def create(self, payload: dict) -> Group:
        group = Group(**payload)
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def update(self, group: Group, payload: dict) -> Group:
        for key, value in payload.items():
            setattr(group, key, value)
        self.db.commit()
        self.db.refresh(group)
        return group

    def delete(self, group: Group) -> None:
        self.db.delete(group)
        self.db.commit()