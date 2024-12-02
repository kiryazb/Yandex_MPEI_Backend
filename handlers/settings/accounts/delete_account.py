"""
Functions for deleting account.
"""
import logging

from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from server import bot
from database import get_gsheet_id
from google_sheet.accounts import get_accounts, delete_account
from keyboards import main_keyboard, list_items_keyboard
from config import CREATOR


class DeleteAccount(StatesGroup):
    name = State()


async def delete_account_callback_handler(message_or_call_query: Union[types.Message, types.CallbackQuery],
                                          state: FSMContext):
    """Starts deleting account process."""
    user_id = message_or_call_query.from_user.id
    gsheet_id = get_gsheet_id(user_id)

    account_names, accounts = get_accounts(gsheet_id=gsheet_id)

    if len(account_names) == 0:
        await bot.send_message(
            user_id,
            "*Удалять нечего!* Ты не создал еще ни одного счета! "
            "Чтобы его создать, введи /add_account",
            reply_markup=main_keyboard()
        )

    else:
        async with state.proxy() as data:
            data["gsheet_id"] = gsheet_id
            data["account_names"] = account_names

        await bot.send_message(
            user_id,
            "*Удаление счета*\n\nВыбери из списка ниже счет, который ты хочешь удалить.",
            parse_mode="Markdown",
            reply_markup=list_items_keyboard(sorted(account_names)),
        )
        await DeleteAccount.name.set()


async def get_account_name_handler(message: types.Message, state: FSMContext):
    """Gets and deletes account."""
    name = message.text

    async with state.proxy() as data:
        account_names = data["account_names"]
        gsheet_id = data["gsheet_id"]

    if name.lower() not in map(lambda word: word.lower(), account_names):
        await message.answer(
            "Упс!\nЯ такого счета не знаю! Похоже, что ты ошибся в названии. Попробуй еще раз!",
            parse_mode="Markdown",
            reply_markup=list_items_keyboard(sorted(account_names)),
        )

    else:
        try:
            delete_account(name, account_names=account_names, gsheet_id=gsheet_id)
        except Exception as exc:
            logging.error("Excpetion during delete_account executing!", exc_info=exc)
            await message.answer(
                "*Ошибка!*\n\nНа моей стороне произошла ошибка. Если ты это читаешь, то "
                f"напиши моему создателю: {CREATOR}. Он все починит)",
                parse_mode="Markdown",
                reply_markup=main_keyboard(),
            )
        else:
            await message.answer(
                f"*Готово!*\n\nАккаунт с именем {name} успешно удален!",
                parse_mode="Markdown",
                reply_markup=main_keyboard(),
            )

        await state.finish()


def register_delete_account_handlers(dp: Dispatcher):
    """Registers functions for deleting account."""
    dp.register_message_handler(
        delete_account_callback_handler,
        commands=["delete_account"],
    )
    dp.register_callback_query_handler(
        delete_account_callback_handler,
        lambda cb: cb.data == "delete_account",
    )
    dp.register_message_handler(
        get_account_name_handler,
        state=DeleteAccount.name,
    )
