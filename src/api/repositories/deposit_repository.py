from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.entities import Deposit


class DepositRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Deposit]:
        return list(self.db.scalars(select(Deposit).order_by(Deposit.id)).all())

    def get(self, deposit_id: int) -> Deposit | None:
        return self.db.get(Deposit, deposit_id)

    def by_user(self, user_id: int) -> list[Deposit]:
        statement = select(Deposit).where(Deposit.user_id == user_id).order_by(Deposit.id)
        return list(self.db.scalars(statement).all())

    def create(self, payload: dict) -> Deposit:
        deposit = Deposit(**payload)
        self.db.add(deposit)
        self.db.commit()
        self.db.refresh(deposit)
        return deposit

    def update(self, deposit: Deposit, payload: dict) -> Deposit:
        for key, value in payload.items():
            setattr(deposit, key, value)
        self.db.commit()
        self.db.refresh(deposit)
        return deposit

    def delete(self, deposit: Deposit) -> None:
        self.db.delete(deposit)
        self.db.commit()
