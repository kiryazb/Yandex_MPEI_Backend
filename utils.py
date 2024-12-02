import functools
import typing
import gspread

from aiogram import types

from server import bot
from database import get_user


def auth(func):
    """Checks is user logged in."""
    @functools.wraps(func)
    async def wrapper(message_or_callback: typing.Union[types.Message, types.CallbackQuery], *args, **kwargs):
        is_logged_in = True
        try:
            user = get_user(message_or_callback.from_user.id)
        except ValueError:
            is_logged_in = False
        else:
            if user.gsheet_id == "":
                is_logged_in = False

        if is_logged_in:
            await func(message_or_callback, *args, **kwargs)
        else:
            await bot.send_message(message_or_callback.from_user.id,
                                   "😐 Сначала подключи меня к таблице командой /register, "
                                   "а потом используй все мои возможности.")

    return wrapper


def delete_previous_message(func):
    """This decorator delets previous message"""
    @functools.wraps(func)
    async def wrapper(callback_or_message: typing.Union[types.CallbackQuery, types.Message], *args, **kwargs):
        if type(callback_or_message) == types.CallbackQuery:
            callback = callback_or_message
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            return await func(callback, *args, **kwargs)

        elif type(callback_or_message) == types.Message:
            message = callback_or_message
            await bot.delete_message(message.from_user.id, message.message_id)
            return await func(message, *args, **kwargs)

        else:
            raise ValueError(f"'callback_or_message' must be types.CallbackQuery "
                             f"or types.Message but not {type(callback_or_message)}!")

    return wrapper


def is_gsheet_id_correct(gsheet_id: str) -> bool:
    """Checks that user's Google sheet ID is correct"""
    service_account = gspread.service_account(filename="google_token.json")
    try:
        service_account.open_by_key(gsheet_id)
    except gspread.exceptions.APIError:
        return False
    except gspread.exceptions.NoValidUrlKeyFound:
        return False

    return True
