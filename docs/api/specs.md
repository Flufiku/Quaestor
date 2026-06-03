# API Specs and Planning

API: FastAPI and Uvicorn

## API Endpoints

## Login and Registration

- `POST /api/auth/register`: Register a new user.
- `POST /api/auth/login`: Authenticate a user and return a JWT token.

### Users

- `GET /api/users`: List users.
- `GET /api/users/{user_id}`: Get a single user by ID.
- `GET /api/users/{group_id}`: Get users in a group by group ID.
- `GET /api/users/{withdrawal_id}`: Get users in a withdrawal by withdrawal ID.
- `GET /api/users/me`: Get the authenticated user's profile.
- `POST /api/users`: Create a user.
- `PATCH /api/users/{user_id}`: Update part of a user.
- `DELETE /api/users/{user_id}`: Delete a user.

### Groups

- `GET /api/groups`: List groups.
- `GET /api/groups/{group_id}`: Get a single group by ID.
- `GET /api/groups/{user_id}`: Get groups that a user belongs to.
- `GET /api/groups/{deposit_id}`: Get groups associated with a deposit.
- `GET /api/groups/me`: Get the authenticated user's groups.
- `POST /api/groups`: Create a group.
- `PATCH /api/groups/{group_id}`: Update part of a group.
- `DELETE /api/groups/{group_id}`: Delete a group.

### Deposits

- `GET /api/deposits`: List deposits.
- `GET /api/deposits/{deposit_id}`: Get a single deposit by ID.
- `GET /api/deposits/{user_id}`: Get deposits made by a user by user ID.
- `GET /api/deposits/me`: Get the authenticated user's deposits.
- `POST /api/deposits`: Create a deposit.
- `PATCH /api/deposits/{deposit_id}`: Update part of a deposit.
- `DELETE /api/deposits/{deposit_id}`: Delete a deposit.

### Withdrawals

- `GET /api/withdrawals`: List withdrawals.
- `GET /api/withdrawals/{withdrawal_id}`: Get a single withdrawal by ID.
- `GET /api/withdrawals/{user_id}`: Get withdrawals made by a user by user ID.
- `GET /api/withdrawals/{group_id}`: Get withdrawals associated with a group by group ID.
- `GET /api/withdrawals/me`: Get the authenticated user's withdrawals.
- `POST /api/withdrawals`: Create a withdrawal.
- `PATCH /api/withdrawals/{withdrawal_id}`: Update part of a withdrawal.
- `DELETE /api/withdrawals/{withdrawal_id}`: Delete a withdrawal.
- `POST /api/withdrawals/me/pay/{withdrawal_id}`: Pay a withdrawal for the authenticated user.