"""
Adding account functions.
"""
import logging

from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import get_gsheet_id
from google_sheet.accounts import get_accounts, add_account
from server import bot
from keyboards import main_keyboard
from config import CREATOR


class AddingAccount(StatesGroup):
    name = State()
    amount = State()


# @delete_previous_message
async def adding_account_callback_handler(message_or_callback: Union[types.Message, types.CallbackQuery],
                                          state: FSMContext):
    """Starts adding account process."""
    user_id = message_or_callback.from_user.id
    gsheet_id = get_gsheet_id(user_id)

    account_names, accounts = get_accounts(gsheet_id=gsheet_id)

    async with state.proxy() as data:
        data["gsheet_id"] = gsheet_id
        data["account_names"] = account_names
        data["accounts"] = accounts

    await bot.send_message(
        user_id,
        "*Добавление счета*\n\nВведи название нового счета.",
        parse_mode="Markdown",
    )
    await AddingAccount.name.set()


async def get_account_name_handler(message: types.Message, state: FSMContext):
    """Gets account name from user."""
    account_name = message.text

    async with state.proxy() as data:
        account_names = data["account_names"]

    lowercase_account_names = list(map(lambda word: word.lower(), account_names))
    if account_name.lower() in lowercase_account_names:
        await message.answer("Счет с таким названием уже существует! Придумай другое!")
    else:
        async with state.proxy() as data:
            data["account_name"] = account_name

        await message.answer(
            "*Добавление счета*\n\nВведи сумму, которая лежит на счету.",
            parse_mode="Markdown",
        )
        await AddingAccount.amount.set()


async def get_amount_handler(message: types.Message, state: FSMContext):
    """Gets amount from user."""
    amount = message.text.replace(",", ".")

    num_points = amount.count(".")
    if num_points > 1:
        await message.answer(
            f"Ты можешь использовать *максимум один* символ `.`, но не {num_points}!",
            parse_mode="Markdown",
        )

    else:
        try:
            amount = float(amount)
        except ValueError:
            await message.answer("Введи, пожалуйста, *числовое* значение!", parse_mode="Markdown")
        else:
            async with state.proxy() as data:
                account_name = data["account_name"]
                accounts = data["accounts"]
                account_names = data["account_names"]

            try:
                add_account(
                    account_name,
                    amount,
                    accounts=accounts,
                    account_names=account_names,
                    gsheet_id=data["gsheet_id"],
                )
            except Exception as exc:
                logging.error("Excpetion during add_account executing!", exc_info=exc)
                await message.answer(
                    "*Ошибка!*\n\nНа моей стороне произошла ошибка. Если ты это читаешь, то "
                    f"напиши моему создателю: {CREATOR}. Он все починит)",
                    parse_mode="Markdown",
                    reply_markup=main_keyboard(),
                )

            else:
                await message.answer(
                    f"*Готово!*\n\nДобавлен новый аккаунт с именем: {account_name} "
                    f"и балансом: {amount}.",
                    parse_mode="Markdown",
                    reply_markup=main_keyboard(),
                )

            await state.finish()


def register_adding_account_handlers(dp: Dispatcher):
    """Register handlers for account adding."""
    dp.register_callback_query_handler(
        adding_account_callback_handler,
        lambda cb: cb.data == "add_account",
    )
    dp.register_message_handler(
        adding_account_callback_handler,
        commands=["add_account"],
    )

    dp.register_message_handler(
        get_account_name_handler,
        state=AddingAccount.name,
    )
    dp.register_message_handler(
        get_amount_handler,
        state=AddingAccount.amount,
    )
