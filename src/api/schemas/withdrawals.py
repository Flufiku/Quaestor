from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class WithdrawalCreate(BaseModel):
    name: str
    description: str | None = None
    amount: Decimal


class WithdrawalUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    amount: Decimal | None = None


class WithdrawalRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    amount: Decimal
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
