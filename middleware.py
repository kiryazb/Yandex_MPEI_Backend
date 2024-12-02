import logging

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class LoggingMiddleware(BaseMiddleware):
    """Logs user's message as info."""
    
    def __init__(self) -> None:
        super(LoggingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict) -> None:
        logging.info(f"User ({message.from_user.id}, @{message.from_user.username}, "
                     f"{message.from_user.first_name}) sent: {message.text}")
