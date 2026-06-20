from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str
    privilege: int = 0


class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    password: str | None = None
    privilege: int | None = None


class UserRead(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    privilege: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
