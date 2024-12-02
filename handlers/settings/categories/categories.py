"""
Categories settings.
"""
from typing import Union

from aiogram import types, Dispatcher
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from server import bot


async def categories_settings_callback_handler(message_or_call_query: Union[types.Message, types.CallbackQuery]):
    """Categories settings."""
    user_id = message_or_call_query.from_user.id

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Удалить категорию", callback_data="delete_category"),
        InlineKeyboardButton("Добавить категорию", callback_data="add_category"),
    )
    markup.row(
        InlineKeyboardButton("Переименовать категорию", callback_data="rename_category"),
        InlineKeyboardButton("Отмена", callback_data="settings_cancel"),
    )

    await bot.send_message(
        user_id,
        "*Настройки категорий*\n\nВыбери, что ты хлчешь сделать, нажав на нужную кнопку под сообщением",
        parse_mode="Markdown",
        reply_markup=markup
    )


def register_categories_settings_handlers(dp: Dispatcher):
    """Registers handlers related to categories settings."""
    from handlers.settings.categories.add_category import register_add_category_handlers
    from handlers.settings.categories.delete_category import register_delete_category_handlers
    from handlers.settings.categories.rename_category import register_rename_category_handlers

    dp.register_callback_query_handler(
        categories_settings_callback_handler,
        lambda cb: cb.data == "settings_categories",
    )

    register_add_category_handlers(dp)
    register_delete_category_handlers(dp)
    register_rename_category_handlers(dp)
