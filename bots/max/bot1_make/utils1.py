from datetime import datetime
from config1 import MASTERS


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")
    except:
        return date_str


def get_master_by_id(master_id):
    return next((m for m in MASTERS if m["id"] == master_id), None)


def format_bookings_list(bookings):
    if not bookings:
        return ""

    lines = []
    for i, booking in enumerate(bookings[:5], 1):
        date = booking.get('date', '')
        time = booking.get('time', '')
        master = booking.get('master', '')

        lines.append(f"{i}. *{format_date(date)}* в *{time}*")
        lines.append(f"   👩‍🎨 Мастер: {master}\n")

    return "\n".join(lines)