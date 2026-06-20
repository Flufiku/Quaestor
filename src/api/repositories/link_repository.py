from __future__ import annotations

from sqlalchemy import delete, insert, select, text
from sqlalchemy.orm import Session

from models.entities import (
    Group,
    User,
    Withdrawal,
    WithdrawalUser,
    users_groups,
    withdrawals_groups,
    withdrawals_tags,
)


class LinkRepository:
    def __init__(self, db: Session):
        self.db = db

    def link_user_group(self, user_id: int, group_id: int) -> None:
        statement = insert(users_groups).values(user_id=user_id, group_id=group_id)
        self.db.execute(statement)
        self.db.commit()

    def unlink_user_group(self, user_id: int, group_id: int) -> None:
        statement = delete(users_groups).where(
            users_groups.c.user_id == user_id,
            users_groups.c.group_id == group_id,
        )
        self.db.execute(statement)
        self.db.commit()

    def link_withdrawal_group(self, withdrawal_id: int, group_id: int) -> None:
        self.db.execute(
            insert(withdrawals_groups).values(withdrawal_id=withdrawal_id, group_id=group_id)
        )

        user_ids = self.db.scalars(
            select(users_groups.c.user_id).where(users_groups.c.group_id == group_id)
        ).all()
        for user_id in user_ids:
            if not self.db.get(WithdrawalUser, {"withdrawal_id": withdrawal_id, "user_id": user_id}):
                self.db.add(WithdrawalUser(withdrawal_id=withdrawal_id, user_id=user_id, paid=False))
        self.db.commit()

    def unlink_withdrawal_group(self, withdrawal_id: int, group_id: int) -> None:
        self.db.execute(
            delete(withdrawals_groups).where(
                withdrawals_groups.c.withdrawal_id == withdrawal_id,
                withdrawals_groups.c.group_id == group_id,
            )
        )
        user_ids = self.db.scalars(
            select(users_groups.c.user_id).where(users_groups.c.group_id == group_id)
        ).all()
        for user_id in user_ids:
            self.db.execute(
                delete(WithdrawalUser).where(
                    WithdrawalUser.withdrawal_id == withdrawal_id,
                    WithdrawalUser.user_id == user_id,
                )
            )
        self.db.commit()

    def link_withdrawal_user(self, withdrawal_id: int, user_id: int, paid: bool = False) -> None:
        if not self.db.get(WithdrawalUser, {"withdrawal_id": withdrawal_id, "user_id": user_id}):
            self.db.add(WithdrawalUser(withdrawal_id=withdrawal_id, user_id=user_id, paid=paid))
            self.db.commit()

    def update_withdrawal_user_by_rowid(self, rowid: int, paid: bool) -> bool:
        row = self.db.execute(
            text("SELECT rowid, withdrawal_id, user_id FROM withdrawals_users WHERE rowid = :rowid"),
            {"rowid": rowid},
        ).mappings().first()
        if not row:
            return False

        self.db.execute(
            text(
                "UPDATE withdrawals_users SET paid = :paid "
                "WHERE withdrawal_id = :withdrawal_id AND user_id = :user_id"
            ),
            {
                "paid": 1 if paid else 0,
                "withdrawal_id": row["withdrawal_id"],
                "user_id": row["user_id"],
            },
        )
        self.db.commit()
        return True

    def unlink_withdrawal_user(self, withdrawal_id: int, user_id: int) -> None:
        self.db.execute(
            delete(WithdrawalUser).where(
                WithdrawalUser.withdrawal_id == withdrawal_id,
                WithdrawalUser.user_id == user_id,
            )
        )
        self.db.commit()

    def link_withdrawal_tag(self, withdrawal_id: int, tag_id: int) -> None:
        self.db.execute(insert(withdrawals_tags).values(withdrawal_id=withdrawal_id, tag_id=tag_id))
        self.db.commit()

    def unlink_withdrawal_tag(self, withdrawal_id: int, tag_id: int) -> None:
        self.db.execute(
            delete(withdrawals_tags).where(
                withdrawals_tags.c.withdrawal_id == withdrawal_id,
                withdrawals_tags.c.tag_id == tag_id,
            )
        )
        self.db.commit()