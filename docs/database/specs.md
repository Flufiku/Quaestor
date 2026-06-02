# Database Specs and Planning

Database: SQLite


## Database Schema

```
TABLE users {
  id INTEGER PRIMARY KEY AUTOINCREMENT
  firstname TEXT NOT NULL UNIQUE
  lastname TEXT NOT NULL UNIQUE
  username TEXT NOT NULL UNIQUE
  password_hash TEXT NOT NULL
  privilege INTEGER NOT NULL DEFAULT 0
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
}

TABLE groups {
  id INTEGER PRIMARY KEY AUTOINCREMENT
  name TEXT NOT NULL UNIQUE
  description TEXT
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
}

TABLE users_groups {
  user_id INTEGER NOT NULL
  group_id INTEGER NOT NULL
  PRIMARY KEY (user_id, group_id)
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
  FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE
}

TABLE deposits {
  id INTEGER PRIMARY KEY AUTOINCREMENT
  user_id INTEGER NOT NULL
  amount DECIMAL(10, 2) NOT NULL
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
}

TABLE withdrawals {
  id INTEGER PRIMARY KEY AUTOINCREMENT
  name TEXT NOT NULL
  description TEXT
  amount DECIMAL(10, 2) NOT NULL
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
}

TABLE withdrawals_groups {
  withdrawal_id INTEGER NOT NULL
  group_id INTEGER NOT NULL
  PRIMARY KEY (withdrawal_id, group_id)
  FOREIGN KEY (withdrawal_id) REFERENCES withdrawals(id) ON DELETE CASCADE
  FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE
}

TABLE withdrawals_users {
  withdrawal_id INTEGER NOT NULL
  user_id INTEGER NOT NULL
  paid BOOLEAN NOT NULL DEFAULT 0
  PRIMARY KEY (withdrawal_id, user_id)
  FOREIGN KEY (withdrawal_id) REFERENCES withdrawals(id) ON DELETE CASCADE
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
}
```
