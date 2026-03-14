from config5 import GROUPS


def get_main_menu(is_admin=False):
    keyboard = [
        [{"text": "✅ Подписаться", "data": "subscribe"}],
        [{"text": "❌ Отписаться", "data": "unsubscribe"}],
        [{"text": "📋 Мои подписки", "data": "my_subscriptions"}],
    ]

    if is_admin:
        keyboard.append([{"text": "📊 Статистика", "data": "stats"}])
        keyboard.append([{"text": "📨 Создать рассылку", "data": "create_mailing"}])

    return keyboard


def get_groups_keyboard():
    keyboard = []
    for group in GROUPS:
        keyboard.append([{
            "text": group['name'],
            "data": f"group_{group['id']}"
        }])
    return keyboard


def get_mailing_confirm_keyboard():
    return [
        [{"text": "✅ Отправить", "data": "mailing_send"}],
        [{"text": "❌ Отмена", "data": "mailing_cancel"}],
    ]