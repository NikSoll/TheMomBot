import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN"
ADMIN_ID = os.getenv("ADMIN_ID") or "YOUR_ADMIN_ID"
SHEET_URL = "YOUR_GOOGLE_SHEET_URL"

QUIZZES = [
    {
        "id": 1,
        "name": "Тест: Какая ты звезда?",
        "description": "Пройди тест и узнай, на какую звезду ты похож! ✨",
        "questions": [
            {
                "id": 1,
                "text": "Как ты проводишь выходные?",
                "options": [
                    {"text": "Тусуюсь с друзьями", "points": {"star": 10, "moon": 5, "sun": 0}},
                    {"text": "Читаю книгу дома", "points": {"star": 0, "moon": 10, "sun": 5}},
                    {"text": "Гуляю на природе", "points": {"star": 5, "moon": 0, "sun": 10}}
                ]
            },
            {
                "id": 2,
                "text": "Твой любимый цвет?",
                "options": [
                    {"text": "Красный", "points": {"star": 10, "moon": 0, "sun": 5}},
                    {"text": "Синий", "points": {"star": 0, "moon": 10, "sun": 5}},
                    {"text": "Желтый", "points": {"star": 5, "moon": 0, "sun": 10}}
                ]
            },
            {
                "id": 3,
                "text": "Что ты выберешь на десерт?",
                "options": [
                    {"text": "Шоколадный торт", "points": {"star": 10, "moon": 5, "sun": 0}},
                    {"text": "Фрукты", "points": {"star": 0, "moon": 5, "sun": 10}},
                    {"text": "Мороженое", "points": {"star": 5, "moon": 10, "sun": 5}}
                ]
            }
        ],
        "results": [
            {"type": "star", "text": "🌟 Ты — ЗВЕЗДА! Ты всегда в центре внимания, яркая и харизматичная!"},
            {"type": "moon", "text": "🌙 Ты — ЛУНА! Загадочная, романтичная и мудрая личность."},
            {"type": "sun", "text": "☀️ Ты — СОЛНЦЕ! Теплая, добрая и энергичная, ты согреваешь всех вокруг!"}
        ]
    }
]

QUIZ_SETTINGS = {
    "name": "Квиз-бот",
    "admin_chat_id": ADMIN_ID,
    "sheet_url": SHEET_URL,
}

MESSAGES = {
    "welcome": "🎯 *Добро пожаловать в мир квизов!*\n\nВыберите интересующий вас тест:",
    "quiz_start": "📝 *{name}*\n\n{description}\n\nВсего вопросов: {questions}",
    "question": "❓ *Вопрос {current}/{total}*\n\n{text}",
    "result": "🎉 *Ваш результат:*\n\n{result}",
    "no_quizzes": "📭 Пока нет доступных квизов",
    "my_results": "📊 *Мои результаты:*\n\n{results}",
    "no_results": "📭 Вы еще не проходили квизы",
}