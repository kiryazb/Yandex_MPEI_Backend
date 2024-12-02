"""
Functions for deleting category.
"""
import logging

from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from database import get_gsheet_id
from google_sheet.categories import get_categories, delete_category
from server import bot
from keyboards import list_items_keyboard, main_keyboard
from config import CREATOR


class DeleteCategory(StatesGroup):
    category_type = State()
    name = State()


async def delete_category_callback_handler(message_or_call_query: Union[types.Message, types.CallbackQuery],
                                           state: FSMContext):
    """Starts delete category process."""
    user_id = message_or_call_query.from_user.id
    gsheet_id = get_gsheet_id(user_id)

    async with state.proxy() as data:
        data["gsheet_id"] = gsheet_id

    await bot.send_message(
        user_id,
        "*Удаление категории*\n\nВыбери тип категории под твоей клавиатурой.",
        parse_mode="Markdown",
        reply_markup=list_items_keyboard(["Расходы", "Доходы"]),
    )
    await DeleteCategory.category_type.set()


async def get_category_type_handler(message: types.Message, state: FSMContext):
    """Gets category type from user."""
    category_type = message.text.lower()
    if category_type in ["расходы", "доходы"]:
        category_type = category_type.replace("расходы", "expense").replace("доходы", "income")
        async with state.proxy() as data:
            categories = get_categories(gsheet_id=data["gsheet_id"])
            data["categories"] = categories
            data["category_type"] = category_type

        await message.answer(
            "*Удаление категории*\n\nНапиши мне название категории, которую ты хочешь удалить. "
            "Под твоей клавиатурой есть список доступных к удалению категорий.",
            parse_mode="Markdown",
            reply_markup=list_items_keyboard(sorted(categories[category_type])),
        )
        await DeleteCategory.name.set()

    else:
        await message.answer(
            "Упс! Похоже ты ошибся, потому что тип категории может быть только "
            f"*расходы* или *доходы*, но никак не {category_type}!",
            parse_mode="Markdown",
            reply_markup=list_items_keyboard(["Расходы", "Доходы"]),
        )


async def get_category_name_handler(message: types.Message, state: FSMContext):
    """Gets category name from user."""
    category_name = message.text.lower()

    async with state.proxy() as data:
        categories = data["categories"]
        category_type = data["category_type"]
        gsheet_id = data["gsheet_id"]

    lowercase_categories = list(map(lambda word: word.lower(), categories[category_type]))
    if category_name not in lowercase_categories:
        await message.answer(
            "Я не знаю такой категории! Попробуй еще раз!",
            reply_markup=list_items_keyboard(categories[category_type]),
        )

    else:
        try:
            delete_category(
                category_name,
                category_type,
                categories=categories,
                gsheet_id=gsheet_id
            )
        except Exception as exc:
            logging.error("Excpetion during delete_category executing!", exc_info=exc)
            await message.answer(
                "*Ошибка!*\n\nНа моей стороне произошла ошибка. Если ты это читаешь, то "
                f"напиши моему создателю: {CREATOR}. Он все починит)",
                parse_mode="Markdown",
                reply_markup=main_keyboard(),
            )

        else:
            await message.answer(
                f"Категория с именем {category_name} успешно удалена!",
                reply_markup=main_keyboard(),
            )

        await state.finish()


def register_delete_category_handlers(dp: Dispatcher):
    """Registers functions related to deleting category."""
    dp.register_message_handler(
        delete_category_callback_handler,
        commands=["delete_category"],
    )
    dp.register_callback_query_handler(
        delete_category_callback_handler,
        lambda cb: cb.data == "delete_category",
    )

    dp.register_message_handler(
        get_category_type_handler,
        state=DeleteCategory.category_type,
    )
    dp.register_message_handler(
        get_category_name_handler,
        state=DeleteCategory.name,
    )
