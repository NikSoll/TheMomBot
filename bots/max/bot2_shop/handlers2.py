from datetime import datetime
from config2 import SHOP_SETTINGS, MESSAGES, ADMIN_ID
from . import keyboards2 as kb
from . import utils2
from .states2 import ShopStates
from .database2 import db

user_carts = {}
user_sessions = {}


def register_handlers(bot):
    @bot.on_message("text")
    async def message_handler(event):
        user_id = event.user_id
        text = event.text
        session = user_sessions.get(user_id, {"state": None})

        if text == "/start":
            await start_handler(event, bot)
        elif session.get("state") == ShopStates.ENTERING_NAME:
            await process_name(event, bot)
        elif session.get("state") == ShopStates.ENTERING_PHONE:
            await process_phone(event, bot)
        elif session.get("state") == ShopStates.ENTERING_ADDRESS:
            await process_address(event, bot)
        elif session.get("state") == ShopStates.ENTERING_COMMENT:
            await process_comment(event, bot)
        else:
            await start_handler(event, bot)

    @bot.on_callback("start")
    async def start_handler(event, bot=None):
        user_id = event.user_id
        await bot.send_message(
            user_id=user_id,
            text=MESSAGES["welcome"].format(name=SHOP_SETTINGS['name']),
            keyboard=kb.get_main_menu()
        )

    @bot.on_callback("catalog")
    async def catalog_handler(event):
        user_id = event.user_id
        user_sessions[user_id] = {"state": ShopStates.BROWSING}
        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["catalog"],
            keyboard=kb.get_categories_keyboard()
        )

    @bot.on_callback_pattern(r"cat_(\d+)")
    async def category_handler(event, category_id):
        user_id = event.user_id
        category = utils2.get_category_by_id(int(category_id))
        if category:
            user_sessions[user_id]["current_category"] = int(category_id)
            await event.bot.send_message(
                user_id=user_id,
                text=f"📁 *{category['emoji']} {category['name']}*\n\nВыберите товар:",
                keyboard=kb.get_products_keyboard(int(category_id))
            )

    @bot.on_callback_pattern(r"prod_(\d+)")
    async def product_handler(event, product_id):
        user_id = event.user_id
        product = utils2.get_product_by_id(int(product_id))
        if product:
            user_sessions[user_id]["current_product"] = int(product_id)
            user_sessions[user_id]["state"] = ShopStates.VIEWING_PRODUCT
            text = MESSAGES["product_info"].format(
                name=product['name'],
                price=product['price'],
                currency=SHOP_SETTINGS['currency'],
                desc=product['desc']
            )
            await event.bot.send_message(
                user_id=user_id,
                text=text,
                keyboard=kb.get_product_detail_keyboard(int(product_id))
            )

    @bot.on_callback_pattern(r"add_(\d+)")
    async def add_to_cart_handler(event, product_id):
        user_id = event.user_id
        product = utils2.get_product_by_id(int(product_id))
        if product:
            cart = user_carts.get(user_id, [])
            cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"]
            })
            user_carts[user_id] = cart
            await event.bot.send_message(
                user_id=user_id,
                text=f"✅ {product['name']} добавлен в корзину!"
            )
            # Возврат к товарам категории
            category_id = user_sessions.get(user_id, {}).get("current_category")
            if category_id:
                await event.bot.send_message(
                    user_id=user_id,
                    text="📁 Выберите товар:",
                    keyboard=kb.get_products_keyboard(category_id)
                )

    @bot.on_callback("view_cart")
    async def view_cart_handler(event):
        user_id = event.user_id
        cart = user_carts.get(user_id, [])

        if not cart:
            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["cart_empty"]
            )
            return

        total = utils2.calculate_total(cart)
        cart_text = utils2.format_cart(cart)
        text = MESSAGES["cart"].format(
            cart=cart_text,
            total=total,
            currency=SHOP_SETTINGS['currency']
        )
        user_sessions[user_id]["state"] = ShopStates.IN_CART
        await event.bot.send_message(
            user_id=user_id,
            text=text,
            keyboard=kb.get_cart_keyboard()
        )

    @bot.on_callback("clear_cart")
    async def clear_cart_handler(event):
        user_id = event.user_id
        user_carts[user_id] = []
        await event.bot.send_message(
            user_id=user_id,
            text="🗑 *Корзина очищена*"
        )

    @bot.on_callback("checkout")
    async def checkout_handler(event):
        user_id = event.user_id
        cart = user_carts.get(user_id, [])

        if not cart:
            await event.bot.send_message(
                user_id=user_id,
                text="Корзина пуста!"
            )
            return

        user_sessions[user_id]["state"] = ShopStates.ENTERING_NAME
        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["ask_name"]
        )

    async def process_name(event):
        user_id = event.user_id
        user_sessions[user_id]["name"] = event.text
        user_sessions[user_id]["state"] = ShopStates.ENTERING_PHONE
        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["ask_phone"],
            keyboard=kb.get_cancel_keyboard()
        )

    async def process_phone(event):
        user_id = event.user_id
        user_sessions[user_id]["phone"] = event.text
        user_sessions[user_id]["state"] = ShopStates.ENTERING_ADDRESS
        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["ask_address"]
        )

    async def process_address(event):
        user_id = event.user_id
        user_sessions[user_id]["address"] = event.text
        user_sessions[user_id]["state"] = ShopStates.ENTERING_COMMENT
        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["ask_comment"]
        )

    async def process_comment(event):
        user_id = event.user_id
        comment = event.text if event.text != "-" else ""

        data = user_sessions.get(user_id, {})
        cart = user_carts.get(user_id, [])

        order = {
            'user_id': user_id,
            'username': event.username or "",
            'name': data.get('name'),
            'phone': data.get('phone'),
            'address': data.get('address'),
            'comment': comment,
            'cart': cart.copy(),
            'total': utils2.calculate_total(cart),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Сохранение в БД
        db.add_order(order)

        cart_text = utils2.format_cart(order['cart'])
        order_details = (
            f"*Ваш заказ:*\n"
            f"{cart_text}\n"
            f"💰 *Итого: {order['total']}{SHOP_SETTINGS['currency']}*\n\n"
            f"📞 *Телефон:* {order['phone']}\n"
            f"📍 *Адрес:* {order['address']}"
        )

        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["order_success"].format(order_details=order_details),
            keyboard=kb.get_main_menu()
        )

        # Уведомление админу
        if ADMIN_ID:
            admin_text = f"🛍 *Новый заказ!*\n\n{order_details}"
            await event.bot.send_message(
                user_id=ADMIN_ID,
                text=admin_text
            )

        # Очистка
        user_carts[user_id] = []
        user_sessions.pop(user_id, None)

    @bot.on_callback("back_to_categories")
    async def back_to_categories_handler(event):
        user_id = event.user_id
        user_sessions[user_id]["state"] = ShopStates.BROWSING
        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["catalog"],
            keyboard=kb.get_categories_keyboard()
        )

    @bot.on_callback("back_to_products")
    async def back_to_products_handler(event):
        user_id = event.user_id
        category_id = user_sessions.get(user_id, {}).get("current_category")
        if category_id:
            await event.bot.send_message(
                user_id=user_id,
                text="📁 Выберите товар:",
                keyboard=kb.get_products_keyboard(category_id)
            )

    @bot.on_callback("about")
    async def about_handler(event):
        await event.bot.send_message(
            user_id=event.user_id,
            text=f"🛍 *О магазине {SHOP_SETTINGS['name']}*\n\n"
                 "Мы предлагаем качественные товары по доступным ценам."
        )

    @bot.on_callback("cancel_order")
    async def cancel_order_handler(event):
        user_id = event.user_id
        user_sessions.pop(user_id, None)
        await event.bot.send_message(
            user_id=user_id,
            text="❌ Оформление заказа отменено",
            keyboard=kb.get_main_menu()
        )