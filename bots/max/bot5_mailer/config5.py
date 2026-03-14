import os
from dotenv import load_dotenv

load_dotenv()

MAX_KEY = os.getenv("MAX_KEY") or "your_max_api_key"
BOT_ID = os.getenv("BOT_ID") or "your_bot_id"
ADMIN_ID = os.getenv("ADMIN_ID") or "6496349641"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or "https://your-domain.com/webhook"
SECRET_KEY = os.getenv("SECRET_KEY") or "your_secret_key"
SHEET_URL = os.getenv("SHEET_URL") or "https://docs.google.com/spreadsheets/d/your-sheet/edit"

MAILER_SETTINGS = {
    "name": "Рассыльщик",
    "admin_chat_id": ADMIN_ID,
    "sheet_url": SHEET_URL,
    "subscribe_on_start": True,
    "welcome_message": "👋 Добро пожаловать! Вы подписались на наши новости.",
}

GROUPS = [
    {"id": 1, "name": "Все подписчики"},
    {"id": 2, "name": "Новости"},
    {"id": 3, "name": "Акции"},
    {"id": 4, "name": "Мероприятия"},
]

MESSAGES = {
    "welcome": "📢 *Добро пожаловать в бот-рассыльщик!*\n\nЗдесь вы можете подписаться на новости и получать уведомления.",
    "subscribed": "✅ Вы успешно подписались на рассылку!",
    "unsubscribed": "❌ Вы отписались от рассылки. Будем ждать вас снова!",
    "already_subscribed": "ℹ️ Вы уже подписаны на рассылку",
    "not_subscribed": "ℹ️ Вы не подписаны на рассылку",
    "stats": "📊 *Статистика*\n\n👥 Всего подписчиков: {total}\n✅ Активных: {active}",
    "mailing_start": "📨 Рассылка начата. Отправлено: {sent} | Ошибок: {failed}",
    "mailing_complete": "✅ Рассылка завершена!\n\nВсего: {total}\n✅ Доставлено: {sent}\n❌ Ошибок: {failed}",
}