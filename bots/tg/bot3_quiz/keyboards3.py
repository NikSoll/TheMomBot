from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from .config3 import QUIZZES

def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🎯 Квизы"))
    builder.add(KeyboardButton(text="📊 Мои результаты"))
    builder.add(KeyboardButton(text="🏠 Главное меню"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_quizzes_keyboard():
    builder = InlineKeyboardBuilder()
    for quiz in QUIZZES:
        builder.add(InlineKeyboardButton(
            text=quiz['name'],
            callback_data=f"quiz_{quiz['id']}"
        ))
    builder.adjust(1)
    return builder.as_markup()

def get_quiz_start_keyboard(quiz_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="▶️ Начать квиз",
        callback_data=f"start_quiz_{quiz_id}"
    ))
    return builder.as_markup()

def get_question_keyboard(quiz_id, q_index, question):
    builder = InlineKeyboardBuilder()
    for i, option in enumerate(question['options']):
        builder.add(InlineKeyboardButton(
            text=option['text'],
            callback_data=f"answer_{quiz_id}_{q_index}_{i}"
        ))
    builder.adjust(1)
    return builder.as_markup()

def get_after_quiz_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🎯 Другие квизы",
        callback_data="back_to_quizzes"
    ))
    return builder.as_markup()