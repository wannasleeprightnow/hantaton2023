CREATE TABLE user(
    id INTEGER primary key AUTOINCREMENT,
    telegram_user_id INTEGER UNIQUE,
    is_admin BOOLEAN DEFAULT=False
);