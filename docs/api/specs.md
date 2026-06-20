# API Specs and Planning

API: FastAPI and Uvicorn

## API Endpoints

### Login and Registration

- `POST /api/auth/register`: Register a new user.
- `POST /api/auth/login`: Authenticate a user and return a JWT token.

### Users

- `GET /api/users`: List users.
- `GET /api/users/me`: Get the authenticated user's profile.
- `GET /api/users/{user_id}`: Get a single user by ID.
- `GET /api/users/by-group/{group_id}`: Get users in a group by group ID.
- `GET /api/users/by-withdrawal/{withdrawal_id}`: Get users in a withdrawal by withdrawal ID.
- `POST /api/users`: Create a user.
- `PATCH /api/users/{user_id}`: Update part of a user.
- `DELETE /api/users/{user_id}`: Delete a user.

### Groups

- `GET /api/groups`: List groups.
- `GET /api/groups/me`: Get the authenticated user's groups.
- `GET /api/groups/{group_id}`: Get a single group by ID.
- `GET /api/groups/by-user/{user_id}`: Get groups that a user belongs to.
- `GET /api/groups/by-deposit/{deposit_id}`: Get groups associated with a deposit.
- `POST /api/groups`: Create a group.
- `PATCH /api/groups/{group_id}`: Update part of a group.
- `DELETE /api/groups/{group_id}`: Delete a group.

### Deposits

- `GET /api/deposits`: List deposits.
- `GET /api/deposits/me`: Get the authenticated user's deposits.
- `GET /api/deposits/{deposit_id}`: Get a single deposit by ID.
- `GET /api/deposits/by-user/{user_id}`: Get deposits made by a user by user ID.
- `POST /api/deposits`: Create a deposit.
- `PATCH /api/deposits/{deposit_id}`: Update part of a deposit.
- `DELETE /api/deposits/{deposit_id}`: Delete a deposit.

### Withdrawals

- `GET /api/withdrawals`: List withdrawals.
- `GET /api/withdrawals/me`: Get the authenticated user's withdrawals.
- `GET /api/withdrawals/{withdrawal_id}`: Get a single withdrawal by ID.
- `GET /api/withdrawals/by-user/{user_id}`: Get withdrawals made by a user by user ID.
- `GET /api/withdrawals/by-group/{group_id}`: Get withdrawals associated with a group by group ID.
- `GET /api/withdrawals/by-tag/{tag_id}`: Get withdrawals associated with a tag by tag ID.
- `POST /api/withdrawals`: Create a withdrawal.
- `PATCH /api/withdrawals/{withdrawal_id}`: Update part of a withdrawal.
- `DELETE /api/withdrawals/{withdrawal_id}`: Delete a withdrawal.
- `POST /api/withdrawals/{withdrawal_id}/pay/{user_id}`: Pay a withdrawal for a specific user.

### Tags

- `GET /api/tags`: List tags.
- `GET /api/tags/{tag_id}`: Get a single tag by ID.
- `GET /api/tags/by-withdrawal/{withdrawal_id}`: Get tags associated with a withdrawal by withdrawal ID.
- `POST /api/tags`: Create a tag.
- `PATCH /api/tags/{tag_id}`: Update part of a tag.
- `DELETE /api/tags/{tag_id}`: Delete a tag.

### Linking

#### User-Group Linking
- `POST /api/link/user-group`: Link a user to a group.
- `DELETE /api/link/user-group`: Unlink a user from a group.

#### Withdrawal-Group Linking
- `POST /api/link/withdrawal-group`: Link a withdrawal to a group, and also all users of a group.
- `DELETE /api/link/withdrawal-group`: Unlink a withdrawal from a group, and also all users of a group.

#### Withdrawal-User Linking
- `POST /api/link/withdrawal-user`: Link a withdrawal to a user (unpaid by default).
- `PATCH /api/link/withdrawal-user/{withdrawal_user_id}`: Update the status of a withdrawal for a user (e.g., mark as paid).
- `DELETE /api/link/withdrawal-user`: Unlink a withdrawal from a user.

#### Withdrawal-Tag Linking
- `POST /api/link/withdrawal-tag`: Link a withdrawal to a tag.
- `DELETE /api/link/withdrawal-tag`: Unlink a withdrawal from a tag.