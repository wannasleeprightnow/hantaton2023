ADD_USER = """INSERT INTO user
(telegram_user_id)
VALUES (?)"""
GET_USERS = "SELECT telegram_user_id FROM user"
