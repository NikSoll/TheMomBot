import os
from dotenv import load_dotenv

load_dotenv()

MAX_KEY = os.getenv("MAX_KEY") or "your_max_api_key"
BOT_ID = os.getenv("BOT_ID") or "your_bot_id"
ADMIN_ID = os.getenv("ADMIN_ID") or "6496349641"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or "https://your-domain.com/webhook"
SECRET_KEY = os.getenv("SECRET_KEY") or "your_secret_key"
SHEET_URL = os.getenv("SHEET_URL") or "https://docs.google.com/spreadsheets/d/your-sheet/edit"

CATEGORIES = [
    {"id": 1, "name": "👕 Одежда", "emoji": "👕"},
    {"id": 2, "name": "👟 Обувь", "emoji": "👟"},
    {"id": 3, "name": "👜 Аксессуары", "emoji": "👜"},
]

PRODUCTS = [
    {"id": 1, "category_id": 1, "name": "Футболка базовая", "price": 990, "desc": "Хлопок 100%", "photo": None},
    {"id": 2, "category_id": 1, "name": "Худи оверсайз", "price": 2490, "desc": "Теплое, с капюшоном", "photo": None},
    {"id": 3, "category_id": 1, "name": "Джинсы прямые", "price": 2990, "desc": "Классический синий", "photo": None},
    {"id": 4, "category_id": 2, "name": "Кроссовки белые", "price": 3990, "desc": "Унисекс, дышащие", "photo": None},
    {"id": 5, "category_id": 2, "name": "Кеды кожаные", "price": 4590, "desc": "Черные, натуральная кожа", "photo": None},
    {"id": 6, "category_id": 3, "name": "Сумка через плечо", "price": 1890, "desc": "Эко-кожа, 3 цвета", "photo": None},
    {"id": 7, "category_id": 3, "name": "Шапка вязаная", "price": 790, "desc": "Акрил, один размер", "photo": None},
]

SHOP_SETTINGS = {
    "name": "Мой магазин",
    "currency": "₽",
    "delivery_available": True,
    "payment_methods": ["Наличные", "Карта при получении"],
    "admin_chat_id": ADMIN_ID,
}

MESSAGES = {
    "welcome": "🛍 *Добро пожаловать в {name}!*\n\nВыберите действие:",
    "catalog": "📋 *Выберите категорию:*",
    "product_info": "🛍 *{name}*\n\n💰 Цена: *{price}{currency}*\n📝 {desc}",
    "cart_empty": "🛒 *Ваша корзина пуста*",
    "cart": "🛒 *Ваша корзина:*\n\n{cart}\n💰 *Итого: {total}{currency}*",
    "ask_name": "📝 *Введите ваше имя:*",
    "ask_phone": "📞 *Введите ваш телефон:*",
    "ask_address": "📍 *Введите адрес доставки:*",
    "ask_comment": "💬 *Добавьте комментарий (или отправьте '-'):*",
    "order_success": "✅ *Заказ успешно оформлен!*\n\n{order_details}\n\nСпасибо за покупку!",
}

user_carts = {}