"""
File with income control handlers.
"""
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
from google_sheet.incomes import get_total_incomes, add_income


class AddsIncome(StatesGroup):
    amount = State()
    category = State()
    account = State()
    comment = State()


@auth
async def add_income_handler(message: types.Message, state: FSMContext):
    """Adds income to user's Google sheet."""
    await message.answer(
        "*Добавление дохода*\n\nНапиши и отправь мне сумму, которую ты получил\n\n"
        "Чтобы прервать добавление доходов напиши *отмена*.",
        parse_mode="Markdown",
    )
    await AddsIncome.amount.set()

    gsheet_id = get_gsheet_id(message.from_user.id)
    sheet = service_account.open_by_key(gsheet_id)

    settings_worksheet = sheet.worksheet("Настройки")
    transactions_worksheet = sheet.worksheet("Транзакции")

    async with state.proxy() as data:
        data["gsheet_id"] = gsheet_id
        data["categories"] = get_categories(worksheet=settings_worksheet)["income"]
        data["account_names"], data["accounts"] = get_accounts(worksheet=settings_worksheet)
        data["total_incomes"] = get_total_incomes(transactions_worksheet)


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
                "Похоже, что ты еще не добавил ни одной категории доходов.\n"
                "Чтобы ее добавить, введи команду /add_category"
            )
            await state.finish()

        else:
            await message.answer(
                "Теперь выбери категорию доходов из списка под твоей клавиатурой.\n\n",
                reply_markup=list_items_keyboard(sorted(categories)),
            )
            await AddsIncome.category.set()


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
            await message.answer("Ты не создал еще ни одного счета! Чтобы его создать, введи /add_account")
            await state.finish()

        else:
            await message.answer(
                "Выбери из списка под клавиатурой счет, на который пришли деньги.",
                reply_markup=list_items_keyboard(sorted(account_names))
            )
            await AddsIncome.account.set()


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

        await AddsIncome.comment.set()

        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("Пропустить", callback_data="finish_income"))

        await message.answer(
            "Ок! Также ты можешь добавить описание доходу."
            "Для этого напиши его в поле ввода и отправь его мне. Если ты "
            "не хочешь его добавлять, то нажми на кнопку *Пропустить*.",
            parse_mode="Markdown",
            reply_markup=markup,
        )


async def save_income_to_sheet(user_id: int, state: FSMContext, comment: str = ""):
    """
    Saves income data to user's Google sheet.

    :param user_id: Telegram ID of the user.
    :param state: FSMContext object.
    :param comment: Description to income.
    """
    async with state.proxy() as data:
        add_income(
            data["amount"],
            data["category"],
            data["account"],
            comment,
            total_incomes=data["total_incomes"],
            gsheet_id=data["gsheet_id"],
        )

    await state.finish()
    await bot.send_message(
        user_id,
        "Запись успешно добавлена в вашу Goolge таблицу!",
        reply_markup=main_keyboard(),
    )


async def cancel_comment_callback(call_query: types.CallbackQuery, state: FSMContext):
    """Saves income data to Google sheet."""
    await save_income_to_sheet(call_query.from_user.id, state)


async def get_comment_handler(message: types.Message, state: FSMContext):
    """Gets user's comment and saves income data to Google sheet."""
    await save_income_to_sheet(message.from_user.id, state, message.text)


async def cancel_adding_income_handler(message: types.Message, state: FSMContext):
    """Breaks the adding income process."""
    await state.finish()
    await message.answer(
        "*Отмена*\n\nТеперь ты можешь продолжать вести учет расходов! 💵",
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


def register_incomes_handlers(dp: Dispatcher):
    """Registers all handlers related to adding an expence"""
    dp.register_message_handler(
        cancel_adding_income_handler,
        lambda msg: msg.text.lower().startswith("отмена"),
        state="*",
    )

    dp.register_message_handler(
        add_income_handler,
        lambda msg: msg.text.lower().startswith("доход"),
        state="*",
    )
    dp.register_message_handler(
        add_income_handler,
        commands=["add_income"],
        state="*",
    )
    dp.register_message_handler(
        get_category_handler,
        state=AddsIncome.category,
    )
    dp.register_message_handler(
        get_amount_handler,
        state=AddsIncome.amount,
    )
    dp.register_message_handler(
        get_account_handler,
        state=AddsIncome.account,
    )
    dp.register_message_handler(
        get_comment_handler,
        state=AddsIncome.comment,
    )
    dp.register_callback_query_handler(
        cancel_comment_callback,
        lambda cb: cb.data and cb.data == "finish_income",
        state=AddsIncome.comment,
    )
