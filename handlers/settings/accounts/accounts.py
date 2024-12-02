"""
Accounts settings.
"""
from typing import Union

from aiogram import Dispatcher, types
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from utils import delete_previous_message
from server import bot


@delete_previous_message
async def accounts_settings_handler_callback(message_or_call_query: Union[types.Message, types.CallbackQuery]):
    """Accounts settings."""
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Изменить баланс", callback_data="change_amount"),
        InlineKeyboardButton("Добавить счет", callback_data="add_account"),
    )
    markup.row(
        InlineKeyboardButton("Переименовать счет", callback_data="rename_account"),
        InlineKeyboardButton("Удалить счет", callback_data="delete_account"),
    )
    markup.row(
        InlineKeyboardButton("Отмена", callback_data="settings_cancel")
    )

    await bot.send_message(
        message_or_call_query.from_user.id,
        "*Настройки счетов*\n\nВыбери, что ты хочешь сделать, нажав на нужную кнопку под сообщением.",
        parse_mode="Markdown",
        reply_markup=markup,
    )


def register_accounts_settings_handlers(dp: Dispatcher):
    """Registers accounts settings handler."""
    from handlers.settings.accounts.change_amount import register_change_amount_handlers
    from handlers.settings.accounts.add_account import register_adding_account_handlers
    from handlers.settings.accounts.rename_account import register_rename_account_handlers
    from handlers.settings.accounts.delete_account import register_delete_account_handlers

    dp.register_callback_query_handler(
        accounts_settings_handler_callback,
        lambda cb: cb.data == "account_settings"
    )

    register_change_amount_handlers(dp)
    register_adding_account_handlers(dp)
    register_rename_account_handlers(dp)
    register_delete_account_handlers(dp)
