from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DepositCreate(BaseModel):
    user_id: int
    amount: Decimal


class DepositUpdate(BaseModel):
    user_id: int | None = None
    amount: Decimal | None = None


class DepositRead(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)