"""
Functions for renaming a category.
"""
import logging

from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import get_gsheet_id
from google_sheet.categories import get_categories, rename_category
from server import bot
from keyboards import list_items_keyboard, main_keyboard
from config import CREATOR


class RenameCategory(StatesGroup):
    category_type = State()
    category_name = State()
    new_category_name = State()


async def rename_category_handler_callback(message_or_call_query: Union[types.Message, types.CallbackQuery],
                                           state: FSMContext):
    """Starts renaming a category."""
    user_id = message_or_call_query.from_user.id
    gsheet_id = get_gsheet_id(user_id)

    await bot.send_message(
        user_id,
        "*Изменение категории*\n\nКатегорию какого типа ты хочешь переименовать? Выбери из списка под клавиатурой.",
        parse_mode="Markdown",
        reply_markup=list_items_keyboard(["Доходы", "Расходы"]),
    )
    await RenameCategory.category_type.set()

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
            categories = data["categories"]

        await message.answer(
            "*Изменение категории*\n\nВыбери категорию, которую ты хочешь переименовать!",
            parse_mode="Markdown",
            reply_markup=list_items_keyboard(categories[category_type])
        )
        await RenameCategory.category_name.set()

    else:
        await message.answer(
            "Я не знаю такого типа категории! Попробуй еще раз!",
            reply_markup=list_items_keyboard(["Доходы", "Расходы"]),
        )


async def get_category_name_handler(message: types.Message, state: FSMContext):
    """Gets category name form user."""
    category_name = message.text

    async with state.proxy() as data:
        categories = data["categories"]
        category_type = data["category_type"]
        # gsheet_id = data["gsheet_id"]

    lowercase_categories = list(map(lambda word: word.lower(), categories[category_type]))
    if category_name.lower() not in lowercase_categories:
        await message.answer(
            f"*Хм...* Категории {category_name} типа {category_type.lower()} не "
            f"существует! Попробуй еще раз!",
            parse_mode="Markdown",
            reply_markup=list_items_keyboard(categories[category_type]),
        )

    else:
        await message.answer(
            f"*Изменение категории*\n\nВведи новое название для категории {category_name}.",
            parse_mode="Markdown",
        )

        async with state.proxy() as data:
            data["category_name"] = category_name

        await RenameCategory.new_category_name.set()


async def get_new_category_name_handler(message: types.Message, state: FSMContext):
    """Gets new category name form user and adds it to user's Google sheet."""
    new_name = message.text

    async with state.proxy() as data:
        categories = data["categories"]
        category_type = data["category_type"]
        category_name = data["category_name"]
        gsheet_id = data["gsheet_id"]

    if new_name.lower() in map(lambda word: word.lower(), categories[category_type]):
        await message.answer(
            f"*Опа!*\nКатегория с именем {new_name} типа {category_type} уже существует! "
            "Ты не можешь переименовать категорию в уже существующую! Попробуй еще раз!",
            parse_mode="Markdown",
        )

    else:
        try:
            rename_category(
                category_name,
                new_name,
                category_type,
                categories=categories,
                gsheet_id=gsheet_id,
            )
        except Exception as exc:
            logging.error("Excpetion during rename_category executing!", exc_info=exc)
            await message.answer(
                "*Ошибка!*\n\nНа моей стороне произошла ошибка. Если ты это читаешь, то "
                f"напиши моему создателю: {CREATOR}. Он все починит)",
                parse_mode="Markdown",
                reply_markup=main_keyboard(),
            )

        else:
            await message.answer(
                f"Категория с именем {category_name} успешно переименована в {new_name}!",
                reply_markup=main_keyboard(),
            )

        await state.finish()


def register_rename_category_handlers(dp: Dispatcher):
    """Registers handlers related to renaimg a category."""
    dp.register_message_handler(
        rename_category_handler_callback,
        commands=["rename_category"],
    )
    dp.register_callback_query_handler(
        rename_category_handler_callback,
        lambda cb: cb.data == "rename_category",
    )

    dp.register_message_handler(
        get_category_type,
        state=RenameCategory.category_type,
    )
    dp.register_message_handler(
        get_category_name_handler,
        state=RenameCategory.category_name,
    )
    dp.register_message_handler(
        get_new_category_name_handler,
        state=RenameCategory.new_category_name,
    )

