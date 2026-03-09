from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import asyncio
from datetime import datetime

from . import keyboards5 as kb
from . import utils5
from .states5 import MailerStates
from .config5 import MAILER_SETTINGS, MESSAGES, GROUPS, ADMIN_ID
from .database5 import db


def register_handlers(dp):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message, state: FSMContext):
        await state.clear()

        # Автоподписка
        if MAILER_SETTINGS.get("subscribe_on_start"):
            db.add_subscriber(
                message.from_user.id,
                message.from_user.username or "",
                message.from_user.full_name
            )
            welcome_text = f"{MAILER_SETTINGS['welcome_message']}\n\n{MESSAGES['subscribed']}"
        else:
            welcome_text = MESSAGES["welcome"]

        await message.answer(
            welcome_text,
            reply_markup=kb.get_main_menu(is_admin=str(message.from_user.id) == ADMIN_ID),
            parse_mode="Markdown"
        )

    @dp.message(F.text == "✅ Подписаться")
    async def subscribe(message: types.Message):
        user_id = message.from_user.id
        username = message.from_user.username or ""
        full_name = message.from_user.full_name

        if db.is_subscribed(user_id):
            await message.answer(MESSAGES["already_subscribed"])
        else:
            db.add_subscriber(user_id, username, full_name)
            await message.answer(MESSAGES["subscribed"])

    @dp.message(F.text == "❌ Отписаться")
    async def unsubscribe(message: types.Message):
        user_id = message.from_user.id

        if db.is_subscribed(user_id):
            db.remove_subscriber(user_id)
            await message.answer(MESSAGES["unsubscribed"])
        else:
            await message.answer(MESSAGES["not_subscribed"])

    @dp.message(F.text == "📊 Статистика")
    async def show_stats(message: types.Message):
        if str(message.from_user.id) != ADMIN_ID:
            await message.answer("⛔️ Нет доступа")
            return

        stats = db.get_stats()
        await message.answer(
            MESSAGES["stats"].format(total=stats['total'], active=stats['active']),
            parse_mode="Markdown"
        )

    @dp.message(F.text == "📨 Создать рассылку")
    async def create_mailing(message: types.Message, state: FSMContext):
        if str(message.from_user.id) != ADMIN_ID:
            await message.answer("⛔️ Нет доступа")
            return

        await message.answer(
            "Выберите группу для рассылки:",
            reply_markup=kb.get_groups_keyboard()
        )
        await state.set_state(MailerStates.choosing_group)

    @dp.callback_query(F.data.startswith("group_"), MailerStates.choosing_group)
    async def choose_group(callback: types.CallbackQuery, state: FSMContext):
        group_id = int(callback.data.split("_")[1])
        group = next((g for g in GROUPS if g['id'] == group_id), None)

        if group_id == 1:  # Все подписчики
            subscribers = db.get_all_subscribers()
        else:
            subscribers = db.get_group_subscribers(group_id)

        await state.update_data(
            group_id=group_id,
            group_name=group['name'] if group else "Все",
            subscribers=subscribers,
            total=len(subscribers)
        )

        await callback.message.edit_text(
            f"📨 *Создание рассылки*\n\n"
            f"Группа: *{group['name'] if group else 'Все'}*\n"
            f"Подписчиков: *{len(subscribers)}*\n\n"
            f"Введите текст рассылки:",
            parse_mode="Markdown"
        )
        await state.set_state(MailerStates.entering_text)
        await callback.answer()

    @dp.message(MailerStates.entering_text)
    async def enter_text(message: types.Message, state: FSMContext):
        await state.update_data(text=message.text)

        await message.answer(
            "📎 Отправьте фото для рассылки (или отправьте '-' чтобы пропустить):"
        )
        await state.set_state(MailerStates.entering_photo)

    @dp.message(MailerStates.entering_photo)
    async def enter_photo(message: types.Message, state: FSMContext):
        photo_id = None
        if message.photo:
            photo_id = message.photo[-1].file_id
        elif message.text == "-":
            photo_id = None
        else:
            await message.answer("Пожалуйста, отправьте фото или '-'")
            return

        await state.update_data(photo_id=photo_id)

        data = await state.get_data()

        preview = f"📨 *Предпросмотр рассылки*\n\n"
        preview += f"Группа: *{data.get('group_name')}*\n"
        preview += f"Получателей: *{data.get('total')}*\n\n"
        preview += f"*Текст:*\n{data.get('text')}\n"

        if photo_id:
            preview += "\n*+ Фото*"

        await message.answer(
            preview,
            reply_markup=kb.get_mailing_confirm_keyboard(),
            parse_mode="Markdown"
        )
        await state.set_state(MailerStates.confirm)

    @dp.callback_query(F.data == "mailing_send", MailerStates.confirm)
    async def send_mailing(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        subscribers = data.get('subscribers', [])
        text = data.get('text')
        photo_id = data.get('photo_id')

        await callback.message.edit_text(
            MESSAGES["mailing_start"].format(sent=0, failed=0)
        )

        sent = 0
        failed = 0

        for subscriber in subscribers:
            try:
                if photo_id:
                    await callback.bot.send_photo(
                        subscriber['user_id'],
                        photo_id,
                        caption=text,
                        parse_mode="Markdown"
                    )
                else:
                    await callback.bot.send_message(
                        subscriber['user_id'],
                        text,
                        parse_mode="Markdown"
                    )
                sent += 1
            except Exception as e:
                failed += 1
                print(f"Ошибка отправки {subscriber['user_id']}: {e}")

            await asyncio.sleep(0.05)  # Anti-flood

        db.save_mailing({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'group': data.get('group_name'),
            'text': text,
            'total': data.get('total'),
            'sent': sent,
            'failed': failed
        })

        await callback.message.answer(
            MESSAGES["mailing_complete"].format(
                total=data.get('total'),
                sent=sent,
                failed=failed
            ),
            parse_mode="Markdown"
        )

        await state.clear()
        await callback.answer()

    @dp.callback_query(F.data == "mailing_cancel", MailerStates.confirm)
    async def cancel_mailing(callback: types.CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("❌ Рассылка отменена")
        await callback.answer()

    @dp.message(F.text == "📋 Мои подписки")
    async def my_subscriptions(message: types.Message):
        if db.is_subscribed(message.from_user.id):
            await message.answer(
                "✅ Вы подписаны на рассылку\n\n"
                "Хотите отписаться? Нажмите ❌ Отписаться"
            )
        else:
            await message.answer(
                "❌ Вы не подписаны на рассылку\n\n"
                "Хотите подписаться? Нажмите ✅ Подписаться"
            )