"""
Settings for bot.
"""
from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from server import bot
from keyboards import main_keyboard
from utils import auth


async def settings_cancel(call_query: types.CallbackQuery):
    """Breaks account setting process."""
    await bot.send_message(
        call_query.from_user.id,
        "*Отмена*\n\nТеперь ты можешь продолжать вести учет расходов! 💵",
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


@auth
async def settings_handler(message: types.Message):
    """Go to settings."""
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Счета", callback_data="account_settings"),
        InlineKeyboardButton("Категории", callback_data="settings_categories"),
    )

    await message.answer(
        "*Настройки*\n\nВ настройках ты можешь добавить новый счет или изменить старый, "
        "то же самое ты можешь сделать и с категориями.",
        parse_mode="Markdown",
        reply_markup=markup,
    )


def register_settings_handlers(dp: Dispatcher):
    """Registers all handlers related to new user registration."""
    from handlers.settings.accounts.accounts import register_accounts_settings_handlers
    from handlers.settings.categories.categories import register_categories_settings_handlers

    register_accounts_settings_handlers(dp)
    register_categories_settings_handlers(dp)

    dp.register_callback_query_handler(
        settings_cancel,
        lambda cb: cb.data == "settings_cancel",
    )

    dp.register_message_handler(
        settings_handler,
        lambda msg: msg.text.lower().startswith("настройки"),
    )
