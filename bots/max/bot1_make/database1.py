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
            print("✅ Подключено к Google Sheets")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            self.sheet = None

    def add_booking(self, user_data):
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
            self.sheet.append_row(row)
            return True
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False

    def get_user_bookings(self, user_id):
        if not self.sheet:
            return []

        try:
            records = self.sheet.get_all_records()
            user_bookings = []
            for record in records:
                if str(record.get('ID пользователя', '')) == str(user_id):
                    user_bookings.append(record)
            return user_bookings
        except:
            return []


db = SimpleDatabase()