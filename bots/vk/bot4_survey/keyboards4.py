from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from .config4 import SURVEYS


def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📋 Пройти опрос"))
    builder.add(KeyboardButton(text="📋 Мои опросы"))
    builder.add(KeyboardButton(text="🏠 Главное меню"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_surveys_keyboard():
    builder = InlineKeyboardBuilder()
    for survey in SURVEYS:
        builder.add(InlineKeyboardButton(
            text=survey['name'],
            callback_data=f"survey_{survey['id']}"
        ))
    builder.adjust(1)
    return builder.as_markup()


def get_survey_start_keyboard(survey_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="▶️ Начать опрос",
        callback_data=f"start_survey_{survey_id}"
    ))
    return builder.as_markup()


def get_single_choice_keyboard(survey_id, q_index, options):
    builder = InlineKeyboardBuilder()
    for i, option in enumerate(options):
        builder.add(InlineKeyboardButton(
            text=option,
            callback_data=f"single_{survey_id}_{q_index}_{i}"
        ))
    builder.adjust(1)
    return builder.as_markup()


def get_multiple_choice_keyboard(survey_id, q_index, options, selected=None):
    if selected is None:
        selected = []

    builder = InlineKeyboardBuilder()
    for i, option in enumerate(options):
        check = "✅ " if i in selected else ""
        builder.add(InlineKeyboardButton(
            text=f"{check}{option}",
            callback_data=f"multiple_{survey_id}_{q_index}_select_{i}"
        ))
    builder.add(InlineKeyboardButton(
        text="✅ Готово",
        callback_data=f"multiple_{survey_id}_{q_index}_done"
    ))
    builder.adjust(1)
    return builder.as_markup()


def get_scale_keyboard(survey_id, q_index, min_val, max_val):
    builder = InlineKeyboardBuilder()
    for i in range(min_val, max_val + 1):
        builder.add(InlineKeyboardButton(
            text=str(i),
            callback_data=f"scale_{survey_id}_{q_index}_{i}"
        ))
    builder.adjust(5)
    return builder.as_markup()


def get_after_survey_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="📋 Другие опросы",
        callback_data="back_to_surveys"
    ))
    return builder.as_markup()