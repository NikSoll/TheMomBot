from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from .config5 import GROUPS


def get_main_menu(is_admin=False):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="✅ Подписаться"))
    builder.add(KeyboardButton(text="❌ Отписаться"))
    builder.add(KeyboardButton(text="📋 Мои подписки"))

    if is_admin:
        builder.add(KeyboardButton(text="📊 Статистика"))
        builder.add(KeyboardButton(text="📨 Создать рассылку"))

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_groups_keyboard():
    builder = InlineKeyboardBuilder()
    for group in GROUPS:
        builder.add(InlineKeyboardButton(
            text=group['name'],
            callback_data=f"group_{group['id']}"
        ))
    builder.adjust(1)
    return builder.as_markup()


def get_mailing_confirm_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="✅ Отправить",
        callback_data="mailing_send"
    ))
    builder.add(InlineKeyboardButton(
        text="❌ Отмена",
        callback_data="mailing_cancel"
    ))
    builder.adjust(2)
    return builder.as_markup()