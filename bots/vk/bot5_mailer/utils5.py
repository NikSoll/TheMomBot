def format_subscribers_list(subscribers):
    if not subscribers:
        return "Нет подписчиков"

    lines = []
    for i, sub in enumerate(subscribers[:10], 1):
        name = sub.get('name', sub.get('username', 'Неизвестно'))
        user_id = sub.get('user_id', '')
        lines.append(f"{i}. {name} (ID: {user_id})")

    if len(subscribers) > 10:
        lines.append(f"... и еще {len(subscribers) - 10}")

    return "\n".join(lines)


def format_mailings_list(mailings):
    if not mailings:
        return "Нет рассылок"

    lines = []
    for i, mail in enumerate(mailings[:5], 1):
        date = mail.get('Дата', mail.get('date', ''))
        group = mail.get('Группа', mail.get('group', ''))
        sent = mail.get('Доставлено', mail.get('sent', 0))
        total = mail.get('Всего', mail.get('total', 0))

        lines.append(f"{i}. *{date}*")
        lines.append(f"   📨 {group} | ✅ {sent}/{total}\n")

    return "\n".join(lines)