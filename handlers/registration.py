from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.types.inline_keyboard import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

import gspread
from gspread.utils import extract_id_from_url

import database as db

from server import bot
from utils import delete_previous_message, is_gsheet_id_correct
from keyboards import main_keyboard
from config import LINK_TO_GOOGLE_SHEET, BOT_EMAIL


class GetLinkToGoogleSheet(StatesGroup):
    waiting_for_gsheet_id = State()


async def register(user_id: int):
    """
    Registers new user or change old's user gsheet_id
    Helps new user to create Google account

    :param user_id: telegram user ID
    """
    ReplyKeyboardRemove()

    user = db.get_or_add_user(user_id)
    if user.gsheet_id:
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("Подключить к другой таблице 📃", callback_data="connect_to_other_table"))
        markup.row(InlineKeyboardButton("Удалить мои данные 🗑️", callback_data="delete_user_data"))
        markup.row(InlineKeyboardButton("Отмена ❌", callback_data="reg_cancel"))

        await bot.send_message(
            user_id,
            "Я уже подключен к твоей Google таблице 🤔\n"
            "Может быть ты хочешь подключить меня к другой таблице "
            "или ты хочешь, чтобы я удалил данные о текущей (тогда "
            "ты меня больше не сможешь использовать)?",
            reply_markup=markup,
        )

    else:
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(">>> Готово! ✅", callback_data="google_drive_sign_in"))
        markup.row(InlineKeyboardButton("Отмена ❌", callback_data="reg_cancel"))

        await bot.send_message(
            user_id,
            "*ШАГ 1*\n\n"
            "Для всей действий тебе понадобится "
            "Goolge аккаунт. Если у тебя его ещё нет, то, перейдя по "
            "[ссылке](https://support.google.com/accounts/answer/27441?hl=ru), "
            "ты получишь подробную инструкцию по его созданию",
            reply_markup=markup,
            parse_mode="Markdown"
        )


async def register_cmd(message: types.Message):
    """
    Registers new user or change old's user gsheet_id
    Helps new user to create Google account
    """
    await register(message.from_user.id)


@delete_previous_message
async def register_callback(call_query: types.CallbackQuery):
    """
    Registers new user or change old's user gsheet_id
    Helps new user to create Google account
    """
    await register(call_query.from_user.id)


@delete_previous_message
async def google_drive_sign_in_callback(call_query: types.CallbackQuery):
    """Helps new user to copy Goolge sheet to their own Google Drive"""
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(">>> Готово! ✅", callback_data="share_google_sheet_to_bot"))
    markup.row(InlineKeyboardButton("<<< Назад ↩", callback_data="register"))
    markup.row(InlineKeyboardButton("Отмена ❌", callback_data="reg_cancel"))

    await bot.send_message(
        call_query.from_user.id,
        "*ШАГ 2*\n\n"
        "Отлично!\nТеперь перейди по [уже другой ссылке]"
        f"({LINK_TO_GOOGLE_SHEET})"
        " и выполни следующие действия:\n"
        "1. На верхней панели нажми на *\"Файл\" -> \"Создать копию\"*.\n"
        "2. Теперь введи название для файла (любой текст) и выбери "
        "папку, в которую он будет сохранен.\n\n",
        parse_mode="Markdown",
        reply_markup=markup,
    )


@delete_previous_message
async def share_google_sheet_to_bot_callback(call_query: types.CallbackQuery):
    """Asks the user to share their Google sheet with bot"""
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(">>> Готово! ✅", callback_data="get_user_google_sheet_id"))
    markup.row(InlineKeyboardButton("<<< Назад ↩", callback_data="google_drive_sign_in"))
    markup.row(InlineKeyboardButton("Отмена ❌", callback_data="reg_cancel"))

    await bot.send_message(
        call_query.from_user.id,
        "*ШАГ 3*\n\n"
        "Супер!\nТеперь нажми в правом верхнем углу на кнопку "
        "*\"Настройки доступа\"* и в поле ввода вставь мой email адрес: "
        f"`{BOT_EMAIL}` "
        "(нажми на него и он скопируется).\n"
        "Справа от поля выбери роль *Редактор* (обычно стоит "
        "по умолчанию редактор), убери галочку с "
        "*Уведомить пользователей* и нажми на кнопку *Настройки доступа*. ",
        parse_mode="Markdown",
        reply_markup=markup,
    )


