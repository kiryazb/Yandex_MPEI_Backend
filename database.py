"""
This file contains all necessary tools for working with finance.db
"""
import sqlite3

con = sqlite3.connect("finance.db")
cursor = con.cursor()


class User:
    """Represents user"""
    def __init__(self, user_id: int, gsheet_id: str = ""):
        self.user_id = user_id
        self.gsheet_id = gsheet_id


def add_user(user_id: int, gsheet_id: str = "") -> User:
    """
    Add new user to user table

    :param user_id: telegram ID of the user
    :param gsheet_id: ID of the Google sheet
    :return: User
    """
    cursor.execute(f"INSERT INTO user VALUES ({user_id}, {gsheet_id!r})")
    con.commit()

    return User(user_id)


def update_gsheet_id(user_id: int, gsheet_id: str) -> User:
    """
    Add/update google_sheet_id field in the database

    :param user_id: telegram ID of the user
    :param gsheet_id: ID of the Google sheet
    """
    cursor.execute(
        f"UPDATE user SET google_sheet_id={gsheet_id!r} "
        f"WHERE id={user_id}"
    )
    con.commit()

    return User(user_id, gsheet_id)


def get_gsheet_id(user_id: int) -> str:
    """
    Returns user's Google sheet ID.

    :param user_id: Telegram ID of the user.
    """
    _, gsheet_id = list(cursor.execute(f"SELECT * FROM user WHERE id={user_id}"))[0]
    return gsheet_id


def get_user(user_id: int) -> User:
    """
    Gets user from the database by user_id

    :param user_id: telegram ID of the user
    :return: User
    :raise ValueError: if user with user_id does not exist in database
    """
    try:
        user = list(cursor.execute(f"SELECT * FROM user WHERE id={user_id}"))[0]
    except IndexError:
        raise ValueError("User does not exists in database!")

    return User(user_id=user[0], gsheet_id=user[1])


def get_or_add_user(user_id: int) -> User:
    """
    Gets and returns user by user_id if it exists
    in database otherwise adds a new user.

    :param int user_id: Telegram ID of the user
    :return: User
    """
    try:
        user = get_user(user_id)
    except ValueError:
        user = add_user(user_id)

    return user
