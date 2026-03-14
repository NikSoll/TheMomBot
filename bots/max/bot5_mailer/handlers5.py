import asyncio
from datetime import datetime
from config5 import MAILER_SETTINGS, MESSAGES, GROUPS, ADMIN_ID
from . import keyboards5 as kb
from . import utils5
from .states5 import MailerStates
from .database5 import db


def register_handlers(bot):
    @bot.on_message("text")
    async def message_handler(event):
        user_id = event.user_id
        text = event.text

        if text == "/start":
            await start_handler(event, bot)

    @bot.on_callback("start")
    async def start_handler(event, bot=None):
        user_id = event.user_id

        if MAILER_SETTINGS.get("subscribe_on_start"):
            db.add_subscriber(
                user_id,
                event.username or "",
                event.full_name or ""
            )
            welcome_text = f"{MAILER_SETTINGS['welcome_message']}\n\n{MESSAGES['subscribed']}"
        else:
            welcome_text = MESSAGES["welcome"]

        is_admin = str(user_id) == ADMIN_ID
        await event.bot.send_message(
            user_id=user_id,
            text=welcome_text,
            keyboard=kb.get_main_menu(is_admin)
        )

    @bot.on_callback("subscribe")
    async def subscribe_handler(event):
        user_id = event.user_id
        username = event.username or ""
        full_name = event.full_name or ""

        if db.is_subscribed(user_id):
            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["already_subscribed"]
            )
        else:
            db.add_subscriber(user_id, username, full_name)
            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["subscribed"]
            )

    @bot.on_callback("unsubscribe")
    async def unsubscribe_handler(event):
        user_id = event.user_id

        if db.is_subscribed(user_id):
            db.remove_subscriber(user_id)
            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["unsubscribed"]
            )
        else:
            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["not_subscribed"]
            )

    @bot.on_callback("my_subscriptions")
    async def my_subscriptions_handler(event):
        user_id = event.user_id

        if db.is_subscribed(user_id):
            await event.bot.send_message(
                user_id=user_id,
                text="✅ Вы подписаны на рассылку\n\nХотите отписаться? Нажмите ❌ Отписаться"
            )
        else:
            await event.bot.send_message(
                user_id=user_id,
                text="❌ Вы не подписаны на рассылку\n\nХотите подписаться? Нажмите ✅ Подписаться"
            )

    @bot.on_callback("stats")
    async def stats_handler(event):
        user_id = event.user_id
        if str(user_id) != ADMIN_ID:
            await event.bot.send_message(
                user_id=user_id,
                text="⛔️ Нет доступа"
            )
            return

        stats = db.get_stats()
        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["stats"].format(total=stats['total'], active=stats['active'])
        )

    @bot.on_callback("create_mailing")
    async def create_mailing_handler(event, state=None):
        user_id = event.user_id
        if str(user_id) != ADMIN_ID:
            await event.bot.send_message(
                user_id=user_id,
                text="⛔️ Нет доступа"
            )
            return

        await event.bot.send_message(
            user_id=user_id,
            text="Выберите группу для рассылки:",
            keyboard=kb.get_groups_keyboard()
        )
        # Здесь нужно сохранить состояние
        user_sessions[user_id] = {"state": "choosing_group"}

    @bot.on_callback_pattern(r"group_(\d+)")
    async def choose_group_handler(event, group_id):
        user_id = event.user_id
        group_id = int(group_id)
        group = next((g for g in GROUPS if g['id'] == group_id), None)

        if group_id == 1:
            subscribers = db.get_all_subscribers()
        else:
            subscribers = []  # Для других групп

        user_sessions[user_id] = {
            "state": "entering_text",
            "group_id": group_id,
            "group_name": group['name'] if group else "Все",
            "subscribers": subscribers,
            "total": len(subscribers)
        }

        await event.bot.send_message(
            user_id=user_id,
            text=f"📨 *Создание рассылки*\n\n"
                 f"Группа: *{group['name'] if group else 'Все'}*\n"
                 f"Подписчиков: *{len(subscribers)}*\n\n"
                 f"Введите текст рассылки:"
        )

    @bot.on_message("text")
    async def mailing_text_handler(event):
        user_id = event.user_id
        session = user_sessions.get(user_id)

        if session and session.get("state") == "entering_text":
            session["text"] = event.text
            session["state"] = "entering_photo"
            await event.bot.send_message(
                user_id=user_id,
                text="📎 Отправьте фото для рассылки (или отправьте '-' чтобы пропустить):"
            )

    @bot.on_message("text")
    async def mailing_photo_handler(event):
        user_id = event.user_id
        session = user_sessions.get(user_id)

        if session and session.get("state") == "entering_photo":
            photo_id = None
            if event.text == "-":
                photo_id = None
            else:
                await event.bot.send_message(
                    user_id=user_id,
                    text="Пожалуйста, отправьте фото или '-'"
                )
                return

            session["photo_id"] = photo_id
            session["state"] = "confirm"

            preview = f"📨 *Предпросмотр рассылки*\n\n"
            preview += f"Группа: *{session.get('group_name')}*\n"
            preview += f"Получателей: *{session.get('total')}*\n\n"
            preview += f"*Текст:*\n{session.get('text')}\n"

            if photo_id:
                preview += "\n*+ Фото*"

            await event.bot.send_message(
                user_id=user_id,
                text=preview,
                keyboard=kb.get_mailing_confirm_keyboard()
            )

    @bot.on_callback("mailing_send")
    async def send_mailing_handler(event):
        user_id = event.user_id
        session = user_sessions.get(user_id)

        if not session:
            return

        subscribers = session.get('subscribers', [])
        text = session.get('text')
        photo_id = session.get('photo_id')

        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["mailing_start"].format(sent=0, failed=0)
        )

        sent = 0
        failed = 0

        for subscriber in subscribers:
            try:
                if photo_id:
                    # Отправка с фото
                    await event.bot.send_message(
                        user_id=subscriber['user_id'],
                        text=text
                    )
                else:
                    await event.bot.send_message(
                        user_id=subscriber['user_id'],
                        text=text
                    )
                sent += 1
            except Exception as e:
                failed += 1
                print(f"Ошибка отправки {subscriber['user_id']}: {e}")

            await asyncio.sleep(0.05)

        db.save_mailing({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'group': session.get('group_name'),
            'text': text,
            'total': session.get('total'),
            'sent': sent,
            'failed': failed
        })

        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["mailing_complete"].format(
                total=session.get('total'),
                sent=sent,
                failed=failed
            )
        )

        user_sessions.pop(user_id, None)

    @bot.on_callback("mailing_cancel")
    async def cancel_mailing_handler(event):
        user_id = event.user_id
        user_sessions.pop(user_id, None)
        await event.bot.send_message(
            user_id=user_id,
            text="❌ Рассылка отменена"
        )


user_sessions = {}