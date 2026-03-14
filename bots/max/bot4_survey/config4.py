import os
from dotenv import load_dotenv

load_dotenv()

MAX_KEY = os.getenv("MAX_KEY") or "your_max_api_key"
BOT_ID = os.getenv("BOT_ID") or "your_bot_id"
ADMIN_ID = os.getenv("ADMIN_ID") or "6496349641"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or "https://your-domain.com/webhook"
SECRET_KEY = os.getenv("SECRET_KEY") or "your_secret_key"
SHEET_URL = os.getenv("SHEET_URL") or "https://docs.google.com/spreadsheets/d/your-sheet/edit"

SURVEYS = [
    {
        "id": 1,
        "name": "Опрос: Обратная связь",
        "description": "Помогите нам стать лучше! 🙏",
        "questions": [
            {
                "id": 1,
                "type": "text",
                "text": "Как вас зовут?"
            },
            {
                "id": 2,
                "type": "single",
                "text": "Как часто вы пользуетесь нашими услугами?",
                "options": ["Впервые", "Несколько раз", "Постоянно"]
            },
            {
                "id": 3,
                "type": "multiple",
                "text": "Что вам понравилось? (можно выбрать несколько)",
                "options": ["Качество", "Цена", "Сервис", "Удобство"]
            },
            {
                "id": 4,
                "type": "scale",
                "text": "Оцените нашу работу от 1 до 5",
                "min": 1,
                "max": 5
            },
            {
                "id": 5,
                "type": "text",
                "text": "Ваши пожелания и комментарии:"
            }
        ]
    }
]

SURVEY_SETTINGS = {
    "name": "Опросник-бот",
    "admin_chat_id": ADMIN_ID,
    "sheet_url": SHEET_URL,
    "allow_anonymous": True,
}

MESSAGES = {
    "welcome": "📋 *Добро пожаловать!*\n\nЗдесь вы можете пройти опросы и поделиться своим мнением.",
    "surveys_list": "📋 *Доступные опросы:*",
    "no_surveys": "📭 Пока нет доступных опросов",
    "survey_start": "📝 *{name}*\n\n{description}\n\nВсего вопросов: {questions}\n\n*Начать опрос?*",
    "question_text": "📝 *Вопрос {current}/{total}*\n\n{text}",
    "question_single": "📝 *Вопрос {current}/{total}*\n\n{text}\n\nВыберите один вариант:",
    "question_multiple": "📝 *Вопрос {current}/{total}*\n\n{text}\n\nВыберите несколько вариантов (когда закончите, нажмите Готово):",
    "question_scale": "📝 *Вопрос {current}/{total}*\n\n{text}\n\nОцените от {min} до {max}:",
    "thanks": "🙏 *Спасибо за участие в опросе!*\n\nВаши ответы помогут нам стать лучше.",
    "my_surveys": "📋 *Мои пройденные опросы:*\n\n{surveys}",
    "no_surveys_taken": "📭 Вы еще не проходили опросы",
}

user_sessions = {}