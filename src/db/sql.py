ADD_USER = """INSERT INTO user
(telegram_user_id)
VALUES (?)"""

ADD_ADMIN = """UPDATE user
(is_admin)
VALUES true
WHERE telegram_user_id=?"""

GET_USERS = "SELECT telegram_user_id FROM user"

GET_ADMINS = """SELECT telegram_user_id FROM user
WHERE is_admin=true"""
