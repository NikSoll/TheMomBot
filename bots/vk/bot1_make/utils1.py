from datetime import datetime


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")
    except:
        return date_str


def get_master_by_id(master_id):
    from .config1 import MASTERS
    return next((m for m in MASTERS if m["id"] == master_id), None)


def format_bookings_list(bookings):
    if not bookings:
        return ""

    lines = []
    for i, booking in enumerate(bookings, 1):
        date = booking.get('Дата визита', booking.get('date', ''))
        time = booking.get('Время', booking.get('time', ''))
        master = booking.get('Мастер', booking.get('master', ''))
        status = booking.get('Статус', booking.get('status', 'новая'))

        status_emoji = "✅" if "новая" in status.lower() else "⏳"

        lines.append(f"{i}. *{date}* в *{time}*")
        lines.append(f"   👩‍🎨 Мастер: {master}")
        lines.append(f"   {status_emoji} Статус: {status}\n")

    if len(bookings) > 5:
        lines.append(f"_Показаны последние 5 из {len(bookings)} записей_")

    return "\n".join(lines)