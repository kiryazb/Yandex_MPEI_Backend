"""
Renaming account functions.
"""
import logging

from typing import Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from google_sheet.accounts import get_accounts, rename_account
from database import get_gsheet_id
from keyboards import list_items_keyboard, main_keyboard
from server import bot
from config import CREATOR


class RenameAccount(StatesGroup):
    account_name = State()
    new_account_name = State()


# @delete_previous_message
async def rename_account_callback_handler(message_or_call_query: Union[types.Message, types.CallbackQuery],
                                          state: FSMContext):
    """Renames account."""
    user_id = message_or_call_query.from_user.id
    gsheet_id = get_gsheet_id(user_id)

    account_names, accounts = get_accounts(gsheet_id=gsheet_id)

    if len(account_names) == 0:
        await bot.send_message(
            user_id,
            "*Переименовывать нечего!* Ты не создал еще ни одного счета! "
            "Чтобы его создать, введи /add_account",
            reply_markup=main_keyboard()
        )

    else:
        async with state.proxy() as data:
            data["gsheet_id"] = gsheet_id
            data["accounts"] = accounts
            data["account_names"] = account_names

        await bot.send_message(
            user_id,
            "*Изменение названия счета*\n\nВыбери из списка ниже счет, нозвание которого ты хочешь изменить.",
            parse_mode="Markdown",
            reply_markup=list_items_keyboard(sorted(account_names)),
        )
        await RenameAccount.account_name.set()


async def get_account_name_handler(message: types.Message, state: FSMContext):
    """Gets account name from user."""
    account_name = message.text.lower()

    async with state.proxy() as data:
        account_names = data["account_names"]

    if account_name in map(lambda word: word.lower(), account_names):
        async with state.proxy() as data:
            data["account_name"] = account_name

        await message.answer(
            f"*Изменение названия счета*\n\nВведи новое название счета.",
            parse_mode="Markdown",
        )
        await RenameAccount.new_account_name.set()

    else:
        await message.answer(
            "Упс!\nЯ такого счета не знаю! Похоже, что ты ошибся в названии. Попробуй еще раз!",
            parse_mode="Markdown",
            reply_markup=list_items_keyboard(sorted(account_names)),
        )


async def get_new_account_name_handler(message: types.Message, state: FSMContext):
    """Gets new account name from user."""
    new_name = message.text

    async with state.proxy() as data:
        account_names = data["account_names"]

    if new_name.lower() in map(lambda word: word.lower(), account_names):
        await message.answer(
            f"Счет с именем: {new_name} уже *существует!* Придумай другое название!",
            parse_mode="Markdown",
        )

    else:
        async with state.proxy() as data:
            name = data["account_name"]
            gsheet_id = data["gsheet_id"]

        try:
            rename_account(
                name,
                new_name,
                account_names=account_names,
                gsheet_id=gsheet_id,
            )
        except Exception as exc:
            logging.error("Excpetion during rename_account executing!", exc_info=exc)
            await message.answer(
                "*Ошибка!*\n\nНа моей стороне произошла ошибка. Если ты это читаешь, то "
                f"напиши моему создателю: {CREATOR}. Он все починит)",
                parse_mode="Markdown",
                reply_markup=main_keyboard(),
            )

        else:
            await message.answer(
                f"*Готово!*\n\nАккаунт с именем {name} переименован в {new_name}!",
                parse_mode="Markdown",
                reply_markup=main_keyboard(),
            )

        await state.finish()


def register_rename_account_handlers(dp: Dispatcher):
    """Registers handlers for rename account."""
    dp.register_callback_query_handler(
        rename_account_callback_handler,
        lambda cb: cb.data == "rename_account",
    )
    dp.register_message_handler(
        rename_account_callback_handler,
        commands=["change_amount"],
    )

    dp.register_message_handler(
        get_account_name_handler,
        state=RenameAccount.account_name,
    )
    dp.register_message_handler(
        get_new_account_name_handler,
        state=RenameAccount.new_account_name,
    )
