import gspread
import datetime
from google.oauth2.service_account import Credentials
from config3 import QUIZ_SETTINGS


class QuizDatabase:
    def __init__(self, creds_file="creds3.json"):
        self.creds_file = creds_file
        self.sheet = None
        self.connect()

    def connect(self):
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                'https://www.googleapis.com/auth/drive'
            ]
            creds = Credentials.from_service_account_file(
                self.creds_file,
                scopes=scopes
            )
            client = gspread.authorize(creds)

            if QUIZ_SETTINGS.get('sheet_url'):
                self.sheet = client.open_by_url(QUIZ_SETTINGS['sheet_url']).sheet1
                print("✅ Подключено к Google Sheets")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            self.sheet = None

    def save_result(self, result_data):
        if not self.sheet:
            return False

        try:
            points_str = ", ".join([f"{k}:{v}" for k, v in result_data.get('points', {}).items()])

            row = [
                result_data.get('date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                result_data.get('user_id', ''),
                result_data.get('username', ''),
                result_data.get('quiz_name', ''),
                result_data.get('result', ''),
                points_str
            ]

            self.sheet.append_row(row)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False

    def get_user_results(self, user_id):
        if not self.sheet:
            return []

        try:
            records = self.sheet.get_all_records()
            user_results = []
            for record in records:
                if str(record.get('ID пользователя', '')) == str(user_id):
                    user_results.append(record)
            return user_results
        except:
            return []


db = QuizDatabase()