import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8574049417:AAHW-sdccf78WSer73GW3pPYXOstWqj6HSw"
ADMIN_ID = os.getenv("ADMIN_ID") or "6496349641"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1oWhN2WYuLhVz63gZEjlUGuiKlIQoZx3Ux_mzTC-kxCQ/edit"

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