"""
File with expence control handlers.
"""
from typing import Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from server import bot
from database import get_gsheet_id
from keyboards import list_items_keyboard, main_keyboard
from utils import auth

from google_sheet.categories import get_categories, service_account
from google_sheet.accounts import get_accounts
from google_sheet.expenses import add_expense, get_total_expenses


class AddsExpense(StatesGroup):
    amount = State()
    category = State()
    account = State()
    comment = State()


@auth
async def add_expense_handler_callback(message_or_call_query: Union[types.Message, types.CallbackQuery],
                                       state: FSMContext):
    """Launches adding expense."""
    user_id = message_or_call_query.from_user.id

    await bot.send_message(
        user_id,
        "*Добавление расхода*\n\nНапиши и отправь мне сумму, которую ты потратил\n\n"
        "Чтобы прервать добавление расходов напиши *отмена*.",
        parse_mode="Markdown",
    )
    await AddsExpense.amount.set()

    async with state.proxy() as data:
        if data.get("gsheet_id") is None:
            gsheet_id = get_gsheet_id(user_id)
            sheet = service_account.open_by_key(gsheet_id)

            settings_worksheet = sheet.worksheet("Настройки")
            transactions_worksheet = sheet.worksheet("Транзакции")

            data["gsheet_id"] = gsheet_id
            data["categories"] = get_categories(settings_worksheet)["expense"]
            data["account_names"], data["accounts"] = get_accounts(settings_worksheet)
            data["total_expenses"] = get_total_expenses(transactions_worksheet)


async def get_amount_handler(message: types.Message, state: FSMContext):
    """Gets amount from user."""
    amount = message.text
    try:
        amount = float(amount)
    except ValueError:
        await message.answer("Введи числовое значение!")
    else:
        async with state.proxy() as data:
            data["amount"] = amount
            categories = data["categories"]

        if len(categories) == 0:
            await message.answer(
                "Похоже, что ты еще не добавил ни одной категории расходов.\n"
                "Чтобы ее добавить, введи команду /add_category"
            )
            await state.finish()

        else:
            await message.answer(
                "Теперь выбери категорию расходов из списка под твоей клавиатурой.\n\n",
                reply_markup=list_items_keyboard(sorted(categories)),
            )
            await AddsExpense.category.set()


async def get_category_handler(message: types.Message, state: FSMContext):
    """Gets category type from user."""
    category = message.text

    async with state.proxy() as data:
        categories = data["categories"]

    if category.lower() not in map(lambda word: word.lower(), categories):
        await message.answer(
            "Я не знаю такой категории, попробуй ввести ее еще раз!",
            reply_markup=list_items_keyboard(sorted(categories)),
        )

    else:
        async with state.proxy() as data:
            data["category"] = category
            account_names = data["account_names"]

        if len(account_names) == 0:
            await message.answer(
                "Ты не создал еще ни одного счета! Чтобы его создать, введи /add_account",
                reply_markup=main_keyboard(),
            )
            await state.finish()

        else:
            await message.answer(
                "Выбери из списка под клавиатурой счет, с которого была совершена покупка.",
                reply_markup=list_items_keyboard(sorted(account_names))
            )
            await AddsExpense.account.set()


async def get_account_handler(message: types.Message, state: FSMContext):
    """Gets user's account name."""
    account = message.text

    async with state.proxy() as data:
        account_names = data["account_names"]

    if account.lower() not in map(lambda word: word.lower(), account_names):
        await message.answer(
            "Я не знаю такого счета, попробуй ввести его еще раз!",
            reply_markup=list_items_keyboard(account_names)
        )

    else:
        async with state.proxy() as data:
            data["account"] = account

        await AddsExpense.comment.set()

        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("Пропустить", callback_data="finish_expense"))

        await message.answer(
            "Ок! Также ты можешь добавить описание к своей покупке."
            "Для этого напиши его в поле ввода и отправь его мне. Если ты "
            "не хочешь его добавлять, то нажми на кнопку *Пропустить*.",
            parse_mode="Markdown",
            reply_markup=markup,
        )


async def save_expense_to_sheet(user_id: int, state: FSMContext, comment: str = ""):
    """
    Saves expense data to user's Google sheet.

    :param user_id: Telegram ID of the user.
    :param state: FSMContext object.
    :param comment: Description to expense.
    """
    async with state.proxy() as data:
        add_expense(
            data["amount"],
            data["category"],
            data["account"],
            comment,
            total_expenses=data["total_expenses"],
            gsheet_id=data["gsheet_id"],
        )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Прожолжить добавление 💸", callback_data="continue_expense"))
    markup.add(InlineKeyboardButton("Отмена ❌", callback_data="cancel_expense"))

    await bot.send_message(
        user_id,
        "Запись успешно добавлена в Goolge таблицу!\nТакже ты можешь продолжить добавлять расходы.",
        reply_markup=markup,
    )


async def cancel_comment_callback(call_query: types.CallbackQuery, state: FSMContext):
    """Saves expense data to Google sheet."""
    await save_expense_to_sheet(call_query.from_user.id, state)


async def get_comment_handler(message: types.Message, state: FSMContext):
    """Gets user's comment and saves expense data to Google sheet."""
    await save_expense_to_sheet(message.from_user.id, state, message.text)


async def cancel_adding_expense(user_id: int, state: FSMContext):
    """
    Breaks the adding expense process.

    :param user_id: Telegram ID of user.
    :param state: FSMContext object.
    """
    await state.finish()
    await bot.send_message(
        user_id,
        "*Отмена*\n\nТеперь ты можешь продолжать вести учет расходов! 💵",
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


async def cancel_adding_expense_handler(message: types.Message, state: FSMContext):
    """Breaks the adding expense process."""
    await cancel_adding_expense(message.from_user.id, state)


async def cancel_adding_expense_callback(call_query: types.CallbackQuery, state: FSMContext):
    """Breaks the adding expense process."""
    await cancel_adding_expense(call_query.from_user.id, state)


def register_expences_handlers(dp: Dispatcher):
    """Registers all handlers related to adding an expence"""
    dp.register_message_handler(
        cancel_adding_expense_handler,
        lambda msg: msg.text.lower() == "отмена",
        state="*",
    )

    dp.register_message_handler(
        add_expense_handler_callback,
        lambda msg: msg.text.lower().startswith("расход"),
        state="*",
    )
    dp.register_message_handler(
        add_expense_handler_callback,
        commands=["add_expense"],
        state="*",
    )
    dp.register_message_handler(
        get_category_handler,
        state=AddsExpense.category,
    )
    dp.register_message_handler(
        get_amount_handler,
        state=AddsExpense.amount,
    )
    dp.register_message_handler(
        get_account_handler,
        state=AddsExpense.account,
    )
    dp.register_message_handler(
        get_comment_handler,
        state=AddsExpense.comment,
    )
    dp.register_callback_query_handler(
        cancel_comment_callback,
        lambda cb: cb.data and cb.data == "finish_expense",
        state=AddsExpense.comment,
    )
    dp.register_callback_query_handler(
        add_expense_handler_callback,
        lambda cb: cb.data and cb.data == "continue_expense",
        state="*",
    )
    dp.register_callback_query_handler(
        cancel_adding_expense_handler,
        lambda cb: cb.data == "cancel_expense",
        state="*",
    )
