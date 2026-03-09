import gspread
import datetime
from google.oauth2.service_account import Credentials
from config1 import SHEET_URL


class SimpleDatabase:
    def __init__(self):
        self.sheet = None
        self.connect()

    def connect(self):
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                'https://www.googleapis.com/auth/drive'
            ]
            creds = Credentials.from_service_account_file(
                "creds1.json",
                scopes=scopes
            )
            client = gspread.authorize(creds)
            self.sheet = client.open_by_url(SHEET_URL).sheet1
            print("К Google Sheets подключено")


            if self.sheet:
                print(f"Лист: {self.sheet.title}")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            self.sheet = None

    def add_booking(self, user_data: dict):
        if not self.sheet:
            print("Лист не подключен, пытаемся подключиться...")
            self.connect()
            if not self.sheet:
                return False

        try:
            row = [
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                user_data.get('user_id', ''),
                user_data.get('username', ''),
                user_data.get('name', ''),
                user_data.get('phone', ''),
                user_data.get('master', ''),
                user_data.get('date', ''),
                user_data.get('time', ''),
                user_data.get('comment', ''),
                'новая'
            ]

            print(f"Пытаемся добавить запись: {row}")

            self.sheet.append_row(row)
            print(f"Запись добавлена в таблицу")
            return True

        except Exception as e:
            print(f"Ошибка при добавлении записи: {e}")
            return False

    def get_today_bookings(self):
        if not self.sheet:
            self.connect()
            if not self.sheet:
                return []

        try:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            records = self.sheet.get_all_records()

            print(f"Всего записей в таблице: {len(records)}")

            today_bookings = []
            for record in records:

                record_date = str(record.get('Дата', '') or record.get('date', ''))
                if today in record_date:
                    today_bookings.append(record)

            print(f"На сегодня записей: {len(today_bookings)}")
            return today_bookings
        except Exception as e:
            print(f"Ошибка чтения записей: {e}")
            return []

    def get_user_bookings(self, user_id):
        if not self.sheet:
            if not self.connect():
                return []

        try:
            all_records = self.sheet.get_all_records()

            if not all_records:
                print("Таблица пуста")
                return []

            if len(all_records) > 0:
                print(f"Ключи в записи: {list(all_records[0].keys())}")

            user_bookings = []
            for record in all_records:
                record_user_id = None

                possible_keys = [
                    'ID пользователя',
                    'ID',
                    'user_id',
                    'UserId',
                    'Пользователь',
                    'User ID'
                ]

                for key in possible_keys:
                    if key in record:
                        record_user_id = str(record.get(key, ''))
                        break

                if record_user_id and record_user_id == str(user_id):
                    user_bookings.append(record)
                elif str(user_id) in str(record):
                    if str(user_id) in str(record.values()):
                        user_bookings.append(record)

            user_bookings.sort(
                key=lambda x: str(x.get('Дата визита', x.get('Дата', ''))),
                reverse=True
            )

            print(f"Найдено записей для пользователя {user_id}: {len(user_bookings)}")
            return user_bookings

        except Exception as e:
            print(f"Ошибка получения записей пользователя: {e}")
            import traceback
            traceback.print_exc()
            return []



db = SimpleDatabase()