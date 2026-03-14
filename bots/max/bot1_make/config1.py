import os
from dotenv import load_dotenv

load_dotenv()

MAX_KEY = os.getenv("MAX_KEY") or "your_max_api_key"
BOT_ID = os.getenv("BOT_ID") or "your_bot_id"
ADMIN_ID = os.getenv("ADMIN_ID") or "6496349641"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or "https://your-domain.com/webhook"
SECRET_KEY = os.getenv("SECRET_KEY") or "your_secret_key"
SHEET_URL = os.getenv("SHEET_URL") or "https://docs.google.com/spreadsheets/d/your-sheet/edit"

MASTERS = [
    {"id": 1, "name": "Анна", "emoji": "💅"},
    {"id": 2, "name": "Мария", "emoji": "✨"},
    {"id": 3, "name": "Ольга", "emoji": "🌟"},
]

SALON_SETTINGS = {
    "name": "Салон красоты",
    "address": "г. Омск, ул. Масленникова, д. 45",
    "phone": "+7 (905) 190-01-54",
    "working_hours": "Пн-Пт: 10:00-20:00, Сб-Вс: 11:00-18:00",
    "admin_chat_id": ADMIN_ID,
}

MESSAGES = {
    "welcome": "💅 *Добро пожаловать в {name}!*\n\nЯ помогу вам записаться на маникюр. Выберите действие:",
    "choose_master": "👩‍🎨 *Выберите мастера:*",
    "choose_date": "📅 *Выберите дату:*",
    "choose_time": "🕐 *Выберите время:*",
    "enter_name": "📝 *Введите ваше имя:*",
    "enter_phone": "📞 *Введите ваш телефон:*",
    "enter_comment": "💬 *Добавьте комментарий (если нужно):*\nИли отправьте '-'",
    "booking_success": "✅ *Запись успешно оформлена!*\n\n• Мастер: {master}\n• Дата: {date}\n• Время: {time}\n• Телефон: {phone}\n\nМы свяжемся с вами для подтверждения.",
    "booking_error": "😔 *Ошибка при записи*\n\nПопробуйте позже или позвоните нам {phone}",
    "my_bookings": "📋 *Ваши записи:*\n\n{bookings}",
    "no_bookings": "📭 *У вас пока нет записей*",
    "about": "ℹ️ *О салоне*\n\n{address}\n🕐 {hours}\n📞 {phone}",
    "contacts": "📞 *Контакты*\n\n📍 {address}\n🕐 {hours}\n📞 {phone}",
}

AVAILABLE_TIMES = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]