"""
File with reply keyboards for bot
"""

from aiogram.types.reply_keyboard import ReplyKeyboardMarkup


def register_keyboard() -> ReplyKeyboardMarkup:
    """
    Registration keyboard
    :return: ReplyKeyboardMarkup
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("/register")

    return markup


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    Keyboard with all functionality for money management
    :return: ReplyKeyboardMarkup
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Доход 📥', 'Расход 📤')
    markup.add('Настройки ⚙')
    # markup.add('Перевод между счетами 💱')
    # markup.add('Настройки ⚙', 'Статистика 📈')

    return markup


def list_items_keyboard(items: list) -> ReplyKeyboardMarkup:
    """
    Keyboard with list items.

    :param items: List of items.

    :raise AssertionError: If len(categories) less than 1.

    :return: ReplyKeyboardMarkup.
    """
    assert len(items) > 0

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(items) - 1, 2):
        markup.add(*items[i:i + 2])

    if len(items) % 2 == 1:
        markup.add(items[-1])

    return markup