@delete_previous_message
async def get_user_google_sheet_id_callback(call_query: types.CallbackQuery):
    """Asks the user to send to bot their Google sheet url"""
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("<<< Назад ↩", callback_data="share_google_sheet_to_bot"))
    markup.row(InlineKeyboardButton("Отмена ❌", callback_data="reg_cancel"))

    await bot.send_message(
        call_query.from_user.id,
        "*ШАГ 4*\n\n"
        "Ок!\nТеперь в *Настройках доступа* нажми *Копировать ссылку*, "
        "она сохранится в буфер обмена.\n"
        "Отправь ее мне, чтобы я смог подключиться к твоей таблице!",
        parse_mode="Markdown",
        reply_markup=markup,
    )

    await GetLinkToGoogleSheet.waiting_for_gsheet_id.set()


async def get_user_google_sheet_id(message: types.Message, state: FSMContext):
    """Gets user's Google sheet id and saves it to database"""
    try:
        gsheet_id = extract_id_from_url(message.text)

        if not is_gsheet_id_correct(gsheet_id):
            raise gspread.exceptions.NoValidUrlKeyFound

    except gspread.exceptions.NoValidUrlKeyFound:
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("<<< Шаг 3", callback_data="share_google_sheet_to_bot"))
        markup.row(InlineKeyboardButton("<<< Шaг 4", callback_data="get_user_google_sheet_id"))
        await message.answer(
            "Упс! По этой ссылке я не могу подключиться к твоей "
            "Google таблице!\nПроверь, что ты правильно ее скопировал "
            " (шаг 4) и дал мне доступ к твоей Google таблице (шаг 3).\n"
            "Введи ссылку еще раз или попробуй вернуться назад!",
            parse_mode="Markdown",
            reply_markup=markup,
        )

    else:
        await state.update_data(google_sheet_id=gsheet_id)
        db.update_gsheet_id(message.from_user.id, gsheet_id)
        await message.answer(
            "Отлично! 🤩\n\n"
            "Теперь я подключен к твоей таблице и ты можешь "
            "начать вести учет своих финансов с помощью клавиатуры под "
            "полем ввода текста!",
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )

        await state.finish()


@delete_previous_message
async def connect_to_other_table_callback(call_query: types.CallbackQuery):
    """Connects to the other Google table"""
    user = db.update_gsheet_id(call_query.from_user.id, "")

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Пройти обучение 📚", callback_data="register"))

    await bot.send_message(
        user.user_id,
        "*Данные успешно удалены*\n"
        "Отправь мне ссылку на новую Google таблицу, чтобы я мог к ней "
        "подключиться. Также, если ты забыл, где ее брать, ты можешь "
        "пройти обучение, нажав на кнопку снизу.",
        parse_mode="Markdown",
        reply_markup=markup,
    )

    await GetLinkToGoogleSheet.waiting_for_gsheet_id.set()


@delete_previous_message
async def delete_user_data_callback(call_query: types.CallbackQuery):
    """Deletes user's data (gsheet_id) from database"""
    user = db.update_gsheet_id(call_query.from_user.id, "")
    await bot.send_message(
        user.user_id,
        "*Данные успешно удалены*\n\n"
        "Чтобы продолжить меня использовать, напиши /register",
        parse_mode="Markdown",
    )


@delete_previous_message
async def register_cancel_callback(call_query: types.CallbackQuery, state: FSMContext):
    """Returns to the standart usage mode (finance control)"""
    await state.finish()
    await bot.send_message(
        call_query.from_user.id,
        "*Отмена*. Надеюсь, ты не на долго",
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


def register_registration_handlers(dp: Dispatcher):
    """Registers all handlers related to new user registrations"""
    dp.register_message_handler(register_cmd, commands=["register"])
    dp.register_callback_query_handler(
        register_callback,
        lambda cb: cb.data and cb.data == "register",
        state='*',
    )

    dp.register_callback_query_handler(
        google_drive_sign_in_callback,
        lambda cb: cb.data and cb.data == "google_drive_sign_in",
        state='*',
    )
    dp.register_callback_query_handler(
        share_google_sheet_to_bot_callback,
        lambda cb: cb.data and cb.data == "share_google_sheet_to_bot",
        state='*',
    )
    dp.register_callback_query_handler(
        get_user_google_sheet_id_callback,
        lambda cb: cb.data and cb.data == "get_user_google_sheet_id",
        state='*',
    )
    dp.register_message_handler(
        get_user_google_sheet_id,
        state=GetLinkToGoogleSheet.waiting_for_gsheet_id,
    )

    dp.register_callback_query_handler(
        connect_to_other_table_callback,
        lambda cb: cb.data and cb.data == "connect_to_other_table",
    )
    dp.register_callback_query_handler(
        delete_user_data_callback,
        lambda cb: cb.data and cb.data == "delete_user_data",
    )

    dp.register_callback_query_handler(
        register_cancel_callback,
        lambda cb: cb.data and cb.data == "reg_cancel",
        state="*",
    )
