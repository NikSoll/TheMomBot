import gspread
import datetime
from google.oauth2.service_account import Credentials
from config2 import SHOP_SETTINGS


class ShopDatabase:
    def __init__(self, creds_file="creds2.json"):
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

            if SHOP_SETTINGS.get('sheet_url'):
                self.sheet = client.open_by_url(SHOP_SETTINGS['sheet_url']).sheet1
                print("✅ Подключено к Google Sheets")
            else:
                print("⚠️ URL таблицы не указан в настройках")
        except Exception as e:
            print(f"❌ Ошибка подключения к Google Sheets: {e}")
            self.sheet = None

    def add_order(self, order_data: dict):
        if not self.sheet:
            print("❌ Нет подключения к таблице")
            return False

        try:
            cart_summary = "\n".join([
                f"{item['name']} - {item['price']}₽"
                for item in order_data.get('cart', [])
            ])

            row = [
                order_data.get('created_at', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                order_data.get('user_id', ''),
                order_data.get('username', ''),
                order_data.get('name', ''),
                order_data.get('phone', ''),
                order_data.get('address', ''),
                order_data.get('comment', ''),
                cart_summary,
                order_data.get('total', 0),
                SHOP_SETTINGS.get('currency', '₽'),
                'новый'
            ]

            self.sheet.append_row(row)
            print(f"✅ Заказ #{order_data.get('user_id')} сохранен в таблицу")
            return True

        except Exception as e:
            print(f"❌ Ошибка при сохранении заказа: {e}")
            return False

    def get_user_orders(self, user_id):
        if not self.sheet:
            return []

        try:
            records = self.sheet.get_all_records()
            user_orders = []

            for record in records:
                if str(record.get('ID пользователя', '')) == str(user_id):
                    user_orders.append(record)

            return user_orders
        except Exception as e:
            print(f"❌ Ошибка получения заказов: {e}")
            return []

    def get_today_orders(self):
        if not self.sheet:
            return []

        try:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            records = self.sheet.get_all_records()
            today_orders = []

            for record in records:
                created_at = str(record.get('Дата создания', ''))
                if today in created_at:
                    today_orders.append(record)

            return today_orders
        except Exception as e:
            print(f"❌ Ошибка получения заказов: {e}")
            return []


db = ShopDatabase()