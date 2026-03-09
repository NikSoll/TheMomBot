from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime

from . import keyboards1 as kb
from . import utils1
from .states1 import BookingStates
from .config1 import SALON_SETTINGS, MESSAGES
from .database1 import db


def register_handlers(dp):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            MESSAGES["welcome"].format(name=SALON_SETTINGS["name"]),
            reply_markup=kb.get_main_menu(),
            parse_mode="Markdown"
        )

    @dp.message(F.text == "📝 Записаться")
    async def start_booking(message: types.Message, state: FSMContext):
        await message.answer(
            MESSAGES["choose_master"],
            reply_markup=kb.get_masters_keyboard(),
            parse_mode="Markdown"
        )
        await state.set_state(BookingStates.choosing_master)

    @dp.callback_query(F.data.startswith("master_"))
    async def choose_master(callback: types.CallbackQuery, state: FSMContext):
        master_id = int(callback.data.split("_")[1])
        master = utils1.get_master_by_id(master_id)

        if master:
            await state.update_data(master=master["name"], master_id=master_id)

            await callback.message.edit_text(
                f"👩‍🎨 Выбран мастер: *{master['emoji']} {master['name']}*\n\n"
                f"{MESSAGES['choose_date']}",
                reply_markup=kb.get_dates_keyboard(),
                parse_mode="Markdown"
            )
            await state.set_state(BookingStates.choosing_date)
        await callback.answer()

    @dp.callback_query(F.data.startswith("date_"))
    async def choose_date(callback: types.CallbackQuery, state: FSMContext):
        date = callback.data.split("_")[1]
        await state.update_data(date=date)

        await callback.message.edit_text(
            f"📅 Выбрана дата: *{utils1.format_date(date)}*\n\n"
            f"{MESSAGES['choose_time']}",
            reply_markup=kb.get_times_keyboard(),
            parse_mode="Markdown"
        )
        await state.set_state(BookingStates.choosing_time)
        await callback.answer()

    @dp.callback_query(F.data.startswith("time_"))
    async def choose_time(callback: types.CallbackQuery, state: FSMContext):
        time = callback.data.split("_")[1]
        await state.update_data(time=time)

        data = await state.get_data()

        await callback.message.edit_text(
            f"✅ *Предварительные данные:*\n"
            f"• Мастер: {data.get('master')}\n"
            f"• Дата: {utils1.format_date(data.get('date'))}\n"
            f"• Время: {time}\n\n"
            f"{MESSAGES['enter_name']}",
            parse_mode="Markdown"
        )
        await state.set_state(BookingStates.entering_name)
        await callback.answer()

    @dp.message(BookingStates.entering_name)
    async def enter_name(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer(
            MESSAGES["enter_phone"],
            parse_mode="Markdown",
            reply_markup=kb.get_cancel_keyboard()
        )
        await state.set_state(BookingStates.entering_phone)

    @dp.message(BookingStates.entering_phone)
    async def enter_phone(message: types.Message, state: FSMContext):
        await state.update_data(phone=message.text)
        await message.answer(
            MESSAGES["enter_comment"],
            parse_mode="Markdown"
        )
        await state.set_state(BookingStates.entering_comment)

    @dp.message(BookingStates.entering_comment)
    async def enter_comment(message: types.Message, state: FSMContext):
        comment = message.text if message.text != "-" else ""

        data = await state.get_data()
        booking_data = {
            'user_id': message.from_user.id,
            'username': message.from_user.username or "",
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
            await message.answer(
                MESSAGES["booking_success"].format(
                    master=booking_data['master'],
                    date=utils1.format_date(booking_data['date']),
                    time=booking_data['time'],
                    phone=booking_data['phone']
                ),
                reply_markup=kb.get_main_menu(),
                parse_mode="Markdown"
            )

            if SALON_SETTINGS.get('admin_chat_id'):
                try:
                    admin_text = (f"📥 *Новая запись!*\n\n"
                                  f"• Клиент: {booking_data['name']}\n"
                                  f"• Телефон: {booking_data['phone']}\n"
                                  f"• Мастер: {booking_data['master']}\n"
                                  f"• Дата: {utils1.format_date(booking_data['date'])} {booking_data['time']}\n"
                                  f"• Комментарий: {booking_data['comment'] or 'нет'}")
                    await message.bot.send_message(
                        SALON_SETTINGS['admin_chat_id'],
                        admin_text,
                        parse_mode="Markdown"
                    )
                except:
                    pass
        else:
            await message.answer(
                MESSAGES["booking_error"].format(phone=SALON_SETTINGS['phone']),
                reply_markup=kb.get_main_menu(),
                parse_mode="Markdown"
            )

        await state.clear()

    @dp.message(F.text == "📋 Мои записи")
    async def my_bookings(message: types.Message):
        bookings = db.get_user_bookings(message.from_user.id)

        if not bookings:
            await message.answer(
                MESSAGES["no_bookings"],
                parse_mode="Markdown"
            )
            return

        bookings_text = utils1.format_bookings_list(bookings[:5])
        await message.answer(
            MESSAGES["my_bookings"].format(bookings=bookings_text),
            parse_mode="Markdown"
        )

    @dp.message(F.text == "ℹ️ О салоне")
    async def about(message: types.Message):
        await message.answer(
            MESSAGES["about"].format(
                address=SALON_SETTINGS['address'],
                hours=SALON_SETTINGS['working_hours'],
                phone=SALON_SETTINGS['phone']
            ),
            parse_mode="Markdown"
        )

    @dp.message(F.text == "📞 Контакты")
    async def contacts(message: types.Message):
        await message.answer(
            MESSAGES["contacts"].format(
                address=SALON_SETTINGS['address'],
                hours=SALON_SETTINGS['working_hours'],
                phone=SALON_SETTINGS['phone']
            ),
            parse_mode="Markdown"
        )

    @dp.message(F.text == "❌ Отменить запись")
    async def cancel_booking(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "❌ Оформление записи отменено",
            reply_markup=kb.get_main_menu()
        )

    @dp.callback_query(F.data == "back_to_masters")
    async def back_to_masters(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text(
            MESSAGES["choose_master"],
            reply_markup=kb.get_masters_keyboard(),
            parse_mode="Markdown"
        )
        await state.set_state(BookingStates.choosing_master)
        await callback.answer()

    @dp.callback_query(F.data == "back_to_dates")
    async def back_to_dates(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text(
            MESSAGES["choose_date"],
            reply_markup=kb.get_dates_keyboard(),
            parse_mode="Markdown"
        )
        await state.set_state(BookingStates.choosing_date)
        await callback.answer()

    @dp.message(Command("admin"))
    async def admin_panel(message: types.Message):
        if str(message.from_user.id) != SALON_SETTINGS.get('admin_chat_id'):
            await message.answer("⛔️ Нет доступа")
            return

        bookings = db.get_today_bookings()

        if not bookings:
            text = "📭 *Сегодня записей нет*"
        else:
            text = "📊 *Записи на сегодня:*\n\n"
            for i, booking in enumerate(bookings, 1):
                text += (f"{i}. {booking.get('Время', '')} - {booking.get('Имя', '')}\n"
                         f"   📞 {booking.get('Телефон', '')}\n"
                         f"   👩‍🎨 {booking.get('Мастер', '')}\n\n")

        await message.answer(text, parse_mode="Markdown")