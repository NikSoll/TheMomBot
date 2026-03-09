VK_TOKEN = "{{VK_TOKEN}}"
GROUP_ID = "{{GROUP_ID}}"
ADMIN_ID = "6496349641"

CATEGORIES = [
    {"id": 1, "name": "👕 Одежда", "emoji": "👕"},
    {"id": 2, "name": "👟 Обувь", "emoji": "👟"},
    {"id": 3, "name": "👜 Аксессуары", "emoji": "👜"},
]

#товары
PRODUCTS = [
    #одежда (category_id=1)
    {"id": 1, "category_id": 1, "name": "Футболка базовая", "price": 990,
     "desc": "Хлопок 100%, размеры S-M-L", "photo": None},
    {"id": 2, "category_id": 1, "name": "Худи оверсайз", "price": 2490,
     "desc": "Теплое, с капюшоном, 3 цвета", "photo": None},
    {"id": 3, "category_id": 1, "name": "Джинсы прямые", "price": 2990,
     "desc": "Классический синий, все размеры", "photo": None},

    #обувь (category_id=2)
    {"id": 4, "category_id": 2, "name": "Кроссовки белые", "price": 3990,
     "desc": "Унисекс, дышащие", "photo": None},
    {"id": 5, "category_id": 2, "name": "Кеды кожаные", "price": 4590,
     "desc": "Черные, натуральная кожа", "photo": None},

    #аксессуары (category_id=3)
    {"id": 6, "category_id": 3, "name": "Сумка через плечо", "price": 1890,
     "desc": "Эко-кожа, 3 цвета", "photo": None},
    {"id": 7, "category_id": 3, "name": "Шапка вязаная", "price": 790,
     "desc": "Акрил, один размер", "photo": None},
]

#настройки магазина
SHOP_SETTINGS = {
    "name": "Мой магазин",
    "currency": "₽",
    "delivery_available": True,
    "payment_methods": ["Наличные", "Карта при получении"],
    "admin_chat_id": None,  #id админа
}

#тексты сообщений
MESSAGES = {
    "welcome": "🛍 *Добро пожаловать в {name}!*\n\nВыберите действие:",
    "catalog": "📋 *Выберите категорию:*",
    "product_info": "🛍 *{name}*\n\n💰 Цена: *{price}{currency}*\n📝 {desc}",
    "cart_empty": "🛒 *Ваша корзина пуста*",
    "cart": "🛒 *Ваша корзина:*\n\n{cart}\n💰 *Итого: {total}{currency}*",
    "ask_name": "📝 *Введите ваше имя:*",
    "ask_phone": "📞 *Введите ваш телефон:*",
    "ask_address": "📍 *Введите адрес доставки:*",
    "order_success": "✅ *Заказ успешно оформлен!*\n\n{order_details}\n\nСпасибо за покупку!",
}