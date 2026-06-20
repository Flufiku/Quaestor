from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.entities import (
    Tag,
    Withdrawal,
    WithdrawalUser,
    withdrawals_groups,
    withdrawals_tags,
)


class WithdrawalRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Withdrawal]:
        return list(self.db.scalars(select(Withdrawal).order_by(Withdrawal.id)).all())

    def get(self, withdrawal_id: int) -> Withdrawal | None:
        return self.db.get(Withdrawal, withdrawal_id)

    def by_user(self, user_id: int) -> list[Withdrawal]:
        statement = (
            select(Withdrawal)
            .join(WithdrawalUser, WithdrawalUser.withdrawal_id == Withdrawal.id)
            .where(WithdrawalUser.user_id == user_id)
            .order_by(Withdrawal.id)
        )
        return list(self.db.scalars(statement).all())

    def by_group(self, group_id: int) -> list[Withdrawal]:
        statement = (
            select(Withdrawal)
            .join(withdrawals_groups, withdrawals_groups.c.withdrawal_id == Withdrawal.id)
            .where(withdrawals_groups.c.group_id == group_id)
            .order_by(Withdrawal.id)
        )
        return list(self.db.scalars(statement).all())

    def by_tag(self, tag_id: int) -> list[Withdrawal]:
        statement = (
            select(Withdrawal)
            .join(withdrawals_tags, withdrawals_tags.c.withdrawal_id == Withdrawal.id)
            .where(withdrawals_tags.c.tag_id == tag_id)
            .order_by(Withdrawal.id)
        )
        return list(self.db.scalars(statement).all())

    def create(self, payload: dict) -> Withdrawal:
        withdrawal = Withdrawal(**payload)
        self.db.add(withdrawal)
        self.db.commit()
        self.db.refresh(withdrawal)
        return withdrawal

    def update(self, withdrawal: Withdrawal, payload: dict) -> Withdrawal:
        for key, value in payload.items():
            setattr(withdrawal, key, value)
        self.db.commit()
        self.db.refresh(withdrawal)
        return withdrawal

    def delete(self, withdrawal: Withdrawal) -> None:
        self.db.delete(withdrawal)
        self.db.commit()

    def mark_paid(self, withdrawal_id: int, user_id: int, paid: bool = True) -> bool:
        link = self.db.get(WithdrawalUser, {"withdrawal_id": withdrawal_id, "user_id": user_id})
        if not link:
            return False
        link.paid = paid
        self.db.commit()
        return True