import gspread
import datetime
from google.oauth2.service_account import Credentials
from config5 import MAILER_SETTINGS


class MailerDatabase:
    def __init__(self):
        self.subscribers_sheet = None
        self.mailings_sheet = None
        self.connect()

    def connect(self):
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                'https://www.googleapis.com/auth/drive'
            ]
            creds = Credentials.from_service_account_file(
                "creds5.json",
                scopes=scopes
            )
            client = gspread.authorize(creds)
            spreadsheet = client.open_by_url(MAILER_SETTINGS['sheet_url'])

            # Создаем листы если их нет
            try:
                self.subscribers_sheet = spreadsheet.worksheet("Подписчики")
            except:
                self.subscribers_sheet = spreadsheet.add_worksheet("Подписчики", 1000, 20)
                self.subscribers_sheet.append_row([
                    "Дата подписки", "ID пользователя", "Username",
                    "Имя", "Активен", "Группы"
                ])

            try:
                self.mailings_sheet = spreadsheet.worksheet("Рассылки")
            except:
                self.mailings_sheet = spreadsheet.add_worksheet("Рассылки", 1000, 20)
                self.mailings_sheet.append_row([
                    "Дата", "Группа", "Текст", "Всего", "Доставлено", "Ошибок"
                ])

            print("✅ Подключено к Google Sheets")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def add_subscriber(self, user_id, username, full_name):
        if not self.subscribers_sheet:
            return False

        try:
            if self.is_subscribed(user_id):
                return False

            row = [
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_id,
                username,
                full_name,
                "Да",
                "1"
            ]
            self.subscribers_sheet.append_row(row)
            return True
        except:
            return False

    def remove_subscriber(self, user_id):
        if not self.subscribers_sheet:
            return False

        try:
            records = self.subscribers_sheet.get_all_records()
            for i, record in enumerate(records, start=2):
                if str(record.get('ID пользователя', '')) == str(user_id):
                    self.subscribers_sheet.update_cell(i, 5, "Нет")
                    return True
        except:
            pass
        return False

    def is_subscribed(self, user_id):
        if not self.subscribers_sheet:
            return False

        try:
            records = self.subscribers_sheet.get_all_records()
            for record in records:
                if (str(record.get('ID пользователя', '')) == str(user_id) and
                        record.get('Активен', '') == "Да"):
                    return True
        except:
            pass
        return False

    def get_all_subscribers(self):
        if not self.subscribers_sheet:
            return []

        subscribers = []
        try:
            records = self.subscribers_sheet.get_all_records()
            for record in records:
                if record.get('Активен', '') == "Да":
                    subscribers.append({
                        'user_id': int(record.get('ID пользователя', 0)),
                        'username': record.get('Username', ''),
                        'name': record.get('Имя', '')
                    })
        except:
            pass
        return subscribers

    def get_stats(self):
        if not self.subscribers_sheet:
            return {'total': 0, 'active': 0}

        try:
            records = self.subscribers_sheet.get_all_records()
            total = len(records)
            active = sum(1 for r in records if r.get('Активен', '') == "Да")
            return {'total': total, 'active': active}
        except:
            return {'total': 0, 'active': 0}

    def save_mailing(self, mailing_data):
        if not self.mailings_sheet:
            return False

        try:
            row = [
                mailing_data.get('date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                mailing_data.get('group', ''),
                mailing_data.get('text', ''),
                mailing_data.get('total', 0),
                mailing_data.get('sent', 0),
                mailing_data.get('failed', 0)
            ]
            self.mailings_sheet.append_row(row)
            return True
        except:
            return False


db = MailerDatabase()