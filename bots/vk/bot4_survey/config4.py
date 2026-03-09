import os
from dotenv import load_dotenv

load_dotenv()

VK_TOKEN = "{{VK_TOKEN}}"
GROUP_ID = "{{GROUP_ID}}"
ADMIN_ID = "6496349641"

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
    },
    {
        "id": 2,
        "name": "Опрос: Новый продукт",
        "description": "Расскажите нам о своих предпочтениях",
        "questions": [
            {
                "id": 1,
                "type": "text",
                "text": "Ваш возраст?"
            },
            {
                "id": 2,
                "type": "single",
                "text": "Какой продукт вам интересен?",
                "options": ["Продукт А", "Продукт Б", "Продукт В"]
            }
        ]
    }
]

SURVEY_SETTINGS = {
    "name": "Опросник-бот",
    "admin_chat_id": ADMIN_ID,
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