from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from .config2 import CATEGORIES, PRODUCTS, SHOP_SETTINGS

#галвная
def get_main_menu():
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="🛍 Каталог"))
    builder.add(KeyboardButton(text="🛒 Корзина"))
    builder.add(KeyboardButton(text="ℹ️ О магазине"))
    builder.add(KeyboardButton(text="📞 Контакты"))

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

#ктегории
def get_categories_keyboard():
    builder = InlineKeyboardBuilder()

    for cat in CATEGORIES:
        builder.add(InlineKeyboardButton(
            text=f"{cat['emoji']} {cat['name']}",
            callback_data=f"shop_cat_{cat['id']}"
        ))

    builder.add(InlineKeyboardButton(
        text="🛒 Корзина",
        callback_data="shop_view_cart"
    ))

    builder.adjust(2)
    return builder.as_markup()


def get_products_keyboard(category_id):
    builder = InlineKeyboardBuilder()

    #формирован
    category_products = [p for p in PRODUCTS if p["category_id"] == category_id]

    for product in category_products:
        builder.add(InlineKeyboardButton(
            text=f"{product['name']} - {product['price']}{SHOP_SETTINGS['currency']}",
            callback_data=f"shop_prod_{product['id']}"
        ))

    builder.add(InlineKeyboardButton(
        text="🔙 К категориям",
        callback_data="shop_back_to_categories"
    ))

    builder.adjust(1)
    return builder.as_markup()

#детаил товар
def get_product_detail_keyboard(product_id):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="➕ Добавить в корзину",
        callback_data=f"shop_add_{product_id}"
    ))
    builder.add(InlineKeyboardButton(
        text="🔙 К товарам",
        callback_data="shop_back_to_products"
    ))

    builder.adjust(1)
    return builder.as_markup()

#корзина
def get_cart_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="✅ Оформить заказ",
        callback_data="shop_checkout"
    ))
    builder.add(InlineKeyboardButton(
        text="🗑 Очистить корзину",
        callback_data="shop_clear_cart"
    ))
    builder.add(InlineKeyboardButton(
        text="🛍 Продолжить покупки",
        callback_data="shop_back_to_categories"
    ))

    builder.adjust(1)
    return builder.as_markup()

#отмена заказа
def get_cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❌ Отменить заказ"))
    return builder.as_markup(resize_keyboard=True)