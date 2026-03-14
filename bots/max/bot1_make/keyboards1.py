from datetime import datetime, timedelta
from config1 import MASTERS, AVAILABLE_TIMES

def get_main_menu():
    return [
        [{"text": "📝 Записаться", "data": "book"}],
        [{"text": "📋 Мои записи", "data": "my_bookings"}],
        [{"text": "ℹ️ О салоне", "data": "about"}],
    ]

def get_masters_keyboard():
    keyboard = []
    for master in MASTERS:
        keyboard.append([{
            "text": f"{master['emoji']} {master['name']}",
            "data": f"master_{master['id']}"
        }])
    keyboard.append([{"text": "❌ Отмена", "data": "cancel"}])
    return keyboard

def get_dates_keyboard():
    keyboard = []
    today = datetime.now()
    for i in range(7):
        date = today + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        display_str = date.strftime("%d.%m (%a)")
        keyboard.append([{
            "text": display_str,
            "data": f"date_{date_str}"
        }])
    keyboard.append([{"text": "⬅️ Назад", "data": "back_to_masters"}])
    return keyboard

def get_times_keyboard():
    keyboard = []
    for time in AVAILABLE_TIMES:
        keyboard.append([{
            "text": time,
            "data": f"time_{time}"
        }])
    keyboard.append([{"text": "⬅️ Назад", "data": "back_to_dates"}])
    return keyboard

def get_cancel_keyboard():
    return [[{"text": "❌ Отменить запись", "data": "cancel_booking"}]]