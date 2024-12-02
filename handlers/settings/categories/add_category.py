"""
Functions for adding a category.
"""
import logging

from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import get_gsheet_id
from google_sheet.categories import get_categories, add_category
from server import bot
from keyboards import list_items_keyboard, main_keyboard
from config import CREATOR


class AddCategory(StatesGroup):
    category_type = State()
    category_name = State()


async def add_category_handler_callback(message_or_call_query: Union[types.Message, types.CallbackQuery],
                                        state: FSMContext):
    """Starts adding category."""
    user_id = message_or_call_query.from_user.id
    gsheet_id = get_gsheet_id(user_id)

    await bot.send_message(
        user_id,
        "*Добавление категории*\n\nКатегорию какого типа ты хочешь добавить? Выбери из списка под клавиатурой.",
        parse_mode="Markdown",
        reply_markup=list_items_keyboard(["Доходы", "Расходы"]),
    )
    await AddCategory.category_type.set()

    async with state.proxy() as data:
        data["gsheet_id"] = gsheet_id
        data["categories"] = get_categories(gsheet_id=gsheet_id)


async def get_category_type(message: types.Message, state: FSMContext):
    """Gets category type from user."""
    category_type = message.text.lower()
    if category_type in ["расходы", "доходы"]:
        category_type = category_type.replace("расходы", "expense").replace("доходы", "income")
        async with state.proxy() as data:
            data["category_type"] = category_type

        await message.answer(
            "*Добавление категории*\n\nВведи название категории, которую ты хочешь добавить!",
            parse_mode="Markdown",
        )
        await AddCategory.category_name.set()

    else:
        await message.answer(
            "Я не знаю такого типа категории! Попробуй еще раз!",
            reply_markup=list_items_keyboard(["Доходы", "Расходы"]),
        )


async def get_category_name_handler(message: types.Message, state: FSMContext):
    """Gets category name form user and adds it to user's Google sheet."""
    category_name = message.text

    async with state.proxy() as data:
        categories = data["categories"]
        category_type = data["category_type"]
        gsheet_id = data["gsheet_id"]

    lowercase_categories = list(map(lambda word: word.lower(), categories[category_type]))
    if category_name.lower() in lowercase_categories:
        await message.answer(
            f"Хм...  Категория {category_name} типа {category_type.lower()} уже "
            f"существует! Придумай другое название!",
            parse_mode="Markdown",
        )

    else:
        try:
            add_category(
                category_name,
                category_type,
                categories=categories,
                gsheet_id=gsheet_id,
            )
        except Exception as exc:
            logging.error("Excpetion during add_category executing!", exc_info=exc)
            await message.answer(
                "*Ошибка!*\n\nНа моей стороне произошла ошибка. Если ты это читаешь, то "
                f"напиши моему создателю: {CREATOR}. Он все починит)",
                parse_mode="Markdown",
                reply_markup=main_keyboard(),
            )

        else:
            await message.answer(
                f"Категория {category_name} успешно добавлена!",
                reply_markup=main_keyboard(),
            )

        await state.finish()


def register_add_category_handlers(dp: Dispatcher):
    """Registers handlers related to add category."""
    dp.register_message_handler(
        add_category_handler_callback,
        commands=["add_category"],
    )
    dp.register_callback_query_handler(
        add_category_handler_callback,
        lambda cb: cb.data == "add_category",
    )

    dp.register_message_handler(
        get_category_type,
        state=AddCategory.category_type,
    )
    dp.register_message_handler(
        get_category_name_handler,
        state=AddCategory.category_name,
    )
