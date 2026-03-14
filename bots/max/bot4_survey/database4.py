import gspread
import datetime
import json
from google.oauth2.service_account import Credentials
from config4 import SURVEY_SETTINGS


class SurveyDatabase:
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
                "creds4.json",
                scopes=scopes
            )
            client = gspread.authorize(creds)
            self.sheet = client.open_by_url(SURVEY_SETTINGS['sheet_url']).sheet1
            print("✅ Подключено к Google Sheets")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            self.sheet = None

    def save_survey_result(self, survey_data):
        if not self.sheet:
            return False

        try:
            answers_json = json.dumps(survey_data.get('answers', []), ensure_ascii=False)
            row = [
                survey_data.get('date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                survey_data.get('user_id', ''),
                survey_data.get('username', ''),
                survey_data.get('survey_name', ''),
                answers_json
            ]
            self.sheet.append_row(row)
            return True
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False

    def get_user_surveys(self, user_id):
        if not self.sheet:
            return []
        try:
            records = self.sheet.get_all_records()
            user_surveys = []
            for record in records:
                if str(record.get('ID пользователя', '')) == str(user_id):
                    user_surveys.append(record)
            return user_surveys
        except:
            return []


db = SurveyDatabase()