from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime

from . import keyboards2 as kb
from . import utils2
from .states2 import ShopStates
from .config2 import SHOP_SETTINGS, MESSAGES

#затычка бд
user_carts = {}

#все обработч
def register_handlers(dp):
    @dp.message(Command("shop"))
    @dp.message(F.text == "🛍 Каталог")
    #старт
    async def shop_start(message: types.Message, state: FSMContext):
        await message.answer(
            MESSAGES["catalog"],
            reply_markup=kb.get_categories_keyboard(),
            parse_mode="Markdown"
        )
        await state.set_state(ShopStates.browsing)


    @dp.callback_query(F.data.startswith("shop_cat_"), ShopStates.browsing)
    #отображ выбран каты
    async def show_category(callback: types.CallbackQuery, state: FSMContext):
        category_id = int(callback.data.split("_")[2])

        category = utils2.get_category_by_id(category_id)
        if category:
            await state.update_data(current_category=category_id)

            await callback.message.edit_text(
                f"📁 *{category['emoji']} {category['name']}*\n\n"
                f"Выберите товар:",
                reply_markup=kb.get_products_keyboard(category_id),
                parse_mode="Markdown"
            )
        await callback.answer()


    #отображ детаил продукт
    @dp.callback_query(F.data.startswith("shop_prod_"))
    async def show_product(callback: types.CallbackQuery, state: FSMContext):
        product_id = int(callback.data.split("_")[2])
        product = utils2.get_product_by_id(product_id)

        if product:
            await state.update_data(current_product=product_id)

            text = MESSAGES["product_info"].format(
                name=product['name'],
                price=product['price'],
                currency=SHOP_SETTINGS['currency'],
                desc=product['desc']
            )

            await callback.message.edit_text(
                text,
                reply_markup=kb.get_product_detail_keyboard(product_id),
                parse_mode="Markdown"
            )
            await state.set_state(ShopStates.viewing_product)
        await callback.answer()


    #+ в корзину
    @dp.callback_query(F.data.startswith("shop_add_"))
    async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
        product_id = int(callback.data.split("_")[2])
        user_id = callback.from_user.id

        product = utils2.get_product_by_id(product_id)
        if not product:
            await callback.answer("Товар не найден")
            return

        #корзина юзера
        cart = user_carts.get(user_id, [])

        #+ товар
        cart.append({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"]
        })

        user_carts[user_id] = cart

        await callback.answer(f"✅ {product['name']} добавлен в корзину!")

        #к списку продук
        data = await state.get_data()
        category_id = data.get("current_category")

        if category_id:
            await callback.message.edit_text(
                f"📁 *Выберите товар:*",
                reply_markup=kb.get_products_keyboard(category_id),
                parse_mode="Markdown"
            )
            await state.set_state(ShopStates.browsing)


    #содер корзины
    @dp.message(F.text == "🛒 Корзина")
    @dp.callback_query(F.data == "shop_view_cart")
    async def show_cart(event: types.Message | types.CallbackQuery, state: FSMContext):
        user_id = event.from_user.id
        cart = user_carts.get(user_id, [])

        if not cart:
            text = MESSAGES["cart_empty"]
            reply_markup = None

            if isinstance(event, types.CallbackQuery):
                await event.message.edit_text(text, parse_mode="Markdown")
                await event.answer()
            else:
                await event.answer(text, parse_mode="Markdown")
            return

        total = utils2.calculate_total(cart)
        cart_text = utils2.format_cart(cart)

        text = MESSAGES["cart"].format(
            cart=cart_text,
            total=total,
            currency=SHOP_SETTINGS['currency']
        )

        if isinstance(event, types.CallbackQuery):
            await event.message.edit_text(
                text,
                reply_markup=kb.get_cart_keyboard(),
                parse_mode="Markdown"
            )
            await event.answer()
        else:
            await event.answer(
                text,
                reply_markup=kb.get_cart_keyboard(),
                parse_mode="Markdown"
            )

        await state.set_state(ShopStates.in_cart)


    #дел колрзин
    @dp.callback_query(F.data == "shop_clear_cart")
    async def clear_cart(callback: types.CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        user_carts[user_id] = []

        await callback.message.edit_text(
            "🗑 *Корзина очищена*",
            parse_mode="Markdown"
        )
        await callback.answer()

    #нач оформ зааказ
    @dp.callback_query(F.data == "shop_checkout")
    async def start_checkout(callback: types.CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        cart = user_carts.get(user_id, [])

        if not cart:
            await callback.message.edit_text("Корзина пуста!")
            await callback.answer()
            return

        await callback.message.edit_text(
            MESSAGES["ask_name"],
            parse_mode="Markdown"
        )
        await state.set_state(ShopStates.entering_name)
        await callback.answer()

    #валид имя
    @dp.message(ShopStates.entering_name)
    async def process_name(message: types.Message, state: FSMContext):
        await state.update_data(customer_name=message.text)
        await message.answer(
            MESSAGES["ask_phone"],
            parse_mode="Markdown",
            reply_markup=kb.get_cancel_keyboard()
        )
        await state.set_state(ShopStates.entering_phone)

    #валид телефон
    @dp.message(ShopStates.entering_phone)
    async def process_phone(message: types.Message, state: FSMContext):
        await state.update_data(customer_phone=message.text)
        await message.answer(
            MESSAGES["ask_address"],
            parse_mode="Markdown"
        )
        await state.set_state(ShopStates.entering_address)

    #валид адрес
    @dp.message(ShopStates.entering_address)
    async def process_address(message: types.Message, state: FSMContext):
        await state.update_data(customer_address=message.text)
        await message.answer(
            "💬 *Добавьте комментарий к заказу (если нужно):*\n"
            "Или отправьте '-'",
            parse_mode="Markdown"
        )
        await state.set_state(ShopStates.entering_comment)

    #валид и сайв заказ
    @dp.message(ShopStates.entering_comment)
    async def process_comment(message: types.Message, state: FSMContext):
        comment = message.text if message.text != "-" else ""

        #все даные
        data = await state.get_data()
        user_id = message.from_user.id
        cart = user_carts.get(user_id, [])

        #сам заказ
        order = {
            'user_id': user_id,
            'username': message.from_user.username or "",
            'name': data.get('customer_name'),
            'phone': data.get('customer_phone'),
            'address': data.get('customer_address'),
            'comment': comment,
            'cart': cart.copy(),
            'total': utils2.calculate_total(cart),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        #сейв в БД
        #в основе db.add_order(order)

        #детали заказа(нужно больше смайликов!!!!)
        cart_text = utils2.format_cart(order['cart'])
        order_details = (
            f"*Ваш заказ:*\n"
            f"{cart_text}\n"
            f"💰 *Итого: {order['total']}{SHOP_SETTINGS['currency']}*\n\n"
            f"📞 *Телефон:* {order['phone']}\n"
            f"📍 *Адрес:* {order['address']}"
        )

        await message.answer(
            MESSAGES["order_success"].format(order_details=order_details),
            reply_markup=kb.get_main_menu(),
            parse_mode="Markdown"
        )

        #логи
        if SHOP_SETTINGS.get('admin_chat_id'):
            try:
                admin_text = f"🛍 *Новый заказ!*\n\n{order_details}"
                await message.bot.send_message(
                    SHOP_SETTINGS['admin_chat_id'],
                    admin_text,
                    parse_mode="Markdown"
                )
            except:
                pass

        #клин корзины
        user_carts[user_id] = []
        await state.clear()

    #отмена заказа
    @dp.message(F.text == "❌ Отменить заказ")
    async def cancel_order(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "❌ Оформление заказа отменено",
            reply_markup=kb.get_main_menu()
        )

    #авигация к кате
    @dp.callback_query(F.data == "shop_back_to_categories")
    async def back_to_categories(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text(
            MESSAGES["catalog"],
            reply_markup=kb.get_categories_keyboard(),
            parse_mode="Markdown"
        )
        await state.set_state(ShopStates.browsing)
        await callback.answer()

    #возврат
    @dp.callback_query(F.data == "shop_back_to_products")
    async def back_to_products(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        category_id = data.get("current_category")

        if category_id:
            await callback.message.edit_text(
                f"📁 *Выберите товар:*",
                reply_markup=kb.get_products_keyboard(category_id),
                parse_mode="Markdown"
            )
            await state.set_state(ShopStates.browsing)
        await callback.answer()

    #эбаут (если надо пользователь сам добавит смайлов)
    @dp.message(F.text == "О магазине")
    async def about(message: types.Message):
        await message.answer(
            f"🛍 *О магазине {SHOP_SETTINGS['name']}*\n\n"
            "Мы предлагаем качественные товары по доступным ценам.\n"
            "• Доставка по городу\n"
            "• Оплата при получении\n"
            "• Гарантия качества",
            parse_mode="Markdown"
        )

    #лааадно тут добавлю(это никто кроме меня не прочитает)
    @dp.message(F.text == "📞 Контакты")
    async def contacts(message: types.Message):
        await message.answer(
            "📞 *Контакты*\n\n"
            "📍 Адрес: г. Омск, ул. Масленникова, д. 45\n"
            "🕐 Часы работы: 10:00 - 20:00\n"
            "📞 Телефон: +7 (905) 190-01-54",
            parse_mode="Markdown"
        )