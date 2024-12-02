import logging

from random import choice

from aiogram import Dispatcher, executor, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TELEGRAM_TOKEN
from keyboards import register_keyboard
from middleware import LoggingMiddleware


bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    """Handler called when user send /start"""
    await message.answer(
        "Привет! 🤠\n"
        "Я бот для учета расходов/доходов💰\n"
        "Я помогу тебе вести учет финансов в Google таблицах, "
        "которые будут сохранены у тебя на Google диске и ты "
        "всегда будешь иметь к ним доступ!\n\n"
        "Для начала тебе нужно создать файл Google Sheet и "
        "подключить меня к нему.\n"
        "Поэтому скорее нажимай /register и будем начинать!",
        reply_markup=register_keyboard()
    )


async def autoresponder_handler(message: types.Message):
    """Send response to any message not covered by other handlers."""
    gnomes = ['Фили', 'Кили', 'Оин', 'Глоин', 'Двалин', 'Балин', 'Бифур',
              'Бофур', 'Бомбур', 'Дори', 'Нори', 'Ори', 'Торин']
    await message.answer(f"{choice(gnomes).title()} к вашим услугам!")


if __name__ == '__main__':
    from handlers.registration import register_registration_handlers
    from handlers.expenses import register_expences_handlers
    from handlers.incomes import register_incomes_handlers
    from handlers.settings.settings import register_settings_handlers

    dp.middleware.setup(LoggingMiddleware())

    register_registration_handlers(dp)
    register_settings_handlers(dp)
    register_expences_handlers(dp)
    register_incomes_handlers(dp)

    dp.register_message_handler(autoresponder_handler)

    executor.start_polling(dp, skip_updates=True)

