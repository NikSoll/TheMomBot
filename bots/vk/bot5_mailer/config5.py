import os
from dotenv import load_dotenv

load_dotenv()

VK_TOKEN = "{{VK_TOKEN}}"
GROUP_ID = "{{GROUP_ID}}"
ADMIN_ID = "6496349641"

MAILER_SETTINGS = {
    "name": "Рассыльщик",
    "admin_chat_id": ADMIN_ID,
    "subscribe_on_start": True,  #рег при старт
    "welcome_message": "👋 Добро пожаловать! Вы подписались на наши новости.",
}

MESSAGES = {
    "welcome": "📢 *Добро пожаловать в бот-рассыльщик!*\n\nЗдесь вы можете подписаться на новости и получать уведомления.",
    "subscribed": "✅ Вы успешно подписались на рассылку!",
    "unsubscribed": "❌ Вы отписались от рассылки. Будем ждать вас снова!",
    "already_subscribed": "ℹ️ Вы уже подписаны на рассылку",
    "not_subscribed": "ℹ️ Вы не подписаны на рассылку",
    "stats": "📊 *Статистика*\n\n👥 Всего подписчиков: {total}\n✅ Активных: {active}",
    "mailing_start": "📨 Рассылка начата. Отправлено: {sent} | Ошибок: {failed}",
    "mailing_complete": "✅ Рассылка завершена!\n\nВсего: {total}\n✅ Доставлено: {sent}\n❌ Ошибок: {failed}",
}

#подписота
GROUPS = [
    {"id": 1, "name": "Все подписчики"},
    {"id": 2, "name": "Новости"},
    {"id": 3, "name": "Акции"},
    {"id": 4, "name": "Мероприятия"},
]