import json
from datetime import datetime
from max_sdk import MaxBot
from config1 import MESSAGES, SALON_SETTINGS, ADMIN_ID
from . import keyboards1 as kb
from . import utils1
from .states1 import BookingStates
from .database1 import db

user_sessions = {}


def register_handlers(bot: MaxBot):
    @bot.on_message("text")
    async def message_handler(event):
        user_id = event.user_id
        text = event.text

        session = user_sessions.get(user_id, {"state": None})

        if text == "/start":
            await start_handler(event, bot)
        elif session.get("state") == BookingStates.ENTERING_NAME:
            await enter_name(event, bot)
        elif session.get("state") == BookingStates.ENTERING_PHONE:
            await enter_phone(event, bot)
        elif session.get("state") == BookingStates.ENTERING_COMMENT:
            await enter_comment(event, bot)
        else:
            await start_handler(event, bot)

    @bot.on_callback("book")
    async def book_handler(event):
        user_id = event.user_id
        user_sessions[user_id] = {"state": BookingStates.CHOOSING_MASTER}

        await bot.send_message(
            user_id=user_id,
            text=MESSAGES["choose_master"],
            keyboard=kb.get_masters_keyboard()
        )

    @bot.on_callback_pattern(r"master_(\d+)")
    async def master_handler(event, master_id):
        user_id = event.user_id
        master = utils.get_master_by_id(int(master_id))

        if master:
            user_sessions[user_id]["master"] = master["name"]
            user_sessions[user_id]["state"] = BookingStates.CHOOSING_DATE

            await bot.send_message(
                user_id=user_id,
                text=f"👩‍🎨 Выбран мастер: {master['emoji']} {master['name']}\n\n{MESSAGES['choose_date']}",
                keyboard=kb.get_dates_keyboard()
            )

    @bot.on_callback_pattern(r"date_(\d{4}-\d{2}-\d{2})")
    async def date_handler(event, date_str):
        user_id = event.user_id
        user_sessions[user_id]["date"] = date_str
        user_sessions[user_id]["state"] = BookingStates.CHOOSING_TIME

        await bot.send_message(
            user_id=user_id,
            text=f"📅 Выбрана дата: {utils.format_date(date_str)}\n\n{MESSAGES['choose_time']}",
            keyboard=kb.get_times_keyboard()
        )

    @bot.on_callback_pattern(r"time_(\d{2}:\d{2})")
    async def time_handler(event, time_str):
        user_id = event.user_id
        user_sessions[user_id]["time"] = time_str
        user_sessions[user_id]["state"] = BookingStates.ENTERING_NAME

        data = user_sessions[user_id]
        await bot.send_message(
            user_id=user_id,
            text=f"✅ *Предварительные данные:*\n"
                 f"• Мастер: {data.get('master')}\n"
                 f"• Дата: {utils.format_date(data.get('date'))}\n"
                 f"• Время: {time_str}\n\n"
                 f"{MESSAGES['enter_name']}"
        )

    async def enter_name(event):
        user_id = event.user_id
        user_sessions[user_id]["name"] = event.text
        user_sessions[user_id]["state"] = BookingStates.ENTERING_PHONE

        await bot.send_message(
            user_id=user_id,
            text=MESSAGES["enter_phone"],
            keyboard=kb.get_cancel_keyboard()
        )

    async def enter_phone(event):
        user_id = event.user_id
        user_sessions[user_id]["phone"] = event.text
        user_sessions[user_id]["state"] = BookingStates.ENTERING_COMMENT

        await bot.send_message(
            user_id=user_id,
            text=MESSAGES["enter_comment"]
        )

    async def enter_comment(event):
        user_id = event.user_id
        comment = event.text if event.text != "-" else ""

        data = user_sessions.get(user_id, {})
        booking_data = {
            'user_id': user_id,
            'username': event.username or "",
            'name': data.get('name'),
            'phone': data.get('phone'),
            'master': data.get('master'),
            'date': data.get('date'),
            'time': data.get('time'),
            'comment': comment,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        success = db.add_booking(booking_data)

        if success:
            await bot.send_message(
                user_id=user_id,
                text=MESSAGES["booking_success"].format(
                    master=booking_data['master'],
                    date=utils.format_date(booking_data['date']),
                    time=booking_data['time'],
                    phone=booking_data['phone']
                ),
                keyboard=kb.get_main_menu()
            )

            if ADMIN_ID:
                admin_text = (f"📥 *Новая запись!*\n\n"
                              f"• Клиент: {booking_data['name']}\n"
                              f"• Телефон: {booking_data['phone']}\n"
                              f"• Мастер: {booking_data['master']}\n"
                              f"• Дата: {utils.format_date(booking_data['date'])} {booking_data['time']}\n"
                              f"• Комментарий: {booking_data['comment'] or 'нет'}")
                await bot.send_message(
                    user_id=ADMIN_ID,
                    text=admin_text
                )
        else:
            await bot.send_message(
                user_id=user_id,
                text=MESSAGES["booking_error"].format(phone=SALON_SETTINGS['phone']),
                keyboard=kb.get_main_menu()
            )

        user_sessions.pop(user_id, None)

    @bot.on_callback("my_bookings")
    async def my_bookings_handler(event):
        user_id = event.user_id
        bookings = db.get_user_bookings(user_id)

        if not bookings:
            await bot.send_message(
                user_id=user_id,
                text=MESSAGES["no_bookings"]
            )
        else:
            text = MESSAGES["my_bookings"].format(
                bookings=utils.format_bookings_list(bookings)
            )
            await bot.send_message(
                user_id=user_id,
                text=text
            )

    @bot.on_callback("about")
    async def about_handler(event):
        await bot.send_message(
            user_id=event.user_id,
            text=MESSAGES["about"].format(
                address=SALON_SETTINGS['address'],
                hours=SALON_SETTINGS['working_hours'],
                phone=SALON_SETTINGS['phone']
            )
        )

    @bot.on_callback("back_to_masters")
    async def back_to_masters(event):
        await bot.send_message(
            user_id=event.user_id,
            text=MESSAGES["choose_master"],
            keyboard=kb.get_masters_keyboard()
        )

    @bot.on_callback("back_to_dates")
    async def back_to_dates(event):
        await bot.send_message(
            user_id=event.user_id,
            text=MESSAGES["choose_date"],
            keyboard=kb.get_dates_keyboard()
        )

    @bot.on_callback("cancel_booking")
    async def cancel_booking(event):
        user_id = event.user_id
        user_sessions.pop(user_id, None)
        await bot.send_message(
            user_id=user_id,
            text="❌ Оформление записи отменено",
            keyboard=kb.get_main_menu()
        )