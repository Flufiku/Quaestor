from sqlalchemy import (
    BOOLEAN,
    DATETIME,
    DECIMAL,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from database.session import Base


users_groups = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
)

withdrawals_groups = Table(
    "withdrawals_groups",
    Base.metadata,
    Column(
        "withdrawal_id",
        Integer,
        ForeignKey("withdrawals.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("group_id", Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
)

withdrawals_tags = Table(
    "withdrawals_tags",
    Base.metadata,
    Column(
        "withdrawal_id",
        Integer,
        ForeignKey("withdrawals.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    privilege = Column(Integer, nullable=False, default=0)
    created_at = Column(DATETIME, server_default=func.current_timestamp())

    groups = relationship("Group", secondary=users_groups, back_populates="users")
    deposits = relationship("Deposit", back_populates="user", cascade="all, delete-orphan")
    withdrawal_links = relationship(
        "WithdrawalUser", back_populates="user", cascade="all, delete-orphan"
    )


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DATETIME, server_default=func.current_timestamp())

    users = relationship("User", secondary=users_groups, back_populates="groups")
    withdrawals = relationship("Withdrawal", secondary=withdrawals_groups, back_populates="groups")


class Deposit(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DATETIME, server_default=func.current_timestamp())

    user = relationship("User", back_populates="deposits")


class Withdrawal(Base):
    __tablename__ = "withdrawals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DATETIME, server_default=func.current_timestamp())

    groups = relationship("Group", secondary=withdrawals_groups, back_populates="withdrawals")
    tags = relationship("Tag", secondary=withdrawals_tags, back_populates="withdrawals")
    user_links = relationship(
        "WithdrawalUser", back_populates="withdrawal", cascade="all, delete-orphan"
    )


class WithdrawalUser(Base):
    __tablename__ = "withdrawals_users"

    withdrawal_id = Column(
        Integer,
        ForeignKey("withdrawals.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    paid = Column(BOOLEAN, nullable=False, default=False)

    withdrawal = relationship("Withdrawal", back_populates="user_links")
    user = relationship("User", back_populates="withdrawal_links")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    withdrawals = relationship("Withdrawal", secondary=withdrawals_tags, back_populates="tags")