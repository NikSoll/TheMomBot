from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from datetime import datetime, timedelta

from .config1 import MASTERS, AVAILABLE_TIMES

def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📝 Записаться"))
    builder.add(KeyboardButton(text="📋 Мои записи"))
    builder.add(KeyboardButton(text="ℹ️ О салоне"))
    builder.add(KeyboardButton(text="📞 Контакты"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_masters_keyboard():
    builder = InlineKeyboardBuilder()
    for master in MASTERS:
        builder.add(InlineKeyboardButton(
            text=f"{master['emoji']} {master['name']}",
            callback_data=f"master_{master['id']}"
        ))
    builder.add(InlineKeyboardButton(
        text="❌ Отмена",
        callback_data="cancel"
    ))
    builder.adjust(1)
    return builder.as_markup()

def get_dates_keyboard():
    builder = InlineKeyboardBuilder()
    today = datetime.now()
    for i in range(7):
        date = today + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        display_str = date.strftime("%d.%m (%a)")
        builder.add(InlineKeyboardButton(
            text=display_str,
            callback_data=f"date_{date_str}"
        ))
    builder.add(InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data="back_to_masters"
    ))
    builder.adjust(3)
    return builder.as_markup()

def get_times_keyboard():
    builder = InlineKeyboardBuilder()
    for time in AVAILABLE_TIMES:
        builder.add(InlineKeyboardButton(
            text=time,
            callback_data=f"time_{time}"
        ))
    builder.add(InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data="back_to_dates"
    ))
    builder.adjust(3)
    return builder.as_markup()

def get_cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❌ Отменить запись"))
    return builder.as_markup(resize_keyboard=True)