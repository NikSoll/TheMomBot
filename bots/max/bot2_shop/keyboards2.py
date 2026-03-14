from config2 import CATEGORIES, PRODUCTS, SHOP_SETTINGS

def get_main_menu():
    return [
        [{"text": "🛍 Каталог", "data": "catalog"}],
        [{"text": "🛒 Корзина", "data": "view_cart"}],
        [{"text": "ℹ️ О магазине", "data": "about"}],
    ]

def get_categories_keyboard():
    keyboard = []
    for cat in CATEGORIES:
        keyboard.append([{
            "text": f"{cat['emoji']} {cat['name']}",
            "data": f"cat_{cat['id']}"
        }])
    keyboard.append([{"text": "🛒 Корзина", "data": "view_cart"}])
    return keyboard

def get_products_keyboard(category_id):
    keyboard = []
    products = [p for p in PRODUCTS if p["category_id"] == category_id]
    for product in products:
        keyboard.append([{
            "text": f"{product['name']} - {product['price']}{SHOP_SETTINGS['currency']}",
            "data": f"prod_{product['id']}"
        }])
    keyboard.append([{"text": "🔙 К категориям", "data": "back_to_categories"}])
    return keyboard

def get_product_detail_keyboard(product_id):
    return [
        [{"text": "➕ Добавить в корзину", "data": f"add_{product_id}"}],
        [{"text": "🔙 К товарам", "data": "back_to_products"}],
    ]

def get_cart_keyboard():
    return [
        [{"text": "✅ Оформить заказ", "data": "checkout"}],
        [{"text": "🗑 Очистить корзину", "data": "clear_cart"}],
        [{"text": "🛍 Продолжить покупки", "data": "back_to_categories"}],
    ]

def get_cancel_keyboard():
    return [[{"text": "❌ Отменить заказ", "data": "cancel_order"}]]