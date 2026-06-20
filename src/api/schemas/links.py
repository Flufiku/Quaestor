from pydantic import BaseModel


class UserGroupLinkRequest(BaseModel):
    user_id: int
    group_id: int


class WithdrawalGroupLinkRequest(BaseModel):
    withdrawal_id: int
    group_id: int


class WithdrawalUserLinkRequest(BaseModel):
    withdrawal_id: int
    user_id: int
    paid: bool = False


class WithdrawalUserUpdateRequest(BaseModel):
    paid: bool


class WithdrawalTagLinkRequest(BaseModel):
    withdrawal_id: int
    tag_id: int